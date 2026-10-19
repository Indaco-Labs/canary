"""Hardware-independent sensor contract."""

from typing import Protocol

from canary.models import Measurement


class SensorReadError(Exception):
    """A sensor could not provide a measurement."""


class Sensor(Protocol):
    """A sensor that produces one validated measurement per read."""

    @property
    def sensor_id(self) -> str:
        """Unique identifier of the sensor."""
        ...

    def read(self) -> Measurement:
        """Return a measurement or raise SensorReadError."""
        ...
