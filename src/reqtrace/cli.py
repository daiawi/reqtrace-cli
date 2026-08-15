# src/reqtrace/cli.py
import click
from pathlib import Path

from .discover import find_packages, Package
from .parse import parse_requirements_file, filter_valid_requirements

@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


@cli.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.')
@click.option('--all', 'show_all', is_flag=True, help="Include packages without requirements.", default=False)
@click.option('--requirements', 'req_paths_only', is_flag=True)
def scan(dir: Path, show_all: bool, req_paths_only: bool):
	"""Search directory for paths to requirements, tests, and package descriptions"""
	project = find_packages(dir)

	# Filter package list based on whether requirements are present
	packages = (
		project.packages
		if show_all
		else [pkg for pkg in project.packages if pkg.requirements_md]
	)
	
	if req_paths_only:
		_print_requirements(packages)
	else:
		_print_scan_report(dir, packages)

def _print_requirements(packages: list[Package]):
	for pkg in packages:
		for requirement in pkg.requirements_md:
			click.echo(requirement.resolve())

def _print_scan_report(dir: Path, packages):
	click.echo(f"Showing results for directories under {dir.resolve()}")

	if not packages:
		click.echo("No package.xml files found.", err=True)
		return

	if not packages:
		click.echo("  No packages with REQUIREMENTS.md files found.")

	for pkg in packages:
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
	parsed_reqs = parse_requirements_file(file)

	has_errors = any(issue.level == "error" for issue in parsed_reqs.issues)

	if parsed_reqs.issues:
		click.echo(f"!! REQUIREMENTS FILE HAS PROBLEMS !!\n")

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


@parse.command()
def pytest():
	"""Extract traceability from pytest testcases."""
	pass