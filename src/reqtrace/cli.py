import typer

from .parser import parse

app = typer.Typer()
app.command()(parse)


if __name__ == "__main__":
	app()