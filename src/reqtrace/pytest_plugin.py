# pytest_plugin.py

def pytest_configure(config):
    config._reqtrace_tests = []

def pytest_addoption(parser):
    parser.addoption(
        "--reqtrace",
        action="store_true",
        default=False,
        help="Enable reqtrace traceability analysis.",
    )

def pytest_collection_modifyitems(config, items):
	if not config.getoption("--reqtrace"):
		return
      
	for item in items:
		for marker in item.iter_markers("req"):
			print(f"FOUND: {item.nodeid} -> {marker.args}")