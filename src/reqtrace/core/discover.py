# src/reqtrace/discover.py

from pathlib import Path

from .models import Package


def find_packages(root: Path) -> list[Package]:
	packages = []
	for package_xml in root.rglob("package.xml"):
		pkg_root = package_xml.parent

		requirements = list(pkg_root.rglob("REQUIREMENTS.md"))
		tests = find_tests(pkg_root)

		packages.append(Package(
			root=pkg_root,
			package_xml=package_xml,
			requirements_md=requirements,
			tests=tests
		))

	return packages

def find_tests(root: Path) -> list[Path]:
	return list(root.rglob("test_*.py")) + list(root.rglob("*_test.py"))