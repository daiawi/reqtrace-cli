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