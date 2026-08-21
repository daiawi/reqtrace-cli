# src/reqtrace/discover.py

import os
from pathlib import Path

from .models import Package, PackageType


def find_packages(root: Path) -> list[Package]:
	packages = []

	package_configs = find_package_configs(root)

	for config in package_configs:
		package = collect_package(config, package_configs)
		packages.append(package)

	return packages


def find_package_configs(root: Path) -> set[Path]:
    configs = set()

    for current, dirs, files in os.walk(root):
        current_path = Path(current)

        for package_type in PackageType:
            if package_type.value in files:
                configs.add(current_path / package_type.value)

    return configs


def collect_package(config: Path, package_roots: set[Path]) -> Package:
	package_type = PackageType(config.name)

	requirements = []
	tests = []

	for current, dirs, files in os.walk(config.parent):
		current_path = Path(current)

		for directory in dirs[:]:
			child = current_path / directory

			if child in package_roots and child != config:
				dirs.remove(directory)

		if "REQUIREMENTS.md" in files:
			requirements.append(current_path / "REQUIREMENTS.md")

	return Package(
		root=config.parent,
		package_path=config,
		package_type=package_type,
		requirements_md=requirements,
		tests = tests
	)


def find_tests(root: Path) -> list[Path]:
	return list(root.rglob("test_*.py")) + list(root.rglob("*_test.py"))