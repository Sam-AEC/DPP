import type {
  BatteryPassport,
  CreatePassportPayload,
  PublicPassport,
  Component,
  ProductTemplate,
  ImportJob,
  ExportJob,
  CbamDeclaration,
  CbamDeclarationPayload,
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
