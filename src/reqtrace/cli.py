# src/reqtrace/cli.py
import click
from pathlib import Path

from .discover import find_packages

@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


@cli.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.')
@click.option('--all', 'show_all', is_flag=True, help="Include packages without requirements.", default=False)
def scan(dir: Path, show_all: bool):
	"""Search directory for paths to requirements, tests, and package descriptions"""
	project = find_packages(dir)

	click.echo(f"Showing results for directories under {project.root.resolve()}")

	if not project.packages:
		click.echo("  No package.xml files found.")
		return

	# Filter package list to only those containing requirements
	packages = project.packages if show_all else [
		pkg for pkg in project.packages if pkg.requirements_md
	]

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