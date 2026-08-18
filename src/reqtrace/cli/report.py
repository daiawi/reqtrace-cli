from pathlib import Path

import click

from ..core.discover import find_packages
from ..core.trace import extract_req_trace


@click.command()
@click.option('--dir', 
	type=click.Path(
		exists=True, 
		file_okay=False, 
		path_type=Path), 
	default='.'
)
def report(dir):
	"""Creates a requirements-to-tests traceability report."""
	all_packages = find_packages(dir)

	packages = [pkg for pkg in all_packages if pkg.requirements_md]

	# Stage 1: Collect all requirements / test traces
	for pkg in packages:
		reqtraces = extract_req_trace(pkg)
		print(reqtraces)

