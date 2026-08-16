# src/reqtrace/cli_parse.py
from pathlib import Path

import click
import pytest

from ..core.parse import filter_valid_requirements, parse_requirements_file
from ..pytest_plugin import ReqtracePlugin


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
		_parse_requirements(file)


def _parse_requirements(file: Path):
	parsed_reqs = parse_requirements_file(file)
	
	has_errors = any(issue.level == "error" for issue in parsed_reqs.issues)

	if parsed_reqs.issues:
		click.echo("!! REQUIREMENTS FILE HAS PROBLEMS !!\n")

		for issue in parsed_reqs.issues:
			click.secho(f"{issue.level.upper()}" + f"\n{issue.message}\n",
				fg= "red" if issue.level == "error" else "yellow")

		if has_errors:
			raise click.exceptions.Exit(1)

	valid_reqs = filter_valid_requirements(parsed_reqs)

	if valid_reqs:
		click.echo(f"Found {len(valid_reqs)} valid requirements:\n")

		for req in valid_reqs:
			click.echo(f"\t{req.id}: {req.description}\n")


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
	plugin = ReqtracePlugin()

	exit_code = pytest.main(
		[
			"--collect-only",
			"-p",
        	"no:terminal",
			str(file),
		],
		plugins=[plugin]
	)

	if exit_code != 0:
		raise click.ClickException(
			"pytest collection failed"
		)

	click.echo(f"File: {file}\n")
	click.echo(plugin.report())

