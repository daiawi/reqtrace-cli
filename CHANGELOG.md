# Changelog

## [0.0.7] - 2026-08-18

### Added
- New `report` command for reqtrace which finds/parses both requirements and tests


## [0.0.6] - 2026-08-15

### Added
- Pytest plugin to capture [custom markers](https://docs.pytest.org/en/stable/example/markers.html) for requirements tagging
	- Usage: `@pytest.mark.req("REQ-ID")`
- Functionality for `reqtrace parse pytest` which runs `pytest --collect-all` under the hood to collect tests
	- This then stores tests with `req` markers and provides a report of tests per unique marker.

## [0.0.5] - 2026-08-14

### Added
- New options for `reqtrace scan`: `--all` and `--requirements`
	- `--all` shows packages without requirements
	- `--requirements` prints paths to found REQUIREMENTS.md files only
- Parse requirements now supports multiple files through stdin

### Changed
- Abstracted scan and parse logic to helper functions
- Scan no longer shows packages without requirements by default (see: `-all`)

## [0.0.4] - 2026-08-14

### Added
- Added parse to reqtrace cli (usage: `reqtrace parse`)
- Implemented parsing for requirements file (usage: `reqtrace parse requirements FILE`)

## [0.0.3] - 2026-08-09

### Added
- Introduced dataclasses for project and package file paths in models.py
- Wrote logic for package discovery in discover.py

### Changed
- Updated `cli scan` command to show results of package discovery

## [0.0.2] - 2026-08-09

### Changed
- Early transition to [Click](https://click.palletsprojects.com/en/stable/)
- Implemented simple print contents functionality 

## [0.0.1] - 2026-08-08

### Added
- Initial project layout using [Typer](https://typer.tiangolo.com/tutorial/)