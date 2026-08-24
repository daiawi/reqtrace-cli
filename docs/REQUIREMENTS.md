# Requirements

## Parse Requirements
REQ-01: The parser shall extract a requirement id and description from correctly formatted requirements.

REQ-02: The parser shall return an issue for each improperly formatted requirement file.

REQ-03: The parser shall return an issue for each incorrectly formatted requirement.

REQ-04: The parser shall be able to support a requirement spanning multiple lines 
without separating blank lines.

REQ-05: The parser shall not return an issue if the file and all requirements are correctly formatted.

## Discover Requirements
REQ-06: The scan shall identify packages containing a pyproject.toml file.

REQ-07: The scan shall identify packages containing a package.xml file.

REQ-08: The scan shall attempt to collect REQUIREMENTS.md files for each identified package.

REQ-09: The scan shall attempt to collect pytest test files for each identified package.

REQ-10: The scan shall attempt to collect gtest test files for each identified package.

REQ-11: The scan shall not collect files across package boundaries.

