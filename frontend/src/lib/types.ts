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
