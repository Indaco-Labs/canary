"""Tests for application settings."""

import pytest
from pydantic import ValidationError

from canary.config import Settings
from canary.models import SensorBackend, SensorConfig


@pytest.fixture(autouse=True)
def clean_canary_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Prevent host CANARY_ variables from influencing tests."""
    import os

    for name in os.environ:
        if name.startswith("CANARY_"):
            monkeypatch.delenv(name)


def test_default_settings() -> None:
    settings = Settings()
    assert settings.sampling_interval_seconds == 60
    assert settings.sensor_backend is SensorBackend.SIMULATED
    assert [(s.sensor_id, s.gpio_pin) for s in settings.sensors] == [
        ("sensor-01", 4),
        ("sensor-02", 17),
        ("sensor-03", 27),
        ("sensor-04", 22),
    ]


def test_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CANARY_SAMPLING_INTERVAL_SECONDS", "30")
    assert Settings().sampling_interval_seconds == 30


@pytest.mark.parametrize("interval", [0, -1])
def test_invalid_interval(interval: int) -> None:
    with pytest.raises(ValidationError):
        Settings(sampling_interval_seconds=interval)


def test_duplicate_sensor_ids_rejected() -> None:
    with pytest.raises(ValidationError, match="sensor IDs must be unique"):
        Settings(
            sensors=(
                SensorConfig(sensor_id="x", gpio_pin=4),
                SensorConfig(sensor_id="x", gpio_pin=17),
            )
        )


def test_duplicate_gpio_pins_rejected() -> None:
    with pytest.raises(ValidationError, match="GPIO pins must be unique"):
        Settings(
            sensors=(
                SensorConfig(sensor_id="x", gpio_pin=4),
                SensorConfig(sensor_id="y", gpio_pin=4),
            )
        )


def test_json_sensor_environment_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CANARY_SENSORS", '[{"sensor_id":"custom","gpio_pin":5}]')
    assert Settings().sensors == (SensorConfig(sensor_id="custom", gpio_pin=5),)
