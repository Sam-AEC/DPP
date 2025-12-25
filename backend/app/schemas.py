"""Pydantic schemas for request and response bodies."""

from __future__ import annotations

from datetime import date, datetime
from typing import Dict, Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic import field_validator


class OrgCreate(BaseModel):
    name: str


class OrgRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: str
    role: str = "viewer"
    org_id: Optional[UUID] = None


class UserRead(BaseModel):
    id: UUID
    email: str
    role: str
    org_id: Optional[UUID] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApiKeyCreate(BaseModel):
    name: str
    org_id: UUID


class ApiKeyRead(BaseModel):
    id: UUID
    org_id: UUID
    name: str
    key: str
    created_at: datetime
    revoked: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


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
    model_config = ConfigDict(validate_assignment=True)

    @field_validator("battery_weight_kg", "rated_capacity_kwh")
    @classmethod
    def positive_numbers(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Value must be non-negative")
        return value

    @field_validator("carbon_footprint_kg_per_kwh")
    @classmethod
    def cf_reasonable(cls, value: float) -> float:
        if value < 0 or value > 1000:
            raise ValueError("Carbon footprint out of expected range")
        return value


class BatteryPassportFromTemplate(BaseModel):
    template_id: UUID
    serial_number: str
    manufacturing_date: date
    manufacturing_place: str
    battery_status: Optional[str] = "original"
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    battery_model: Optional[str] = None
    gtin: Optional[str] = None
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


class BatteryPassportUpdate(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
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
    template_id: Optional[UUID] = None

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
    template_id: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)


class ComponentBase(BaseModel):
    name: str
    kind: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
    carbon_footprint_ref: Optional[str] = None
    recycled_content: Optional[Dict[str, float]] = None
    hazardous_substances: Optional[str] = None
    test_report_refs: Optional[List[str]] = None


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    kind: Optional[str] = None
    description: Optional[str] = None
    specifications: Optional[Dict[str, str]] = None
    carbon_footprint_ref: Optional[str] = None
    recycled_content: Optional[Dict[str, float]] = None
    hazardous_substances: Optional[str] = None
    test_report_refs: Optional[List[str]] = None


class ComponentRead(ComponentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductTemplateBase(BaseModel):
    name: str
    battery_category: str
    battery_model: Optional[str] = None
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    manufacturing_place: Optional[str] = None
    gtin: Optional[str] = None
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


class ProductTemplateCreate(ProductTemplateBase):
    pass


class ProductTemplateUpdate(BaseModel):
    name: Optional[str] = None
    battery_category: Optional[str] = None
    battery_model: Optional[str] = None
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    manufacturing_place: Optional[str] = None
    gtin: Optional[str] = None
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
    org_id: Optional[str] = None


class ProductTemplateRead(ProductTemplateBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TemplateComponentBase(BaseModel):
    template_id: UUID
    component_id: UUID
    quantity: Optional[float] = None
    notes: Optional[str] = None


class TemplateComponentCreate(TemplateComponentBase):
    pass


class TemplateComponentRead(TemplateComponentBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class RestrictedArtifactBase(BaseModel):
    passport_id: UUID
    kind: str
    title: str
    url: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class RestrictedArtifactCreate(RestrictedArtifactBase):
    pass


class RestrictedArtifactRead(RestrictedArtifactBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogRead(BaseModel):
    id: UUID
    org_id: Optional[str] = None
    actor: Optional[str] = None
    action: str
    entity: str
    entity_id: str
    details: Optional[Dict[str, str]] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CbamSupplierBase(BaseModel):
    name: str
    country: Optional[str] = None
    default_emission_factor: Optional[float] = None
    contact: Optional[str] = None


class CbamSupplierCreate(CbamSupplierBase):
    pass


class CbamSupplierRead(CbamSupplierBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CbamFactorBase(BaseModel):
    cn_prefix: str
    emission_factor: float
    source: Optional[str] = None

    @field_validator("emission_factor")
    @classmethod
    def ef_bounds(cls, value: float) -> float:
        if value < 0 or value > 500:
            raise ValueError("Emission factor out of expected range")
        return value


class CbamFactorCreate(CbamFactorBase):
    pass


class CbamFactorRead(CbamFactorBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CraProductBase(BaseModel):
    name: str
    classification: Optional[str] = None
    sbom_url: Optional[str] = None
    vuln_contact: Optional[str] = None


class CraProductCreate(CraProductBase):
    pass


class CraProductRead(CraProductBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EudrSupplierBase(BaseModel):
    name: str
    country: Optional[str] = None
    geo_coordinates: Optional[str] = None
    risk_score: Optional[float] = None


class EudrSupplierCreate(EudrSupplierBase):
    pass


class EudrSupplierRead(EudrSupplierBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AiSystemBase(BaseModel):
    name: str
    risk_level: Optional[str] = None
    description: Optional[str] = None
    incident_contact: Optional[str] = None


class AiSystemCreate(AiSystemBase):
    pass


class AiSystemRead(AiSystemBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EpdRecordBase(BaseModel):
    product_name: str
    pcr_reference: Optional[str] = None
    lca_document_url: Optional[str] = None


class EpdRecordCreate(EpdRecordBase):
    pass


class EpdRecordRead(EpdRecordBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Nis2AttestationBase(BaseModel):
    supplier_name: str
    status: Optional[str] = None
    evidence_url: Optional[str] = None


class Nis2AttestationCreate(Nis2AttestationBase):
    pass


class Nis2AttestationRead(Nis2AttestationBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ImportJobCreate(BaseModel):
    kind: str
    payload: Optional[Dict[str, str]] = None


class ImportJobRead(BaseModel):
    id: UUID
    org_id: Optional[str] = None
    kind: str
    status: str
    payload: Optional[Dict[str, str]] = None
    result: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExportJobCreate(BaseModel):
    kind: str
    payload: Optional[Dict[str, str]] = None


class ExportJobRead(BaseModel):
    id: UUID
    org_id: Optional[str] = None
    kind: str
    status: str
    payload: Optional[Dict[str, str]] = None
    result: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CbamItemBase(BaseModel):
    cn_code: str
    product_description: Optional[str] = None
    quantity_tonnes: float
    default_emission_factor: Optional[float] = None
    verified_emission_factor: Optional[float] = None
    supplier_id: Optional[UUID] = None
    supplier_name: Optional[str] = None
    country_of_origin: Optional[str] = None

    @field_validator("quantity_tonnes")
    @classmethod
    def non_negative_qty(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Quantity must be non-negative")
        return value

    @field_validator("default_emission_factor", "verified_emission_factor")
    @classmethod
    def ef_bounds(cls, value: Optional[float]) -> Optional[float]:
        if value is None:
            return value
        if value < 0 or value > 500:
            raise ValueError("Emission factor out of expected range")
        return value


class CbamItemCreate(CbamItemBase):
    pass


class CbamItemRead(CbamItemBase):
    id: UUID
    calculated_emissions: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CbamDeclarationCreate(BaseModel):
    period: str
    items: List[CbamItemCreate]


class CbamDeclarationRead(BaseModel):
    id: UUID
    org_id: Optional[str] = None
    period: str
    status: str
    total_emissions: Optional[float] = None
    certificate_cost_estimate: Optional[float] = None
    items: List[CbamItemRead]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
