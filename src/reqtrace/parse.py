# src/reqtrace/parse.py
from collections import defaultdict
from .models import FormatIssue, Requirement
from pathlib import Path


def validate_requirements_file(file: Path) -> list[FormatIssue]:
	issues = []
	lines = file.read_text().splitlines()

	if file.name != "REQUIREMENTS.md":
		issues.append(FormatIssue("error", f"{file.name} must be named REQUIREMENTS.md to be found")) 

	if not lines:
		issues.append(FormatIssue("error", f"Provided file is empty and/or contains no text"))
		return issues

	if not lines[0].startswith("# "):
		issues.append(FormatIssue("warning", "Requirements missing title on first line (expected: # Title)" ))

	reqs = extract_requirements(lines)
	issues += check_for_duplicate_requirements(reqs)

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
				f"Duplicate requirement ID '{req_id}' " +
				f"found on lines {', '.join(map(str,lines))}"
			))
	
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