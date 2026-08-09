# src/reqtrace/cli.py
import click
from pathlib import Path

@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


@cli.command()
@click.option('--dir', type=click.Path(exists=True, file_okay=False, path_type=Path), default='.')
def scan(dir: Path):
	"""Search directory for requirements, tests, and package descriptions"""
	all_files = dir.rglob("*.md")
	print(*[file for file in all_files], sep="\n")
