"""Validated configuration and acquisition data models."""

from datetime import UTC, datetime, timedelta
from enum import StrEnum
from math import isfinite
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def validate_utc_timestamp(value: datetime) -> datetime:
    """Validate that a timestamp is timezone-aware and uses UTC."""
    offset = value.utcoffset()

    if offset is None:
        raise ValueError("timestamp must be timezone-aware")

    if offset != timedelta(0):
        raise ValueError("timestamp must use UTC")

    return value.astimezone(UTC)

class SensorBackend(StrEnum):
    SIMULATED = "simulated"
    DHT22 = "dht22"


class SensorConfig(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sensor_id: str = Field(min_length=1)
    gpio_pin: int = Field(ge=0, le=27)
    enabled: bool = True


class Measurement(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sensor_id: str = Field(min_length=1)
    temperature_c: float
    humidity_percent: float = Field(ge=0, le=100)
    timestamp: datetime

    @field_validator("temperature_c", "humidity_percent")
    @classmethod
    def finite_number(cls, value: float) -> float:
        if not isfinite(value):
            raise ValueError("measurement values must be finite")
        return value

    @field_validator("timestamp")
    @classmethod
    def utc_timestamp(cls, value: datetime) -> datetime:
        return validate_utc_timestamp(value)


class AcquisitionSuccess(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: Literal["success"] = "success"
    measurement: Measurement


class AcquisitionFailure(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    status: Literal["failure"] = "failure"
    sensor_id: str = Field(min_length=1)
    error: str = Field(min_length=1)
    timestamp: datetime

    @field_validator("timestamp")
    @classmethod
    def utc_timestamp(cls, value: datetime) -> datetime:
        return Measurement.utc_timestamp(value)


AcquisitionResult = Annotated[
    AcquisitionSuccess | AcquisitionFailure,
    Field(discriminator="status"),
]
