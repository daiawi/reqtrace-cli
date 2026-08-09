# src/reqtrace/models.py
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Package:
	root: Path
	package_xml: Path
	requirements_md: Path | None = None


@dataclass
class Project:
	root: Path
	packages: list[Package] = field(default_factory=list)
