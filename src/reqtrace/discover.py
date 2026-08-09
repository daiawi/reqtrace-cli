# src/reqtrace/discover.py

from .models import Package, Project
from pathlib import Path

def find_packages(root: Path) -> Project:
	packages = []
	for package_xml in root.rglob("package.xml"):
		pkg_root = package_xml.parent

		requirements = list(pkg_root.rglob("REQUIREMENTS.md"))

		packages.append(Package(
			root=pkg_root,
			package_xml=package_xml,
			requirements_md=requirements
		))

	return Project(root=root, packages=packages)