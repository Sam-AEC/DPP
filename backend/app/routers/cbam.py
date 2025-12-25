"""CBAM scaffold: declarations and line items with simple emissions calc placeholders."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fpdf import FPDF

from .. import models, schemas
from ..auth import get_current_org
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/api/cbam", tags=["cbam"])

DEFAULT_FACTORS = {
    "7208": 2.1,  # flat-rolled iron/steel
    "7207": 2.4,  # semi-finished
    "7210": 1.9,
    "7601": 16.0,  # aluminum
    "2523": 0.8,  # cement
}
settings = get_settings()
CERT_PRICE_PER_TONNE = settings.cbam_certificate_price_per_tonne


def calculate_emissions(item: models.CbamItem) -> float:
    factor = item.verified_emission_factor or item.default_emission_factor or 0.0
    return (item.quantity_tonnes or 0.0) * factor


def render_pdf(decl: models.CbamDeclaration, items: list[models.CbamItem]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"CBAM Declaration {decl.period}", ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Status: {decl.status}", ln=1)
    pdf.cell(0, 8, f"Total emissions: {decl.total_emissions or 0:.2f} tCO2e", ln=1)
    pdf.cell(0, 8, f"Certificate price (€/t): {CERT_PRICE_PER_TONNE:.2f}", ln=1)
    pdf.cell(
        0,
        8,
        f"Certificate cost estimate: {decl.certificate_cost_estimate or 0:.2f} EUR",
        ln=1,
    )
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Line Items", ln=1)
    pdf.set_font("Arial", "", 11)
    for item in items:
        factor_used = item.verified_emission_factor or item.default_emission_factor or 0
        supplier = item.supplier_name or "N/A"
        pdf.multi_cell(
            0,
            6,
            f"CN {item.cn_code} | Qty {item.quantity_tonnes} t | EF {factor_used} | Emissions {item.calculated_emissions or 0} | Supplier {supplier}",
        )
    return pdf.output(dest="S").encode("latin1")


@router.post("/declarations", response_model=schemas.CbamDeclarationRead, status_code=status.HTTP_201_CREATED)
def create_declaration(payload: schemas.CbamDeclarationCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    declaration = models.CbamDeclaration(
        org_id=str(org.id),
        period=payload.period,
        status=payload.status or "draft",
        certificate_price_per_tonne=payload.certificate_price_per_tonne or CERT_PRICE_PER_TONNE,
    )
    db.add(declaration)
    db.flush()

    items: List[models.CbamItem] = []
    for data in payload.items:
        default_factor = data.default_emission_factor
        if default_factor is None:
            prefix = data.cn_code[:4]
            # Lookup org-specific factor first
            factor_entry = (
                db.query(models.CbamFactor)
                .filter(models.CbamFactor.org_id == str(org.id))
                .filter(models.CbamFactor.cn_prefix == prefix)
                .first()
            )
            if factor_entry:
                default_factor = factor_entry.emission_factor
            else:
                default_factor = DEFAULT_FACTORS.get(prefix, 0.0)
        supplier_name = data.supplier_name
        if data.supplier_id:
            supplier = db.get(models.CbamSupplier, data.supplier_id)
            if supplier and supplier.org_id == str(org.id):
                supplier_name = supplier.name
                if default_factor == 0 and supplier.default_emission_factor is not None:
                    default_factor = supplier.default_emission_factor
        item = models.CbamItem(
            declaration_id=declaration.id,
            org_id=str(org.id),
            cn_code=data.cn_code,
            product_description=data.product_description,
            quantity_tonnes=data.quantity_tonnes,
            default_emission_factor=default_factor,
            verified_emission_factor=data.verified_emission_factor,
            supplier_id=data.supplier_id,
            supplier_name=supplier_name,
            country_of_origin=data.country_of_origin,
        )
        item.calculated_emissions = calculate_emissions(item)
        items.append(item)
        db.add(item)

    declaration.total_emissions = sum(i.calculated_emissions or 0.0 for i in items)
    price = declaration.certificate_price_per_tonne or CERT_PRICE_PER_TONNE
    declaration.certificate_cost_estimate = (declaration.total_emissions or 0.0) * price
    db.commit()
    db.refresh(declaration)
    return schemas.CbamDeclarationRead(
        **declaration.__dict__,
        items=[schemas.CbamItemRead.model_validate(item) for item in items],
    )


@router.get("/declarations", response_model=List[schemas.CbamDeclarationRead])
def list_declarations(db: Session = Depends(get_db), org=Depends(get_current_org)):
    declarations = (
        db.query(models.CbamDeclaration)
        .filter(models.CbamDeclaration.org_id == str(org.id))
        .order_by(models.CbamDeclaration.created_at.desc())
        .all()
    )
    results = []
    for decl in declarations:
        items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
        results.append(
            schemas.CbamDeclarationRead(
                **decl.__dict__,
                items=[schemas.CbamItemRead.model_validate(item) for item in items],
            )
        )
    return results


@router.get("/declarations/{declaration_id}", response_model=schemas.CbamDeclarationRead)
def get_declaration(declaration_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    decl = db.get(models.CbamDeclaration, declaration_id)
    if not decl or (decl.org_id and decl.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Declaration not found")
    items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
    return schemas.CbamDeclarationRead(
        **decl.__dict__,
        items=[schemas.CbamItemRead.model_validate(item) for item in items],
    )


@router.post("/declarations/{declaration_id}/status", response_model=schemas.CbamDeclarationRead)
def update_declaration_status(
    declaration_id: UUID,
    payload: schemas.CbamStatusUpdate,
    db: Session = Depends(get_db),
    org=Depends(get_current_org),
):
    decl = db.get(models.CbamDeclaration, declaration_id)
    if not decl or (decl.org_id and decl.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Declaration not found")
    decl.status = payload.status
    db.commit()
    db.refresh(decl)
    items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
    return schemas.CbamDeclarationRead(
        **decl.__dict__,
        items=[schemas.CbamItemRead.model_validate(item) for item in items],
    )


@router.post("/suppliers", response_model=schemas.CbamSupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(payload: schemas.CbamSupplierCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.CbamSupplier(
        org_id=str(org.id),
        **payload.model_dump(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/suppliers", response_model=List[schemas.CbamSupplierRead])
def list_suppliers(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.CbamSupplier)
        .filter(models.CbamSupplier.org_id == str(org.id))
        .order_by(models.CbamSupplier.created_at.desc())
        .all()
    )


@router.post("/factors", response_model=schemas.CbamFactorRead, status_code=status.HTTP_201_CREATED)
def create_factor(payload: schemas.CbamFactorCreate, db: Session = Depends(get_db), org=Depends(get_current_org)):
    record = models.CbamFactor(org_id=str(org.id), **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/factors", response_model=List[schemas.CbamFactorRead])
def list_factors(db: Session = Depends(get_db), org=Depends(get_current_org)):
    return (
        db.query(models.CbamFactor)
        .filter(models.CbamFactor.org_id == str(org.id))
        .order_by(models.CbamFactor.created_at.desc())
        .all()
    )


@router.get("/declarations/{declaration_id}/export/csv")
def export_declaration_csv(declaration_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    decl = db.get(models.CbamDeclaration, declaration_id)
    if not decl or (decl.org_id and decl.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Declaration not found")
    items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
    headers = [
        "cn_code",
        "product_description",
        "quantity_tonnes",
        "default_emission_factor",
        "verified_emission_factor",
        "calculated_emissions",
        "supplier_name",
        "country_of_origin",
        "supplier_name",
        "verified_emission_factor",
        "default_emission_factor",
        "certificate_cost_estimate",
    ]
    lines = [",".join(headers)]
    for item in items:
        row = [
            item.cn_code or "",
            (item.product_description or "").replace(",", " "),
            str(item.quantity_tonnes or ""),
            str(item.default_emission_factor or ""),
            str(item.verified_emission_factor or ""),
            str(item.calculated_emissions or ""),
            (item.supplier_name or "").replace(",", " "),
            (item.country_of_origin or "").replace(",", " "),
            str((item.calculated_emissions or 0) * CERT_PRICE_PER_TONNE),
        ]
        lines.append(",".join(row))
    content = "\n".join(lines)
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="cbam_{declaration_id}.csv"'},
    )


@router.get("/declarations/{declaration_id}/export/pdf")
def export_declaration_pdf(declaration_id: UUID, db: Session = Depends(get_db), org=Depends(get_current_org)):
    decl = db.get(models.CbamDeclaration, declaration_id)
    if not decl or (decl.org_id and decl.org_id != str(org.id)):
        raise HTTPException(status_code=404, detail="Declaration not found")
    items = db.query(models.CbamItem).filter(models.CbamItem.declaration_id == decl.id).all()
    content = render_pdf(decl, items)
    return StreamingResponse(
        iter([content]),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename=\"cbam_{declaration_id}.pdf\"'},
    )
