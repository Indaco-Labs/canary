"""Deterministic, hardware-free sensor implementation."""

from collections.abc import Callable
from datetime import UTC, datetime

from canary.models import Measurement, SensorConfig
from canary.sensors.base import SensorReadError


class SimulatedSensor:
    """Return fixed readings, with optional controlled read failures."""

    def __init__(
        self,
        config: SensorConfig,
        *,
        temperature_c: float = 22.0,
        humidity_percent: float = 60.0,
        clock: Callable[[], datetime] | None = None,
        fail_reads: bool = False,
    ) -> None:
        self._config = config
        self._clock = clock if clock is not None else lambda: datetime.now(UTC)
        self._fail_reads = fail_reads
        # Validate supplied values immediately, not after acquisition starts.
        self._temperature_c = temperature_c
        self._humidity_percent = humidity_percent
        Measurement(
            sensor_id=config.sensor_id,
            temperature_c=temperature_c,
            humidity_percent=humidity_percent,
            timestamp=datetime.now(UTC),
        )

    @property
    def sensor_id(self) -> str:
        return self._config.sensor_id

    def read(self) -> Measurement:
        if self._fail_reads:
            raise SensorReadError(f"Simulated read failure for {self.sensor_id}")
        return Measurement(
            sensor_id=self.sensor_id,
            temperature_c=self._temperature_c,
            humidity_percent=self._humidity_percent,
            timestamp=self._clock(),
        )
