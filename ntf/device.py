# ntf/device.py
from __future__ import annotations
import pyeapi
from typing import Any, Dict, Optional


class Device:
	"""Simple wrapper around pyeapi.Connection for Arista EOS devices.

	Provides helper methods to run show/config commands and return parsed JSON.
	"""
	def __init__(self, host: str, username: str, password: str, port: int = 443, transport: str = "https"):
		self.host = host
		self.username = username
		self.password = password
		self.port = port
		self.transport = transport
		self._conn: Optional[pyeapi.client.Node] = None


	def connect(self):
		if self._conn:
			return
		# pyeapi expects a dict connection config
		conn = pyeapi.client.connect(
			transport=self.transport,
			host=self.host,
			username=self.username,
			password=self.password,
			port=self.port,
			return_node=True,
		)
		self._conn = conn


	def close(self):
		if self._conn:
			try:
				self._conn.enable('')
			except Exception:
				pass
		self._conn = None


	def cli(self, commands: list[str]) -> Any:
		"""Run CLI commands and return pyeapi result list"""
		self.connect()
		assert self._conn is not None
		return self._conn.run_commands(commands, format='json')


	def show(self, show_cmd: str) -> Any:
		return self.cli([show_cmd])[0]


	def show_json(self, show_cmd: str) -> Dict:
		out = self.show(show_cmd)
		return out


	# convenience helpers
	def interface_status(self, ifname: str) -> Dict:
		return self.show_json(f"show interfaces {ifname} | json")