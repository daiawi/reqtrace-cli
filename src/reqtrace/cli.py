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
def scan(dir: Path):
	"""Search directory for requirements, tests, and package descriptions"""
	project = find_packages(dir)

	click.echo(f"Showing results for directories under {project.root.resolve()}")

	if not project.packages:
		click.echo("  No package.xml files found.")
		return

	for pkg in project.packages:
		click.echo(f"\nPackage: {pkg.root}")
		click.echo(_format_paths("REQUIREMENTS", pkg.requirements_md))

# AI-Generated Function
def _format_paths(label: str, paths: list[Path]) -> str:
    if not paths:
        return f"\t{label}: MISSING"
    if len(paths) == 1:
        return f"\t{label}: {paths[0]}"
    lines = [f"\t{label}: {len(paths)} found"]
    lines += [f"\t\t- {p}" for p in paths]
    return "\n".join(lines)