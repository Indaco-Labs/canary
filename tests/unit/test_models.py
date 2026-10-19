"""Tests for measurement and acquisition result models."""

from datetime import UTC, datetime, timedelta, timezone
from math import inf, nan

import pytest
from pydantic import TypeAdapter, ValidationError

from canary.models import (
    AcquisitionFailure,
    AcquisitionResult,
    AcquisitionSuccess,
    Measurement,
    SensorConfig,
)

UTC_NOW = datetime(2026, 10, 19, 12, 0, tzinfo=UTC)


def make_measurement(**overrides: object) -> Measurement:
    data: dict[str, object] = {
        "sensor_id": "sensor-01",
        "temperature_c": 23.5,
        "humidity_percent": 65.0,
        "timestamp": UTC_NOW,
    }
    data.update(overrides)
    return Measurement.model_validate(data)


def test_valid_measurement() -> None:
    measurement = make_measurement()
    assert measurement.temperature_c == 23.5
    assert measurement.humidity_percent == 65.0


@pytest.mark.parametrize("humidity", [-1, 101, nan, inf])
def test_invalid_humidity(humidity: float) -> None:
    with pytest.raises(ValidationError):
        make_measurement(humidity_percent=humidity)


@pytest.mark.parametrize("temperature", [nan, inf, -inf])
def test_nonfinite_temperature(temperature: float) -> None:
    with pytest.raises(ValidationError):
        make_measurement(temperature_c=temperature)


def test_naive_timestamp_rejected() -> None:
    with pytest.raises(ValidationError, match="timezone-aware"):
        make_measurement(timestamp=datetime(2026, 10, 19, 12, 0))


def test_non_utc_timestamp_rejected() -> None:
    with pytest.raises(ValidationError, match="UTC"):
        make_measurement(
            timestamp=datetime(2026, 10, 19, 13, 0, tzinfo=timezone(timedelta(hours=1)))
        )


def test_sensor_config_rejects_invalid_gpio() -> None:
    with pytest.raises(ValidationError):
        SensorConfig(sensor_id="sensor-01", gpio_pin=-1)


def test_acquisition_success() -> None:
    result = AcquisitionSuccess(measurement=make_measurement())
    assert result.status == "success"


def test_acquisition_failure_has_no_measurement() -> None:
    result = AcquisitionFailure(sensor_id="sensor-01", error="read timed out", timestamp=UTC_NOW)
    assert result.status == "failure"
    assert "measurement" not in result.model_dump()


def test_discriminated_result_parsing() -> None:
    adapter = TypeAdapter(AcquisitionResult)
    result = adapter.validate_python({
        "status": "failure",
        "sensor_id": "sensor-01",
        "error": "read timed out",
        "timestamp": UTC_NOW,
    })
    assert isinstance(result, AcquisitionFailure)
