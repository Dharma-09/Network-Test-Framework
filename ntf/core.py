# ntf/core.py
import yaml
import importlib
import pkgutil
import json
from typing import List, Dict
from .device import Device
from pathlib import Path
from rich.console import Console


console = Console()


class NTF:
def __init__(self, inventory_file: str = "inventory.yaml"):
self.inventory_file = inventory_file
self.inventory = self._load_inventory()


def _load_inventory(self) -> Dict:
with open(self.inventory_file) as fh:
return yaml.safe_load(fh)


def list_devices(self) -> List[Dict]:
return self.inventory.get("devices", [])


def _device_from_entry(self, entry: Dict) -> Device:
	return Device(
		host=entry["host"],
		username=entry.get("username"),
		password=entry.get("password"),
		port=entry.get("port", 443),
		transport=entry.get("transport", "https"),
	)


def run_test(self, test_cls, device_entry, params=None) -> Dict:
	device = self._device_from_entry(device_entry)
	test = test_cls(params=params)
	console.log(f"Running {test.name} against {device_entry['name']}")
	try:
		res = test.run(device)
	finally:
		device.close()
	return res


def discover_tests(self) -> Dict[str, object]:
	# dynamic import: load ntf.tests package
	import ntf.tests as tests_pkg
	tests = {}
	for finder, name, ispkg in pkgutil.iter_modules(tests_pkg.__path__):
		mod = importlib.import_module(f"ntf.tests.{name}")
		for attr in dir(mod):
			obj = getattr(mod, attr)
			if isinstance(obj, type) and hasattr(obj, 'run') and hasattr(obj, 'name'):
				tests[obj.name] = obj
	return tests


def run_all(self) -> List[Dict]:
	tests = self.discover_tests()
	results = []
	for device in self.list_devices():
		for test_name, test_cls in tests.items():
			params = {} # extend with test-specific parameter loading
			r = self.run_test(test_cls, device, params)
			r.update({"device": device['name']})
			results.append(r)
	# write report
	Path("reports").mkdir(exist_ok=True)
	with open("reports/report.json", "w") as fh:
		json.dump(results, fh, indent=2)
	return results
return results