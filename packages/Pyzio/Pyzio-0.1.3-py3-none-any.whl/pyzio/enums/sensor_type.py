from enum import Enum


class SensorType(str, Enum):
	TEMPERATURE = 'TEMPERATURE'
	PRESSURE = 'PRESSURE'
