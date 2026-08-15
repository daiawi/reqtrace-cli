# pytest_plugin.py
from collections import defaultdict

from .models import TestTrace


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

	def report(self) -> str:
		requirements = defaultdict(list)

		for trace in self.traces:
			for req_id in trace.req_ids:
				requirements[req_id].append(trace.test_id)

		lines = [
			f"Requirements: {len(requirements)}",
			f"Tests: {len(self.traces)}",
			"",
		]

		for req_id in sorted(requirements):
			lines.append(f"Requirement ID: {req_id}")

			for test_id in requirements[req_id]:
				test_name = test_id.split("::")[-1]
				lines.append(f"\t- {test_name}")

			lines.append("")

		return "\n".join(lines)

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
