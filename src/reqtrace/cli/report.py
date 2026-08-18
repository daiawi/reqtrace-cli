from pathlib import Path

import click

from ..core.discover import find_packages
from ..core.trace import trace_requirement
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
	all_reqs = []
	all_test_traces =[]

	for pkg in packages:
		for file in pkg.requirements_md:
			valid_reqs = _parse_requirements(file)
			all_reqs.extend(valid_reqs)

		for file in pkg.tests:
			traces = _collect_pytest(file)
			all_test_traces.extend(traces)

	for requirement in all_reqs:
		req_trace = trace_requirement(requirement, all_test_traces)
		print(req_trace)
		print("\n")