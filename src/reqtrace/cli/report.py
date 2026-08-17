from pathlib import Path

import click

from ..core.discover import Package, find_packages
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
	project = find_packages(dir)

	packages = [pkg for pkg in project.packages if pkg.requirements_md]

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

	print("Number of Requirements", len(all_reqs))
	print("Number of tests", len(all_test_traces))
	