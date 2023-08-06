from abc import ABC, abstractmethod

from ..enums.job_status import JobStatus
from ..enums.message_type import MessageType
from ..port.phasio_mqtt_port import PhasioMQTTPort
from ..pyzio_listener import PyzioListener
from ..pyzio_logger import PyzioLogger
from ..repository.local_job_repository import Job
from ..service.job_service import JobService
from ..service.printer_service import PrinterService


class MessageHandler(ABC):
	def __init__(self,
				 logger: PyzioLogger,
				 job_service: JobService,
				 printer_service: PrinterService,
				 phasio_port: PhasioMQTTPort,
				 listener: PyzioListener):
		self._job_service = job_service
		self._logger = logger
		self._printer_service = printer_service
		self._phasio_port = phasio_port
		self._listener = listener

	@abstractmethod
	def handle(self, payload: dict) -> None:
		pass

	@abstractmethod
	def can_handle(self) -> MessageType:
		pass


class JobUpdateMessageHandler(MessageHandler):
	def handle(self, payload: dict) -> None:
		jobs = payload['jobs']
		self._logger.info("Received " + str(len(jobs)) + " jobs from server")
		result = []
		for job in jobs:
			if job['jobStatus'] == JobStatus.WAITING:
				job_id = str(job['jobId'])
				cluster_id = str(job['clusterId'])
				new_job = Job(job['sequenceNumber'], job_id, job['filename'], cluster_id)
				result.append(new_job)
		self._job_service.queue_jobs(result)
		self._listener.on_job_received()

	def can_handle(self) -> MessageType:
		return MessageType.JOB_UPDATE_MESSAGE


class PrinterRegistrationMessageHandler(MessageHandler):
	def handle(self, payload: dict) -> None:
		self._logger.info("Printer registered by server with ID " + str(payload['printerId']))
		printer_id = payload['printerId']
		candidate_id = payload['pairingCandidateId']
		if self._printer_is_not_paired() and str(candidate_id) == self._printer_service.get_candidate_id():
			self._printer_service.set_printer_id(printer_id)
			self._phasio_port.finish_registration(printer_id)
			self._listener.on_printer_registered(printer_id)

	def can_handle(self) -> MessageType:
		return MessageType.PRINTER_REGISTRATION_MESSAGE

	def _printer_is_not_paired(self):
		return self._printer_service.get_printer_id() is None


class SensorRegistrationMessageHandler(MessageHandler):
	def handle(self, payload: dict) -> None:
		self._logger.info('Received sensor ack')
		sensor_id = payload['sensorId']
		request_id = payload['requestId']
		self._listener.on_sensor_registered(sensor_id, request_id)

	def can_handle(self) -> MessageType:
		return MessageType.SENSOR_REGISTRATION_MESSAGE


class PrinterActivityStatusUpdateHandler(MessageHandler):
	def handle(self, payload: dict) -> None:
		self._logger.info("Received activity status update to " + str(payload['activityState']) + " from server")
		self._listener.on_markready_received()

	def can_handle(self) -> MessageType:
		return MessageType.ACTIVITY_STATUS_UPDATE_MESSAGE
