"""ORM models."""

from __future__ import annotations

from datetime import datetime, date
from uuid import uuid4

from sqlalchemy import JSON, Column, Date, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class BatteryPassport(Base):
    __tablename__ = "battery_passports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    manufacturer_name = Column(String(255), nullable=False)
    manufacturer_address = Column(String(255), nullable=False)
    battery_model = Column(String(120), nullable=False)
    battery_category = Column(String(50), nullable=False)
    manufacturing_date = Column(Date, nullable=False)
    manufacturing_place = Column(String(120), nullable=False)
    serial_number = Column(String(120), nullable=False, unique=True)
    gtin = Column(String(50), nullable=False)
    battery_status = Column(String(50), default="original", nullable=False)
    battery_weight_kg = Column(Float, nullable=False)
    carbon_footprint_kg_per_kwh = Column(Float, nullable=False)
    carbon_footprint_class = Column(String(50), nullable=True)
    recycled_content_cobalt = Column(Float, nullable=True)
    recycled_content_lead = Column(Float, nullable=True)
    recycled_content_lithium = Column(Float, nullable=True)
    recycled_content_nickel = Column(Float, nullable=True)
    rated_capacity_kwh = Column(Float, nullable=False)
    expected_lifetime_cycles = Column(Integer, nullable=True)
    expected_lifetime_years = Column(Integer, nullable=True)
    hazardous_substances = Column(String(255), nullable=True)
    performance_class = Column(String(50), nullable=True)
    additional_public_data = Column(JSON, nullable=True)
    restricted_data = Column(JSON, nullable=True)
    end_of_life = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
