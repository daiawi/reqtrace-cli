from pathlib import Path

import click

from ..core.discover import find_packages
from ..core.models import TraceReport, reports_to_json
from ..core.parse import parse_package_xml
from ..core.trace import extract_req_traces


@click.command()
@click.option('--dir', 
	type=click.Path(
		exists=True, 
		file_okay=False, 
		path_type=Path), 
	default='.'
)
@click.option(
	'--json',
	"json_output",
	is_flag=True,
	default=False
)
def report(dir, json_output):
	"""Creates a requirements-to-tests traceability report."""
	all_packages = find_packages(dir)

	packages = [pkg for pkg in all_packages if pkg.requirements_md]

	pkg_reports = []
	for pkg in packages:
		software = parse_package_xml(pkg.package_path)
		reqtraces = extract_req_traces(pkg)

		report = TraceReport(software=software, requirements=reqtraces)
		pkg_reports.append(report)

	if json_output:
		click.echo(reports_to_json(pkg_reports))
	else:
		for report in pkg_reports:
			click.echo(_traceability_report(report))
			


def _traceability_report(report: TraceReport) -> str:
	traces = report.requirements

	test_ids = {
		test_id
		for trace in traces
		for test_id in trace.test_ids
	}

	lines = [
		f"Software: {report.software.name}",
		f"Version: {report.software.version}",
		"",
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
