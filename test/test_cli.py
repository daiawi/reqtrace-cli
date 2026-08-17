from textwrap import dedent

from click.testing import CliRunner

from reqtrace.cli.main import cli


def test_parse_requirements_succeeds(tmp_path):
	requirements = tmp_path / "REQUIREMENTS.md"
	requirements.write_text(
		"# Requirements\n\n"
		"## Authentication\n"
		"REQ-001: User can log in\n"
		"REQ-002: User can log out\n"
	)

	result = CliRunner().invoke(
		cli,
		["parse", "requirements", str(requirements)],
	)

	assert result.exit_code == 0
	assert "Found 2 valid requirements:" in result.output
	assert "REQ-001: User can log in" in result.output
	assert "REQ-002: User can log out" in result.output


def test_parse_requirements_invalid_file_fails(tmp_path):
	requirements = tmp_path / "REQUIREMENTS.md"
	requirements.write_text("")

	result = CliRunner().invoke(
		cli,
		["parse", "requirements", str(requirements)],
	)

	assert result.exit_code == 1
	assert "REQUIREMENTS FILE HAS PROBLEMS" in result.output
	assert "Provided file is empty" in result.output


def test_parse_pytest_succeeds(tmp_path):
	test = tmp_path / "test_something.py"
	test.write_text(dedent("""
		import pytest

		@pytest.mark.req("REQ-1")
		def test_first_req():
			assert 1 == 1

		@pytest.mark.req("REQ-2")
		@pytest.mark.parametrize("shouldPass",
			[
				pytest.param(True, id="normal"),
				pytest.param(True, id="tests-req-3", marks=pytest.mark.req("REQ-3"))
			]
		)
		def test_parameters(shouldPass):
			assert shouldPass
	""")
	)

	result = CliRunner().invoke(
		cli,
		["parse", "pytest", str(test)],
	)

	assert result.exit_code == 0, result.output
	assert "Requirements: 3" in result.output


def test_scan_finds_requirements(tmp_path):
	package = tmp_path / "my_package"
	package.mkdir()

	(package / "package.xml").write_text("<package></package>")
	(package / "REQUIREMENTS.md").write_text("# Requirements\n")

	result = CliRunner().invoke(
		cli,
		["scan", "--dir", str(tmp_path)],
	)

	assert result.exit_code == 0
	assert "my_package" in result.output
	assert "REQUIREMENTS" in result.output
