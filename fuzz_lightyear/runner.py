from typing import List

from .datastore import get_user_defined_mapping
from .request import FuzzingRequest
from .response import ResponseSequence


def run_sequence(
    sequence: List[FuzzingRequest],
    responses: ResponseSequence,
):
    # First, determine whether this is a successful request sequence.
    for request in sequence:
        response = request.send(
            data=responses.data,
        )

        responses.add_response(response)

        # The Response object already saves the output of the response.
        # However, we also still want to save some of the *inputs* to the
        # request, if they were factory-generated. This tries to ensure
        # the same object is referenced throughout the sequence, rather than
        # having the fuzzing engine constantly generate new objects.
        for key in request.fuzzed_input:
            if key in get_user_defined_mapping():
                responses.data[key] = request.fuzzed_input[key]

    # Then, check for vulnerabilities.
    responses.analyze_requests(sequence)
    return responses
