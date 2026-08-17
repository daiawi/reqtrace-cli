# src/reqtrace/cli_scan.py
from pathlib import Path

import click

from ..core.discover import Package, find_packages


@click.command()
@click.option('--dir', 
	type=click.Path(
		exists=True, 
		file_okay=False, 
		path_type=Path), 
	default='.'
)
@click.option('--all', 
	'show_all', 
	is_flag=True, 
	help="Include packages without requirements.", 
	default=False
)
@click.option('--requirements', 
	'req_paths_only', 
	is_flag=True,
	help="Print only paths to requirements files"
	)
def scan(dir: Path, show_all: bool, req_paths_only: bool):
	"""Search directory for paths to requirements, tests, and package descriptions"""
	all_packages = find_packages(dir)

	# Filter package list based on whether requirements are present
	packages = (
		all_packages
		if show_all
		else [pkg for pkg in all_packages if pkg.requirements_md]
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