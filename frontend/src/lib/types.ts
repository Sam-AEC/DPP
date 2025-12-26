export type BatteryPassport = {
  id: string;
  manufacturer_name: string;
  manufacturer_address: string;
  battery_model: string;
  battery_category: string;
  manufacturing_date: string;
  manufacturing_place: string;
  serial_number: string;
  gtin: string;
  battery_status: string;
  battery_weight_kg: number;
  carbon_footprint_kg_per_kwh: number;
  carbon_footprint_class?: string;
  recycled_content_cobalt?: number;
  recycled_content_lead?: number;
  recycled_content_lithium?: number;
  recycled_content_nickel?: number;
  rated_capacity_kwh: number;
  expected_lifetime_cycles?: number;
  expected_lifetime_years?: number;
  hazardous_substances?: string;
  performance_class?: string;
  additional_public_data?: Record<string, string>;
  restricted_data?: Record<string, string>;
  end_of_life?: Record<string, string>;
  created_at: string;
  updated_at: string;
};

export type PublicPassport = Omit<
  BatteryPassport,
  "restricted_data" | "end_of_life" | "updated_at"
>;

export type CreatePassportPayload = Omit<
  BatteryPassport,
  "id" | "created_at" | "updated_at"
>;

export type Component = {
  id: string;
  name: string;
  kind?: string;
  description?: string;
  specifications?: Record<string, string>;
  carbon_footprint_ref?: string;
  recycled_content?: Record<string, number>;
  hazardous_substances?: string;
  test_report_refs?: string[];
  created_at: string;
  updated_at: string;
};

export type ProductTemplate = {
  id: string;
  name: string;
  battery_category: string;
  battery_model?: string;
  manufacturer_name?: string;
  manufacturer_address?: string;
  manufacturing_place?: string;
  gtin?: string;
  battery_weight_kg?: number;
  carbon_footprint_kg_per_kwh?: number;
  carbon_footprint_class?: string;
  recycled_content_cobalt?: number;
  recycled_content_lead?: number;
  recycled_content_lithium?: number;
  recycled_content_nickel?: number;
  rated_capacity_kwh?: number;
  expected_lifetime_cycles?: number;
  expected_lifetime_years?: number;
  hazardous_substances?: string;
  performance_class?: string;
  additional_public_data?: Record<string, string>;
  restricted_data?: Record<string, string>;
  created_at: string;
  updated_at: string;
};

export type ImportJob = {
  id: string;
  org_id?: string;
  kind: string;
  status: string;
  payload?: Record<string, any>;
  result?: Record<string, any>;
  error?: string;
  created_at: string;
  updated_at: string;
};

export type ExportJob = {
  id: string;
  org_id?: string;
  kind: string;
  status: string;
  payload?: Record<string, any>;
  result?: Record<string, any>;
  error?: string;
  created_at: string;
  updated_at: string;
};

export type CbamItemPayload = {
  cn_code: string;
  product_description?: string;
  quantity_tonnes: number;
  default_emission_factor?: number;
  verified_emission_factor?: number;
  supplier_id?: string;
  supplier_name?: string;
  country_of_origin?: string;
};

export type CbamDeclarationPayload = {
  period: string;
  items: CbamItemPayload[];
};

export type ComponentCreate = Omit<Component, "id" | "created_at" | "updated_at">;
export type ProductTemplateCreate = Omit<ProductTemplate, "id" | "created_at" | "updated_at">;
export type CbamDeclaration = {
  id: string;
  org_id?: string;
  period: string;
  status: string;
  total_emissions?: number;
  certificate_cost_estimate?: number;
  certificate_price_per_tonne?: number;
  items: (CbamItemPayload & { id: string; calculated_emissions?: number; created_at: string })[];
  created_at: string;
  updated_at: string;
};

export type AuditLog = {
  id: string;
  org_id?: string;
  actor?: string;
  action: string;
  entity: string;
  entity_id: string;
  details?: Record<string, any>;
  created_at: string;
};

export type CraProduct = {
  id: string;
  name: string;
  classification?: string;
  sbom_url?: string;
  vuln_contact?: string;
  created_at: string;
};

export type EudrSupplier = {
  id: string;
  name: string;
  country?: string;
  geo_coordinates?: string;
  risk_score?: number;
  created_at: string;
};

export type AiSystem = {
  id: string;
  name: string;
  risk_level?: string;
  description?: string;
  incident_contact?: string;
  created_at: string;
};

export type AiIncident = {
  id: string;
  system_id: string;
  summary: string;
  severity?: string;
  created_at: string;
};

export type EpdRecord = {
  id: string;
  product_name: string;
  pcr_reference?: string;
  lca_document_url?: string;
  created_at: string;
};

export type Nis2Attestation = {
  id: string;
  supplier_name: string;
  status?: string;
  evidence_url?: string;
  created_at: string;
};
