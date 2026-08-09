import typer
from typing_extensions import Annotated

def parse(
		filename: Annotated[str, typer.Argument(help="The path of the file to parse")]
):
	with open(filename) as f:
		print(f.read())

