"""ORM models."""

from __future__ import annotations

from datetime import datetime, date
from uuid import uuid4

from sqlalchemy import JSON, Column, Date, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(String(50), nullable=False, default="viewer")  # admin/editor/viewer
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(120), nullable=False)
    key = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked = Column(DateTime, nullable=True)


class Component(Base):
    __tablename__ = "components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    kind = Column(String(80), nullable=True)
    description = Column(String(255), nullable=True)
    specifications = Column(JSON, nullable=True)
    carbon_footprint_ref = Column(String(120), nullable=True)
    recycled_content = Column(JSON, nullable=True)
    hazardous_substances = Column(String(255), nullable=True)
    test_report_refs = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ProductTemplate(Base):
    __tablename__ = "product_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    battery_category = Column(String(50), nullable=False)
    battery_model = Column(String(120), nullable=True)
    manufacturer_name = Column(String(255), nullable=True)
    manufacturer_address = Column(String(255), nullable=True)
    manufacturing_place = Column(String(120), nullable=True)
    gtin = Column(String(50), nullable=True)
    battery_weight_kg = Column(Float, nullable=True)
    carbon_footprint_kg_per_kwh = Column(Float, nullable=True)
    carbon_footprint_class = Column(String(50), nullable=True)
    recycled_content_cobalt = Column(Float, nullable=True)
    recycled_content_lead = Column(Float, nullable=True)
    recycled_content_lithium = Column(Float, nullable=True)
    recycled_content_nickel = Column(Float, nullable=True)
    rated_capacity_kwh = Column(Float, nullable=True)
    expected_lifetime_cycles = Column(Integer, nullable=True)
    expected_lifetime_years = Column(Integer, nullable=True)
    hazardous_substances = Column(String(255), nullable=True)
    performance_class = Column(String(50), nullable=True)
    additional_public_data = Column(JSON, nullable=True)
    restricted_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TemplateComponent(Base):
    __tablename__ = "template_components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("product_templates.id"), nullable=False)
    component_id = Column(UUID(as_uuid=True), ForeignKey("components.id"), nullable=False)
    quantity = Column(Float, nullable=True)
    notes = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class BatteryPassport(Base):
    __tablename__ = "battery_passports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
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
    template_id = Column(UUID(as_uuid=True), ForeignKey("product_templates.id"), nullable=True)
    component_snapshot = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class RestrictedArtifact(Base):
    __tablename__ = "restricted_artifacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    passport_id = Column(UUID(as_uuid=True), ForeignKey("battery_passports.id"), nullable=False)
    kind = Column(String(80), nullable=False)  # conformity, test_report, dismantling, safety
    title = Column(String(255), nullable=False)
    url = Column(String(255), nullable=True)
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    actor = Column(String(120), nullable=True)
    action = Column(String(80), nullable=False)
    entity = Column(String(80), nullable=False)
    entity_id = Column(String(120), nullable=False)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    kind = Column(String(80), nullable=False)  # components/templates/passports/cbam
    status = Column(String(50), nullable=False, default="pending")
    payload = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    kind = Column(String(80), nullable=False)  # passports, cbam, etc.
    status = Column(String(50), nullable=False, default="pending")
    payload = Column(JSON, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CbamDeclaration(Base):
    __tablename__ = "cbam_declarations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True)
    period = Column(String(20), nullable=False)  # e.g., 2025-Q4
    status = Column(String(50), nullable=False, default="draft")
    total_emissions = Column(Float, nullable=True)
    certificate_cost_estimate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class CbamItem(Base):
    __tablename__ = "cbam_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    declaration_id = Column(UUID(as_uuid=True), ForeignKey("cbam_declarations.id"), nullable=False)
    org_id = Column(String(120), nullable=True)
    cn_code = Column(String(20), nullable=False)
    product_description = Column(String(255), nullable=True)
    quantity_tonnes = Column(Float, nullable=False)
    default_emission_factor = Column(Float, nullable=True)
    verified_emission_factor = Column(Float, nullable=True)
    calculated_emissions = Column(Float, nullable=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("cbam_suppliers.id"), nullable=True)
    supplier_name = Column(String(255), nullable=True)
    country_of_origin = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CbamFactor(Base):
    __tablename__ = "cbam_factors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    cn_prefix = Column(String(10), nullable=False)
    emission_factor = Column(Float, nullable=False)
    source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CbamSupplier(Base):
    __tablename__ = "cbam_suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(120), nullable=True)
    default_emission_factor = Column(Float, nullable=True)
    contact = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CraProduct(Base):
    __tablename__ = "cra_products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    classification = Column(String(80), nullable=True)
    sbom_url = Column(String(255), nullable=True)
    vuln_contact = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EudrSupplier(Base):
    __tablename__ = "eudr_suppliers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    country = Column(String(120), nullable=True)
    geo_coordinates = Column(String(255), nullable=True)
    risk_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AiSystem(Base):
    __tablename__ = "ai_systems"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    name = Column(String(255), nullable=False)
    risk_level = Column(String(80), nullable=True)
    description = Column(String(255), nullable=True)
    incident_contact = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EpdRecord(Base):
    __tablename__ = "epd_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    product_name = Column(String(255), nullable=False)
    pcr_reference = Column(String(255), nullable=True)
    lca_document_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Nis2Attestation(Base):
    __tablename__ = "nis2_attestations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(String(120), nullable=True, index=True)
    supplier_name = Column(String(255), nullable=False)
    status = Column(String(80), nullable=True)
    evidence_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
