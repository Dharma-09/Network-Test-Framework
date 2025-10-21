# ntf/tests/base.py
from typing import Any, Dict


class TestCase:
	"""Base class for all tests.

	Subclass and implement `run(self, device)` to perform checks and return a dict result.
	"""
	name = "base"
	description = "Base test"

	def __init__(self, params: Dict | None = None):
		self.params = params or {}

	def run(self, device) -> Dict[str, Any]:
		raise NotImplementedError("Test must implement run(device)")

	def ok(self, success: bool, details: Dict | str = "") -> Dict:
		return {
			"name": self.name,
			"success": bool(success),
			"details": details,
		}