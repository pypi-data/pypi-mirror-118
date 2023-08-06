from dataclasses import dataclass
from queue import PriorityQueue
from typing import List, Tuple

from ..pyzio_logger import PyzioLogger


@dataclass
class Job:
	sequence_number: int
	job_id: str
	filename: str
	cluster_id: str


class LocalJobRepository:
	def __init__(self, logger: PyzioLogger):
		self._logger = logger
		self._job_q = PriorityQueue()

	def add_job_to_completed_list(self, job_id: str) -> None:
		pass

	def add_job_to_failed_list(self, job_id: str) -> None:
		pass

	def update_jobs(self, jobs: List[Job]) -> None:
		while not self._job_q.empty():
			self._job_q.get()
		for job in jobs:
			entry = job.sequence_number, job.job_id, job.filename, job.cluster_id
			self._job_q.put((job.sequence_number, entry))

	def get_job_from_queue(self) -> Job:
		sequence_number, job_id, filename, cluster_id = self._job_q.get()[1]
		return Job(sequence_number, job_id, filename, cluster_id)

	def is_queue_empty(self):
		return self._job_q.empty()

	def _get_records_from_queue(self) -> List[Tuple[int, str, str, str]]:
		records = []
		while not self._job_q.empty():
			sequence_number, job_id, filename, cluster_id = self._job_q.get()[1]
			records.append((sequence_number, job_id, filename, cluster_id))
		return records

	def _populate_queue(self, records: List[Tuple[int, str, str, str]]) -> None:
		while len(records) > 0:
			entry = records.pop()
			self._job_q.put((entry[0], entry))
