# Regulatory and Market Opportunities: Battery DPP + DoP Platform

This document is a context pack for AI agents to build product, content, and GTM assets for a SaaS that combines Digital Product Passports (DPP) for batteries with a Declaration of Performance (DoP)-style catalog/template workflow. Focus: SME importers/assemblers who need QR-linked passports and prefer prefilled templates from a component library.

## 1) Regulatory landscape (2024-2027)
- Battery Regulation (EU 2023/1542): Battery passport mandatory from **18 Feb 2027** for LMT, industrial >2 kWh, EV batteries (Article 77, Annex XIII). QR must be ISO/IEC 18004:2015 and link to the passport.
- ESPR (EU 2024/1781): Framework for DPP across product groups; delegated acts will define specifics for other categories (iron/steel 2027+, textiles 2028+). Batteries already covered via Battery Regulation.
- Access tiers (Annex XIII): Public; Authorized operators; Authorities; Legitimate interest. Our MVP covers public; restricted buckets prepared for the others.
- Data retention: Lifetime of product + **10 years after end-of-life**.
- Identifiers: Unique ID must comply with ISO/IEC 15459. GS1 Digital Link (GTIN + serial) is the practical choice for QR payload.
- DoP (Declaration of Performance, CPR context): Static performance declaration for construction products, no QR/access tiers. Here we borrow the *catalog + template* workflow but deliver DPP outputs.

## 2) Who we serve (personas)
- Importer/Distributor (SME): Brings batteries into EU/UK, lacks PLM. Needs quick QR-ready passports and bulk processing.
- Assembler/Brand (SME): Builds packs from cells/modules; wants component library to avoid retyping specs and footprints.
- Installer/Service partner: Deploys storage/industrial batteries; needs printed/engraved QR and easy public scans.
- Compliance lead/consultant: Manages data accuracy, uploads conformity docs/test reports, oversees audits.

## 3) Product concept
- Catalog and Templates (DoP-like workflow):
  - **Components**: Cells/modules/materials with attributes (capacity, weight, recycled content, hazardous substances, carbon footprint references, test report IDs).
  - **Product templates**: Battery models referencing components; default public fields (category, weight, capacity, recycled content, CF class, hazards).
  - **Passport creation**: User picks a template, then adds unit/lot specifics (serial, GTIN, manufacturing date/place, status, deviations). QR is generated and points to `/scan/{id}`.
- Data tiers:
  - Public: Annex XIII public fields + additional_public_data notes.
  - Restricted: Conformity docs, test reports, dismantling/safety, end-of-life instructions.
- Delivery:
  - QR PNG (ISO/IEC 18004:2015) following GS1 Digital Link URL shape.
  - Public scan page (no auth) + operator view (auth) with restricted info.
  - API + bulk import (CSV/Excel) to create passports and load catalogs/templates.

## 4) Core compliance checklist (batteries, Annex XIII public tier)
- Manufacturer identification: name, address, trade name, trademark.
- Battery model identifier.
- Manufacturing date (month/year) and place (country/city).
- Category: LMT / industrial >2 kWh / EV.
- Weight (kg).
- Status: original / repurposed / remanufactured / waste.
- Carbon footprint declaration (kg CO2e per kWh) + performance class.
- Recycled content (%): cobalt, lead, lithium, nickel.
- Rated capacity (kWh).
- Expected lifetime (cycles and/or calendar years).
- Hazardous substances present.
- Separate collection symbol mention.
- Data retention: life + 10 years after end-of-life.
- Access control: only public tier exposed on QR page; restricted tier gated.

## 5) Tech blueprint (built already, extendable)
- Frontend: Next.js (public scan, registry, detail, form) with Tailwind 4 styles. Env: `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_SCAN_BASE`.
- Backend: FastAPI + SQLAlchemy, QR via Segno, Pydantic schemas, PostgreSQL (JSONB buckets for flexible fields). Env: `DATABASE_URL`, `BASE_PUBLIC_URL`, `CORS_ORIGINS`.
- Docker Compose: Postgres + API + UI for local runs.
- Needed extensions for catalog/templates:
  - Tables: `components`, `product_templates`, `template_components`, `api_keys` (for ERP), `audit_logs`.
  - RLS/tenant scoping and auth (Clerk or Supabase Auth) to gate restricted_data and uploads.
  - Export: JSON-LD + PDF; webhooks for downstream systems.

## 6) Business model and packaging
- Plans:
  - Starter (EUR 99–199/mo): UI, QR, public pages, limited passports, manual import.
  - Growth (EUR 299–499/mo): Bulk import, API access, template/catalog management, priority support.
  - Per-passport (EUR 5–15): Low-volume option.
  - Services add-ons: Catalog setup, GTIN/Digital Link setup, QR print/engraving coordination, ERP connector setup.
- Channels:
  - GS1 (GTIN guidance, Digital Link credibility).
  - Producer Responsibility Orgs (e.g., Stichting OPEN) and industry groups (Holland Solar/SBFN) for reach.
  - Compliance/accountant partners who handle paperwork for SMEs.
  - Content/webinars: “Battery passport in 14 months” guide; “GS1 Digital Link + QR checklist.”

## 7) Go-to-market motions
- Pilot bundle: “50 passports + QR labels in 2 weeks” with white-glove import of catalog/templates.
- Proof points to capture: time-to-first-passport, error rate, QR scan reliability, audit readiness (public vs restricted).
- Onboarding steps:
  1) Intake catalog (components, templates), GTINs/serial rules, test report references.
  2) Bulk import into platform; generate first batch of passports.
  3) Print/engrave QR; validate public page shows correct Annex XIII fields.
  4) Upload restricted docs; verify operator view and access controls.
  5) Move to steady-state with API/bulk updates and audit logs.

## 8) Risks and mitigations
- Delegated acts evolve: Keep schema flexible with JSON buckets; monitor CIRPASS/JTC 24 updates.
- Data quality: Add validation ranges (weight, CO2e, recycled content) and audit logs.
- Auth/compliance: Implement org/roles + RLS before onboarding; isolate restricted_data.
- Persistence: Ensure 10+ year retention policy and backups; document data residency (EU).
- Competition: Enterprise tools may launch SME tiers; defensibility via speed, GS1/industry partnerships, and SME-friendly pricing.

## 9) Workback plan (next builds)
- Week 1-2: Add catalog + templates models/API; UI prefill; CSV import for templates.
- Week 3: Auth/roles + orgs; restrict restricted_data; audit logging.
- Week 4: Exports (JSON-LD, PDF) + API keys/webhooks; QR label/engraving guide.
- Week 5: Pilot onboarding playbook; launch 3–5 pilots with channel partners.

## 10) How to use this context
- For AI product agents: Generate schemas for components/templates, import mappers, and UI flows for template selection + prefill.
- For AI content agents: Produce landing pages, pricing pages, checklists, and webinar scripts using the regulatory dates and tiered messaging above.
- For AI eng agents: Extend current codebase to add auth, catalog/templates, bulk import, and export formats while preserving QR/public/restricted split.
