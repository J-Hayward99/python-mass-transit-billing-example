from typing import Iterable
from pydantic import BaseModel, field_validator
from datetime import datetime


def must_be_positive(value: int, start_from_one=False) -> int:
    if value < (1 if start_from_one else 0):
        raise ValueError("price must be non-negative")
    return value


def convert_pounds_to_pence(value: str | int | float) -> int:
    if isinstance(value, str):
        value = value.replace("£", "").strip()

    return int(float(value) * 100)


def confine_string_to_set(value: str, permitted: Iterable[str]):
    if value not in permitted:
        raise ValueError("Value must be: ", *permitted)
    return value


class JourneyData(BaseModel):
    user_id: int
    station: str
    direction: str
    time: datetime

    @field_validator("zone")
    def validate_zone(cls, value):
        value = must_be_positive(value, start_from_one=True)
        return value

    @field_validator("direction")
    def validate_direction(cls, value):
        value = confine_string_to_set(value, permitted={"IN", "OUT"})
        return value


class StationZones(BaseModel):
    station: str
    zone: int

    @field_validator("zone")
    def validate_zone(cls, value):
        value = must_be_positive(value, start_from_one=True)
        return value


class ZonePrice(BaseModel):
    zone: int
    price: int

    @field_validator("zone")
    def validate_zone(cls, value):
        value = must_be_positive(value, start_from_one=True)
        return value

    @field_validator("price", mode="before")
    def parse_price(cls, value):
        value = convert_pounds_to_pence(value)
        return value

    @field_validator("price")
    def validate_price(cls, value):
        value = must_be_positive(value)
        return value


class TravelCap(BaseModel):
    cap: int

    @field_validator("cap", mode="before")
    def parse_price(cls, value):
        value = convert_pounds_to_pence(value)
        return value

    @field_validator("cap")
    def validate_cap(cls, value):
        value = must_be_positive(value)
        return value


class TravelFee(BaseModel):
    fee: int
    duration: int = 1

    @field_validator("fee", mode="before")
    def parse_price(cls, value):
        value = convert_pounds_to_pence(value)
        return value

    @field_validator("fee")
    def validate_fee(cls, value):
        value = must_be_positive(value)
        return value
