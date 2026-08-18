from collections import defaultdict

from .models import Requirement, RequirementTrace, TestTrace


def trace_requirement(requirement: Requirement, tests: list[TestTrace]) -> RequirementTrace:
	id = requirement.id
	description = requirement.description
	test_ids = [
        test.test_id
        for test in tests
        if requirement.id in test.req_ids
    ]

	return RequirementTrace(req_id=id, description=description, test_ids=test_ids)

def build_requirement_test_map(traces: list[TestTrace]):
	requirements = defaultdict(list)

	for trace in traces:
		for req_id in trace.req_ids:
			requirements[req_id].append(trace.test_id)

	return requirements