# src/reqtrace/parse.py
from collections import defaultdict
from pathlib import Path

from .models import FormatIssue, ParsedRequirements, Requirement


def parse_requirements_file(file: Path) -> ParsedRequirements:
	lines = file.read_text().splitlines()

	issues = check_file_format(file.name, lines)

	has_errors = any(issue.level == "error" for issue in issues)

	if has_errors:
		return ParsedRequirements(requirements= None, issues=issues)

	reqs = extract_requirements(lines)
	issues += check_for_no_requirements(reqs)
	issues += check_for_empty_fields(reqs)
	issues += check_for_duplicate_requirements(reqs)

	return ParsedRequirements(requirements=reqs, issues=issues)


def check_file_format(file_name: str, lines: list[str]) -> list[FormatIssue]:
	issues = []

	if file_name != "REQUIREMENTS.md":
		issues.append(FormatIssue("error", f"{file_name} must be named REQUIREMENTS.md to be found"))

	if not lines:
		issues.append(FormatIssue("error", "Provided file is empty and/or contains no text"))
		return issues

	if not lines[0].startswith("# "):
		issues.append(FormatIssue("warning", "Requirements missing title on first line (expected: # Title)" ))

	return issues


def extract_requirements(lines: list[str]) -> list[Requirement]:
	reqs = []
	category = None

	for line_number, line in enumerate(lines, start=1):
			stripped = line.strip()

			if not stripped:
				continue

			if stripped.startswith("## "):
				category = stripped[2:]
				continue

			parts = line.split(":", 1)

			if len(parts) != 2:
				continue

			id = parts[0].strip()
			description = parts[1].strip()
			reqs.append(Requirement(
				id=id,
				description=description,
				line_number=line_number,
				category=category
			))

	return reqs


def check_for_no_requirements(reqs: list[Requirement]) -> list[FormatIssue]:
	issues = []

	if not reqs:
		issues.append(FormatIssue(
			"error",
			"No requirements were found. Expected format is 'REQ-ID: Description'"
		))

	return issues


def check_for_empty_fields(reqs: list[Requirement]) -> list[FormatIssue]:
	issues = []

	for req in reqs:
		if not req.id:
			issues.append(FormatIssue(
				"error",
				f"Missing ID (somehow) on line {req.line_number}",
				req_id=req.id
			))
		elif not req.description:
			issues.append(FormatIssue(
				"warning",
				f"Missing description for '{req.id}' on line {req.line_number}",
				req_id=req.id
			))

	return issues


def check_for_duplicate_requirements(reqs: list[Requirement])-> list[FormatIssue]:
	id_lines = defaultdict(list)

	for req in reqs:
		id_lines[req.id].append(req.line_number)

	issues = []

	for req_id, lines in id_lines.items():
		if len(lines) > 1:
			issues.append(FormatIssue(
				"warning",
				f"Duplicate requirement ID '{req_id}' found on lines {', '.join(map(str,lines))}",
				req_id=req.id
			))

	return issues
