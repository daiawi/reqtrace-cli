from pathlib import Path

import click

from ..core.discover import find_packages
from ..core.models import Package, RequirementTrace
from ..core.trace import build_requirement_test_map
from .parse import _collect_pytest, _parse_requirements


@click.command()
@click.option('--dir', 
	type=click.Path(
		exists=True, 
		file_okay=False, 
		path_type=Path), 
	default='.'
)
def report(dir):
	"""Creates a requirements-to-tests traceability report."""
	all_packages = find_packages(dir)

	packages = [pkg for pkg in all_packages if pkg.requirements_md]

	# Stage 1: Collect all requirements / test traces
	for pkg in packages:
		reqtraces = _extract_req_trace(pkg)
		print(reqtraces)


def _extract_req_trace(package: Package) -> list[RequirementTrace]:
	requirements = []
	for file in package.requirements_md:
		valid_reqs = _parse_requirements(file)
		requirements.extend(valid_reqs)

	pkg_test_traces = []
	for file in package.tests:
		traces = _collect_pytest(file)
		pkg_test_traces.extend(traces)

	req_to_test = build_requirement_test_map(pkg_test_traces)

	req_traces = []
	for req in requirements:
		req_traces.append(RequirementTrace(
		req_id=req.id,
		description=req.description,
		test_ids=req_to_test[req.id]
		))

	return req_traces