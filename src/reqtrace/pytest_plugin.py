# pytest_plugin.py
from .core.models import TestTrace


class ReqtracePlugin:
	def __init__(self):
		self.traces: list[TestTrace] = []

	def pytest_collection_modifyitems(self, items):
		for item in items:
			requirement_ids = []

			for marker in item.iter_markers("req"):
				requirement_ids.extend(marker.args)

			if not requirement_ids:
				continue

			trace = TestTrace(
				test_id=item.nodeid,
				req_ids=requirement_ids,
			)

			self.traces.append(trace)


plugin = ReqtracePlugin()


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

	plugin.pytest_collection_modifyitems(items)
