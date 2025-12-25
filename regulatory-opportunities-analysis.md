# Regulatory Opportunities and Build Plan (CBAM + DPP + CRA + EUDR + AI Act + EPD + NIS2)

Prepared for: Sam A. Mohammad  
Date: December 2025

## 0) Platform Thesis
Build a modular compliance suite (“ComplianceHub EU”) with shared identity, catalog/templates, reporting, QR/export, and audit rails. Lead with CBAM (urgency now), follow with Battery DPP (Feb 2027), then CRA, EUDR, AI Act, and EPD. Leverage your construction/BIM background and SME focus with self-serve pricing and white-glove onboarding.

## 1) Regulatory Landscape (Deadlines)
- CBAM: January 1, 2026 (financial obligations start; transitional reporting already live).
- CRA: Sept 11, 2026 (reporting) + Dec 11, 2027 (full compliance).
- DPP (Battery): Feb 18, 2027 (Annex XIII public tier + access tiers).
- ESPR delegated acts: Iron/steel (~2027), textiles (~2028+), electronics pending.
- EUDR: Dec 30, 2026 (large) / June 30, 2027 (SMEs).
- AI Act: Aug 2, 2026 (high-risk systems).
- EPD (EN 15804+A2): Ongoing, rising for tenders (construction).
- NIS2: In force; ongoing supplier-security requirements.

## 2) Personas
- Importer/Distributor (steel, aluminum, cement, fertilizers, batteries): needs CBAM and later DPP/EPD.
- Assembler/Brand (batteries/IoT): needs DPP/CRA.
- Installer/Service partner (storage/industrial batteries): needs DPP public QR and restricted ops view.
- Compliance lead/consultant: orchestrates data accuracy, documents, and audits.

## 3) Modules (What to Build)
- CBAM: CN code classifier, emissions calculator (default vs verified), supplier portal, quarterly/annual report generator, certificate cost forecaster, customs/export integration.
- Battery DPP: Catalog + templates; template-driven passports; QR public scan; restricted operator view; restricted artifacts (conformity, test, dismantling/safety); JSON-LD/PDF exports.
- CRA: Product classification, SBOM ingestion/generation, vulnerability intake + 24h/72h/14-day flows, technical docs, CE prep.
- EUDR: Geolocation collection, risk scoring, Due Diligence Statement (DDS) generator, supplier portal.
- AI Act: System classification, risk assessment, documentation package, incident reporting.
- EPD: PCR templates, LCA data capture, EN 15804+A2 export, BIM/IFC hooks.
- NIS2 (light): Supplier security attestation and evidence collection for SMEs.

## 4) Shared Architecture
- Identity/orgs/roles; RLS by org_id.
- Catalog (components), product templates, template_components.
- Artifacts store (restricted docs), audit logs, API keys/webhooks.
- Import/export engine (CSV/Excel/JSON-LD/PDF).
- Public vs restricted delivery: QR/public pages; operator/admin views.
- EU data residency; retention life + 10y (for DPP); backups and logging.

## 5) Pricing (SME-first with volume options)
- Starter: EUR 99–199/mo (UI, QR/public pages, limited records).
- Growth: EUR 299–499/mo (bulk import, API, templates/catalog, priority support).
- Per-record: EUR 5–15 per passport/declaration for low volume.
- Services: Catalog/GTIN setup, QR print/engraving, ERP/customs integrations.
- CBAM-specific: EUR 199–1,499/mo tiers plus per-declaration EUR 50–100.

## 6) Go-to-Market
- Channels: GS1 (Digital Link/GTIN), customs brokers (CBAM), PROs (Stichting OPEN), industry orgs (Metaalunie/FME/Holland Solar/SBFN), accountants/compliance consultants.
- Offers: “50 CBAM declarations + setup in 2 weeks” and “50 battery passports + QR labels in 2 weeks.”
- Content: “CBAM crash guide,” “Battery DPP in 14 months,” “GS1 Digital Link checklist.”

## 7) Risks & Mitigations
- Requirement changes: keep schemas flexible with JSONB; monitor CIRPASS/JTC24/CBAM annex updates.
- Data quality: validation ranges, audit logs, supplier portals with defaults vs verified values.
- Access control: RLS + org roles before onboarding real customers.
- Persistence: 10+ year retention for DPP; backups and DR documented.
- Competition: move fast on CBAM/DPP SME tiers; partner-driven distribution.

## 8) Delivery Roadmap (Phased Build)
### Phase 1 (CBAM-now: 4–6 weeks)
- Implement CBAM module: CN classifier, emissions calculator (default factors), quarterly/annual report generator, supplier data intake, PDF/CSV exports.
- API keys + webhooks; audit logs; basic org/roles/RLS.
- Ship a pilot bundle for Dutch steel/aluminum importers with customs broker partners.

### Phase 2 (Battery DPP: 4–6 weeks, overlaps)
- Finish template-driven passport flow (already scaffolded): templates/components CRUD, create-from-template endpoint, component snapshots.
- Restricted artifacts endpoints (docs) + auth gating; QR bulk labels; JSON-LD/PDF exports.
- UI: template picker, catalog manager, restricted panel, audit viewer, bulk import wizard.

### Phase 3 (CRA/EUDR foundations: 6–8 weeks)
- Add product classification + SBOM ingestion, vuln intake workflows (CRA).
- Add geolocation capture, risk scoring, DDS export (EUDR).
- Shared supplier portal and evidence storage.

### Phase 4 (AI Act / EPD / NIS2-lite: 8–12 weeks)
- AI system classification + documentation pack + incident logging.
- EPD PCR templates + EN 15804 exports; BIM/IFC hooks.
- NIS2-lite supplier security attestations.

### Continuous
- Validation, monitoring, backups, retention policies.
- Marketing site + pricing + onboarding playbooks per module.

## 9) Immediate Dev Tasks (Codebase you have)
- Fix merge state (done by creating this clean doc).
- Backend: keep extending org/roles/RLS, import/export engine, API keys/webhooks.
- Frontend: template-aware forms, catalog manager, bulk import UI, restricted artifacts upload/UI, audit log viewer, export triggers.
- Add CBAM module scaffold next (new services + endpoints + UI).

## 10) Usage for AI Agents
- Product agents: derive PRDs per module from this doc.
- Content agents: generate site copy, pricing pages, checklists, webinars using deadlines/pricing here.
- Eng agents: extend current FastAPI/Next.js stack with modules, auth/RLS, import/export, and public/restricted delivery.
