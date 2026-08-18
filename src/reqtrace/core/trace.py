from collections import defaultdict

from .models import Package, RequirementTrace, TestTrace
from .parse import collect_pytest, parse_requirements_file


def build_requirement_test_map(traces: list[TestTrace]):
	requirements = defaultdict(list)

	for trace in traces:
		for req_id in trace.req_ids:
			requirements[req_id].append(trace.test_id)

	return requirements

def extract_req_traces(package: Package) -> list[RequirementTrace]:
	requirements = []
	for file in package.requirements_md:
		parsed_reqs = parse_requirements_file(file)
		requirements.extend(parsed_reqs.valid_reqs)

	pkg_test_traces = []
	for file in package.tests:
		traces = collect_pytest(file)
		pkg_test_traces.extend(traces)

	req_to_test = build_requirement_test_map(pkg_test_traces)

	req_traces = []
	for req in requirements:
		req_traces.append(RequirementTrace(
		req_id=req.id,
		description=req.description,
		test_ids=req_to_test.get(req.id, [])
		))

	return req_traces