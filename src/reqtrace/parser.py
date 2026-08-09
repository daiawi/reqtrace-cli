import click
from typing import TextIO

@click.command()
@click.argument('file', type = click.File('r'))
def cli(file: TextIO):
	print(file.read())