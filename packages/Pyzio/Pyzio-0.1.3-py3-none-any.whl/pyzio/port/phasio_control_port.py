from abc import ABC, abstractmethod


class PhasioControlPort(ABC):

	@abstractmethod
	def get_file(self, printer_id: str, secret: str, job_id: str, filename: str, cluster_id: str) -> str:
		pass

	@abstractmethod
	def register_candidate(self, job_id: str, filename: str, cluster_id: str) -> (int, str, str):
		pass
