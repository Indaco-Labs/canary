"""Tests for the simulated sensor backend."""

from collections.abc import Callable
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from canary.models import SensorConfig
from canary.sensors.base import Sensor, SensorReadError
from canary.sensors.simulated import SimulatedSensor

FIXED_TIME = datetime(2026, 10, 19, 12, 0, tzinfo=UTC)


def make_sensor(
    *,
    temperature_c: float = 22.0,
    humidity_percent: float = 60.0,
    clock: Callable[[], datetime] | None = None,
    fail_reads: bool = False,
) -> SimulatedSensor:
    return SimulatedSensor(
        SensorConfig(sensor_id="sensor-01", gpio_pin=4),
        temperature_c=temperature_c,
        humidity_percent=humidity_percent,
        clock=clock,
        fail_reads=fail_reads,
    )


def test_implements_sensor_protocol() -> None:
    sensor: Sensor = make_sensor()
    assert sensor.sensor_id == "sensor-01"


def test_fixed_reading_is_deterministic() -> None:
    sensor = make_sensor(temperature_c=25.5, humidity_percent=72.0, clock=lambda: FIXED_TIME)
    first = sensor.read()
    assert first == sensor.read()
    assert first.sensor_id == "sensor-01"
    assert first.temperature_c == 25.5
    assert first.humidity_percent == 72.0
    assert first.timestamp == FIXED_TIME


def test_default_reading_is_valid() -> None:
    measurement = make_sensor().read()
    assert measurement.temperature_c == 22.0
    assert measurement.humidity_percent == 60.0
    assert measurement.timestamp.utcoffset() is not None
    assert measurement.timestamp.utcoffset().total_seconds() == 0


def test_controlled_failure() -> None:
    sensor = make_sensor(fail_reads=True)
    with pytest.raises(SensorReadError, match="sensor-01"):
        sensor.read()


@pytest.mark.parametrize("humidity", [-1.0, 101.0, float("nan")])
def test_invalid_simulated_humidity_rejected(humidity: float) -> None:
    with pytest.raises(ValidationError):
        make_sensor(humidity_percent=humidity)


def test_invalid_clock_timestamp_rejected() -> None:
    sensor = make_sensor(clock=lambda: datetime(2026, 10, 19, 12, 0))
    with pytest.raises(ValidationError, match="timezone-aware"):
        sensor.read()
