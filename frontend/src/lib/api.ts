import type {
  BatteryPassport,
  CreatePassportPayload,
  PublicPassport,
} from "./types";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
    ...init,
    headers: {
      "Content-Type": "application/json",
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
