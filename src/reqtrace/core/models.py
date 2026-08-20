# src/reqtrace/models.py
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Literal


@dataclass
class Package:
	root: Path
	package_path: Path
	package_type: PackageType
	requirements_md: list[Path] = field(default_factory=list)
	tests: list[Path] = field(default_factory=list)


class PackageType(StrEnum):
	PYTHON = "pyproject.toml"
	ROS = "package.xml"


@dataclass
class SoftwareInfo:
	name: str
	version: str

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

	@property
	def valid_reqs(self) -> list[Requirement]:
		if self.requirements is None:
			return []

		invalid_ids = {
			issue.req_id
			for issue in self.issues
			if issue.req_id is not None
		}

		return [req for req in self.requirements if req.id not in invalid_ids]


@dataclass
class TestTrace:
	test_id: str
	req_ids: list[str]


@dataclass
class RequirementTrace:
	req_id: str
	description: str
	test_ids: list[str]


@dataclass
class TraceReport:
	software: SoftwareInfo
	requirements: list[RequirementTrace]

	def to_dict(self):
		return asdict(self)

	def to_json(self):
		return json.dumps(self.to_dict(), indent=2)


def reports_to_json(reports: list[TraceReport]) -> str:
    return json.dumps(
        [report.to_dict() for report in reports],
        indent=2,
    )