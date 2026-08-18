from pathlib import Path

import click

from ..core.discover import find_packages
from ..core.models import RequirementTrace
from ..core.trace import extract_req_traces


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
		reqtraces = extract_req_traces(pkg)
		click.echo(f"Results for package: {pkg.root}")
		click.echo(_traceability_report(reqtraces))


def _traceability_report(traces: list[RequirementTrace]) -> str:
	test_ids = {
		test_id
		for trace in traces
		for test_id in trace.test_ids
	}

	lines = [
		f"Requirements: {len(traces)}",
		f"Tests: {len(test_ids)}",
		"",
	]

	for trace in sorted(traces, key=lambda trace: trace.req_id):
		lines.append(f"{trace.req_id}: {trace.description}")

		for test_id in trace.test_ids:
			test_name = test_id.split("::")[-1]
			lines.append(f"\t- {test_name}")

		lines.append("")

	return "\n".join(lines)
