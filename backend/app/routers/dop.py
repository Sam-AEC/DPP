"""Declaration of Performance (DoP) export from templates."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fpdf import FPDF

from .. import models
from ..auth import get_current_org
from ..database import get_db

router = APIRouter(prefix="/api/dop", tags=["dop"])


def render_dop(template: models.ProductTemplate) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Declaration of Performance", ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Product: {template.battery_model or template.name}", ln=1)
    pdf.cell(0, 8, f"Manufacturer: {template.manufacturer_name or 'N/A'}", ln=1)
    pdf.cell(0, 8, f"Address: {template.manufacturer_address or 'N/A'}", ln=1)
    pdf.cell(0, 8, f"Category: {template.battery_category}", ln=1)
    pdf.cell(0, 8, f"GTIN: {template.gtin or 'N/A'}", ln=1)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Performance Characteristics", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"Rated capacity (kWh): {template.rated_capacity_kwh or 'N/A'}", ln=1)
    pdf.cell(0, 6, f"Weight (kg): {template.battery_weight_kg or 'N/A'}", ln=1)
    pdf.cell(0, 6, f"Carbon footprint class: {template.carbon_footprint_class or 'N/A'}", ln=1)
    pdf.cell(0, 6, f"Hazardous substances: {template.hazardous_substances or 'N/A'}", ln=1)
    return pdf.output(dest="S").encode("latin1")


@router.get("/templates/{template_id}/pdf")
def export_dop_pdf(template_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    template = db.get(models.ProductTemplate, template_id)
    if not template or (template.org_id and template.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Template not found")
    content = render_dop(template)
    return StreamingResponse(
        iter([content]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="dop_{template_id}.pdf"'},
    )
