# src/reqtrace/parse.py
from pathlib import Path
from .models import FormatIssue


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

	return issues