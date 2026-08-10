# src/reqtrace/cli.py
import click
from pathlib import Path

from .discover import find_packages
from .parse import validate_requirements_file

@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


@cli.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.')
def scan(dir: Path):
	"""Search directory for paths to requirements, tests, and package descriptions"""
	project = find_packages(dir)

	click.echo(f"Showing results for directories under {project.root.resolve()}")

	if not project.packages:
		click.echo("  No package.xml files found.")
		return

	for pkg in project.packages:
		click.echo(f"\nPackage: {pkg.root}")
		click.echo(_format_paths("REQUIREMENTS", pkg.requirements_md))
		click.echo(_format_paths("TESTS", pkg.tests))


# AI-Generated Function
def _format_paths(label: str, paths: list[Path]) -> str:
    if not paths:
        return f"\t{label}: MISSING"
    if len(paths) == 1:
        return f"\t{label}: {paths[0]}"
    lines = [f"\t{label}: {len(paths)} found"]
    lines += [f"\t\t- {p}" for p in paths]
    return "\n".join(lines)


@cli.group()
def parse():
	"""Validate formatting of requirements and test traceability."""
	pass


@parse.command()
@click.argument("file", type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path))
def requirements(file: Path):
	"""Extract requirements from REQUIREMENTS.md files."""
	issues = validate_requirements_file(file)

	has_errors = any(issue.level == "error" for issue in issues)

	if issues:
		click.echo(f"!! REQUIREMENTS FILE HAS PROBLEMS !!\n")

		for issue in issues:
			click.secho(f"{issue.level.upper()}" + f"\n{issue.message}\n", 
			   fg= "red" if issue.level == "error" else "yellow")

		if has_errors:
			raise click.exceptions.Exit(1)


@parse.command()
def pytest():
	"""Extract traceability from pytest testcases."""
	pass