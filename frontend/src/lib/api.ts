import type {
  BatteryPassport,
  CreatePassportPayload,
  PublicPassport,
  Component,
  ProductTemplate,
  ComponentCreate,
  ProductTemplateCreate,
  ImportJob,
  ExportJob,
  CbamDeclaration,
  CbamDeclarationPayload,
  AuditLog,
  CraProduct,
  EudrSupplier,
  AiSystem,
  EpdRecord,
  Nis2Attestation,
} from "./types";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(API_KEY ? { "X-API-Key": API_KEY } : {}),
      ...(init?.headers || {}),
    },
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "API request failed");
  }

  return response.json() as Promise<T>;
}

export async function listPassports(): Promise<BatteryPassport[]> {
  return request<BatteryPassport[]>("/passports");
}

export async function getPassport(id: string): Promise<BatteryPassport> {
  return request<BatteryPassport>(`/passports/${id}`);
}

export async function createPassport(
  payload: CreatePassportPayload,
): Promise<BatteryPassport> {
  return request<BatteryPassport>("/passports", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getPublicPassport(
  id: string,
): Promise<PublicPassport> {
  return request<PublicPassport>(`/passports/${id}/public`);
}

export async function createPassportFromTemplate(body: any): Promise<BatteryPassport> {
  return request<BatteryPassport>("/passports/from-template", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function listComponents(): Promise<Component[]> {
  return request<Component[]>("/catalog/components");
}

export async function listTemplates(): Promise<ProductTemplate[]> {
  return request<ProductTemplate[]>("/catalog/templates");
}

export async function createComponent(body: ComponentCreate): Promise<Component> {
  return request<Component>("/catalog/components", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function createTemplate(body: ProductTemplateCreate): Promise<ProductTemplate> {
  return request<ProductTemplate>("/catalog/templates", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function createImportJob(kind: string, records: any[]): Promise<ImportJob> {
  return request<ImportJob>("/jobs/imports", {
    method: "POST",
    body: JSON.stringify({ kind, payload: { records } }),
  });
}

export async function runImportJob(id: string): Promise<ImportJob> {
  return request<ImportJob>(`/jobs/imports/${id}/run`, { method: "POST" });
}

export async function listImportJobs(): Promise<ImportJob[]> {
  return request<ImportJob[]>("/jobs/imports");
}

export async function createExportJob(kind: string): Promise<ExportJob> {
  return request<ExportJob>("/jobs/exports", {
    method: "POST",
    body: JSON.stringify({ kind }),
  });
}

export async function runExportJob(id: string): Promise<ExportJob> {
  return request<ExportJob>(`/jobs/exports/${id}/run`, { method: "POST" });
}

export async function listExportJobs(): Promise<ExportJob[]> {
  return request<ExportJob[]>("/jobs/exports");
}

export async function createCbamDeclaration(payload: CbamDeclarationPayload): Promise<CbamDeclaration> {
  return request<CbamDeclaration>("/cbam/declarations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function listCbamDeclarations(): Promise<CbamDeclaration[]> {
  return request<CbamDeclaration[]>("/cbam/declarations");
}

export async function createCbamSupplier(body: { name: string; country?: string; default_emission_factor?: number; contact?: string; }): Promise<any> {
  return request("/cbam/suppliers", { method: "POST", body: JSON.stringify(body) });
}

export async function listCbamSuppliers(): Promise<any[]> {
  return request<any[]>("/cbam/suppliers");
}

export async function listAuditLogs(): Promise<AuditLog[]> {
  return request<AuditLog[]>("/audit");
}

export async function createCbamFactor(body: { cn_prefix: string; emission_factor: number; source?: string }): Promise<any> {
  return request("/cbam/factors", { method: "POST", body: JSON.stringify(body) });
}

export async function listCbamFactors(): Promise<any[]> {
  return request<any[]>("/cbam/factors");
}

export async function updateCbamStatus(id: string, status: string): Promise<CbamDeclaration> {
  return request<CbamDeclaration>(`/cbam/declarations/${id}/status`, {
    method: "POST",
    body: JSON.stringify({ status }),
  });
}

export async function listArtifacts(): Promise<any[]> {
  return request<any[]>("/artifacts");
}

export async function updateComponent(id: string, body: Partial<Component>): Promise<Component> {
  return request<Component>(`/catalog/components/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export async function updateTemplate(id: string, body: Partial<ProductTemplate>): Promise<ProductTemplate> {
  return request<ProductTemplate>(`/catalog/templates/${id}`, {
    method: "PATCH",
    body: JSON.stringify(body),
  });
}

export async function createCraProduct(body: Partial<CraProduct>): Promise<CraProduct> {
  return request<CraProduct>("/compliance/cra/products", { method: "POST", body: JSON.stringify(body) });
}

export async function listCraProducts(): Promise<CraProduct[]> {
  return request<CraProduct[]>("/compliance/cra/products");
}

export async function createEudrSupplier(body: Partial<EudrSupplier>): Promise<EudrSupplier> {
  return request<EudrSupplier>("/compliance/eudr/suppliers", { method: "POST", body: JSON.stringify(body) });
}

export async function listEudrSuppliers(): Promise<EudrSupplier[]> {
  return request<EudrSupplier[]>("/compliance/eudr/suppliers");
}

export async function createAiSystem(body: Partial<AiSystem>): Promise<AiSystem> {
  return request<AiSystem>("/compliance/ai/systems", { method: "POST", body: JSON.stringify(body) });
}

export async function listAiSystems(): Promise<AiSystem[]> {
  return request<AiSystem[]>("/compliance/ai/systems");
}

export async function createEpdRecord(body: Partial<EpdRecord>): Promise<EpdRecord> {
  return request<EpdRecord>("/compliance/epd/records", { method: "POST", body: JSON.stringify(body) });
}

export async function listEpdRecords(): Promise<EpdRecord[]> {
  return request<EpdRecord[]>("/compliance/epd/records");
}

export async function createNis2Attestation(body: Partial<Nis2Attestation>): Promise<Nis2Attestation> {
  return request<Nis2Attestation>("/compliance/nis2/attestations", { method: "POST", body: JSON.stringify(body) });
}

export async function listNis2Attestations(): Promise<Nis2Attestation[]> {
  return request<Nis2Attestation[]>("/compliance/nis2/attestations");
}
