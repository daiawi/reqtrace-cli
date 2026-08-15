# src/reqtrace/cli.py
import click

from .cli_scan import scan
from .cli_parse import parse


@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""
	pass


cli.add_command(scan)
cli.add_command(parse)
