# src/reqtrace/cli.py
import click

from .parse import parse
from .report import report
from .scan import scan


@click.group()
def cli():
	"""reqtrace: build requirements-to-tests traceability report"""


cli.add_command(scan)
cli.add_command(parse)
cli.add_command(report)
