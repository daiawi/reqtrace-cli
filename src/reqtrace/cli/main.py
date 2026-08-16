# src/reqtrace/cli.py
import click

from .scan import scan
from .parse import parse


@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


cli.add_command(scan)
cli.add_command(parse)
