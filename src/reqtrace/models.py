# src/reqtrace/models.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class Package:
	root: Path
	package_xml: Path
	requirements_md: list[Path] = field(default_factory=list)
	tests: list[Path] = field(default_factory=list)


@dataclass
class Project:
	root: Path
	packages: list[Package] = field(default_factory=list)


@dataclass
class FormatIssue:
	level: Literal["warning", "error"]
	message: str
	req_id: str | None = None


@dataclass
class Requirement:
	id: str
	description: str
	line_number: int | None = None
	category: str | None = None


@dataclass
class ParsedRequirements:
	requirements: list[Requirement] | None
	issues: list[FormatIssue]


@dataclass
class TestTrace:
	test_id: str
	req_ids: list[str]