# src/reqtrace/cli_parse.py
from pathlib import Path

import click

from ..core.models import ParsedRequirements, TestTrace
from ..core.parse import collect_pytest, parse_package_xml, parse_requirements_file
from ..core.trace import build_requirement_test_map


@click.group()
def parse():
	"""Validate formatting of requirements and test traceability."""


@parse.command()
@click.argument("input_file", 
	type=click.Path(
		exists=True, 
		file_okay=True, 
		dir_okay=False, 
		readable=True, 
		path_type=Path, 
		allow_dash=True
	)
)
def requirements(input_file: Path):
	"""Extract requirements from REQUIREMENTS.md files."""

	if input_file == Path("-"):
		files = (
			Path(line.strip())
			for line in click.get_text_stream("stdin")
			if line.strip()
		)
	else:
		files = [input_file]

	for file in files:
		parsed_reqs = parse_requirements_file(file)
		_display_parsed_req_issues(parsed_reqs)

		valid_reqs = parsed_reqs.valid_reqs

		if valid_reqs:
			click.echo(f"Found {len(valid_reqs)} valid requirements:\n")

			for req in valid_reqs:
				click.echo(f"\t{req.id}: {req.description}\n")


def _display_parsed_req_issues(parsed_reqs: ParsedRequirements):
	has_errors = any(issue.level == "error" for issue in parsed_reqs.issues)

	if parsed_reqs.issues:
		click.echo("!! REQUIREMENTS FILE HAS PROBLEMS !!\n")

		for issue in parsed_reqs.issues:
			click.secho(f"{issue.level.upper()}" + f"\n{issue.message}\n",
				fg= "red" if issue.level == "error" else "yellow")

		if has_errors:
			raise click.exceptions.Exit(1)


@parse.command(name="pytest")
@click.argument("file", 
	type=click.Path(
		exists=True, 
		file_okay=True, 
		dir_okay=False, 
		readable=True, 
		path_type=Path, 
		allow_dash=True
	)
)
def parse_pytest(file: Path):
	"""Extract traceability from pytest testcases."""
	traces = collect_pytest(file)
	report = _traceability_report(traces)


	click.echo(f"File: {file}\n")
	click.echo(report)


def _traceability_report(traces: list[TestTrace]) -> str:
	requirements = build_requirement_test_map(traces)

	lines = [
		f"Requirements: {len(requirements)}",
		f"Tests: {len(traces)}",
		"",
	]

	for req_id in sorted(requirements):
		lines.append(f"Requirement ID: {req_id}")

		for test_id in requirements[req_id]:
			test_name = test_id.split("::")[-1]
			lines.append(f"\t- {test_name}")

		lines.append("")

	return "\n".join(lines)


@parse.command(name="package")
@click.argument("file", 
	type=click.Path(
		exists=True, 
		file_okay=True, 
		dir_okay=False, 
		readable=True, 
		path_type=Path, 
		allow_dash=True
	)
)
def parse_package(file: Path):
	"""Extract software information from package"""
	software = parse_package_xml(file)

	click.echo(f"File: {file}\n")
	click.echo(f"Software Name: {software.name}")
	click.echo(f"Version: {software.version}")