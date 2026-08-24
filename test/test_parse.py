import pytest

from reqtrace.core.parse import check_file_format, extract_requirements


@pytest.mark.req('REQ-05')
def test_check_file_format_valid():
	issues = check_file_format(
		"REQUIREMENTS.md",
		["# Requirements"]
	)

	assert issues == []


@pytest.mark.req('REQ-02')
@pytest.mark.parametrize("title, lines",
	[
		pytest.param("invalid_title.md", ["# Requirements"], id="bad-title"),
		pytest.param("REQUIREMENTS.md", [""], id="no-content"),
		pytest.param("REQUIREMENTS.md", ["", "REQ-1: Something"], id="no-header")
	]
)
def test_check_file_format_invalid(title, lines):
	issues = check_file_format(
		title, lines
	)

	assert issues != []


@pytest.mark.req("REQ-01")
@pytest.mark.parametrize(
    "lines, req_id, description",
    [
        pytest.param(
            ["REQ-1: Be curious, not judgmental."],
            "REQ-1",
            "Be curious, not judgmental.",
            id="good-req",
        ),
        pytest.param(
            [
                "REQ-2: You know how they say youth is wasted on the young?",
                "Well I say don't let the wisdom of age be wasted on you.",
            ],
            "REQ-2",
            (
                "You know how they say youth is wasted on the young?\n"
                "Well I say don't let the wisdom of age be wasted on you."
            ),
            id="multi-line-req",
        ),
    ],
)

def test_extract_requirements_valid(lines, req_id, description):
	reqs = extract_requirements(lines)

	assert reqs[0].id == req_id
	assert reqs[0].description == description
