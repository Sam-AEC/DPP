"""Pydantic schemas for request and response bodies."""

from __future__ import annotations

from datetime import date, datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BatteryPassportBase(BaseModel):
    manufacturer_name: str
    manufacturer_address: str
    battery_model: str
    battery_category: str
    manufacturing_date: date
    manufacturing_place: str
    serial_number: str
    gtin: str
    battery_status: str = "original"
    battery_weight_kg: float
    carbon_footprint_kg_per_kwh: float
    carbon_footprint_class: Optional[str] = None
    recycled_content_cobalt: Optional[float] = None
    recycled_content_lead: Optional[float] = None
    recycled_content_lithium: Optional[float] = None
    recycled_content_nickel: Optional[float] = None
    rated_capacity_kwh: float
    expected_lifetime_cycles: Optional[int] = None
    expected_lifetime_years: Optional[int] = None
    hazardous_substances: Optional[str] = None
    performance_class: Optional[str] = None
    additional_public_data: Optional[Dict[str, str]] = None
    restricted_data: Optional[Dict[str, str]] = None
    end_of_life: Optional[Dict[str, str]] = None


class BatteryPassportCreate(BatteryPassportBase):
    pass


class BatteryPassportUpdate(BaseModel):
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    battery_model: Optional[str] = None
    battery_category: Optional[str] = None
    manufacturing_date: Optional[date] = None
    manufacturing_place: Optional[str] = None
    serial_number: Optional[str] = None
    gtin: Optional[str] = None
    battery_status: Optional[str] = None
    battery_weight_kg: Optional[float] = None
    carbon_footprint_kg_per_kwh: Optional[float] = None
    carbon_footprint_class: Optional[str] = None
    recycled_content_cobalt: Optional[float] = None
    recycled_content_lead: Optional[float] = None
    recycled_content_lithium: Optional[float] = None
    recycled_content_nickel: Optional[float] = None
    rated_capacity_kwh: Optional[float] = None
    expected_lifetime_cycles: Optional[int] = None
    expected_lifetime_years: Optional[int] = None
    hazardous_substances: Optional[str] = None
    performance_class: Optional[str] = None
    additional_public_data: Optional[Dict[str, str]] = None
    restricted_data: Optional[Dict[str, str]] = None
    end_of_life: Optional[Dict[str, str]] = None


class BatteryPassportRead(BatteryPassportBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BatteryPassportPublic(BaseModel):
    id: UUID
    manufacturer_name: str
    battery_model: str
    battery_category: str
    manufacturing_date: date
    manufacturing_place: str
    serial_number: str
    gtin: str
    battery_weight_kg: float
    carbon_footprint_kg_per_kwh: float
    carbon_footprint_class: Optional[str] = None
    recycled_content_cobalt: Optional[float] = None
    recycled_content_lead: Optional[float] = None
    recycled_content_lithium: Optional[float] = None
    recycled_content_nickel: Optional[float] = None
    rated_capacity_kwh: float
    expected_lifetime_cycles: Optional[int] = None
    expected_lifetime_years: Optional[int] = None
    hazardous_substances: Optional[str] = None
    performance_class: Optional[str] = None
    additional_public_data: Optional[Dict[str, str]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
