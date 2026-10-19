"""Application settings loaded from environment variables."""

from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from canary.models import SensorBackend, SensorConfig


def default_sensors() -> tuple[SensorConfig, ...]:
    """Return independent, immutable default sensor definitions."""
    return (
        SensorConfig(sensor_id="sensor-01", gpio_pin=4),
        SensorConfig(sensor_id="sensor-02", gpio_pin=17),
        SensorConfig(sensor_id="sensor-03", gpio_pin=27),
        SensorConfig(sensor_id="sensor-04", gpio_pin=22),
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CANARY_",
        extra="forbid",
        frozen=True,
    )

    app_name: str = Field(default="Canary", min_length=1)
    environment: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    sampling_interval_seconds: int = Field(default=60, ge=1)
    sensor_backend: SensorBackend = SensorBackend.SIMULATED
    sensors: tuple[SensorConfig, ...] = Field(default_factory=default_sensors)

    @model_validator(mode="after")
    def validate_sensors(self) -> "Settings":
        if not self.sensors:
            raise ValueError("at least one sensor must be configured")
        ids = [sensor.sensor_id for sensor in self.sensors]
        pins = [sensor.gpio_pin for sensor in self.sensors]
        if len(ids) != len(set(ids)):
            raise ValueError("sensor IDs must be unique")
        if len(pins) != len(set(pins)):
            raise ValueError("sensor GPIO pins must be unique")
        return self
