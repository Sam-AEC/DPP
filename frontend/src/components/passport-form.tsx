/* eslint-disable react/no-unescaped-entities */
"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { createPassport, createPassportFromTemplate } from "@/lib/api";
import type { CreatePassportPayload, ProductTemplate } from "@/lib/types";

const initialForm: CreatePassportPayload = {
  manufacturer_name: "",
  manufacturer_address: "",
  battery_model: "",
  battery_category: "industrial",
  manufacturing_date: new Date().toISOString().slice(0, 10),
  manufacturing_place: "",
  serial_number: "",
  gtin: "",
  battery_status: "original",
  battery_weight_kg: 0,
  carbon_footprint_kg_per_kwh: 0,
  rated_capacity_kwh: 0,
  carbon_footprint_class: "",
  expected_lifetime_cycles: 800,
  expected_lifetime_years: 8,
  hazardous_substances: "",
  performance_class: "",
};

type Field = {
  name: keyof CreatePassportPayload;
  label: string;
  type?: "text" | "number" | "date" | "select";
  helper?: string;
  required?: boolean;
  options?: { value: string; label: string }[];
};

const fields: Field[] = [
  { name: "manufacturer_name", label: "Manufacturer name", required: true },
  {
    name: "manufacturer_address",
    label: "Manufacturer address",
    required: true,
  },
  { name: "battery_model", label: "Battery model", required: true },
  {
    name: "battery_category",
    label: "Category",
    type: "select",
    required: true,
    options: [
      { value: "lmt", label: "Light means of transport (LMT)" },
      { value: "industrial", label: "Industrial >2kWh" },
      { value: "ev", label: "Electric vehicle" },
    ],
  },
  {
    name: "manufacturing_date",
    label: "Manufacturing date",
    type: "date",
    required: true,
  },
  {
    name: "manufacturing_place",
    label: "Manufacturing place (country/city)",
    required: true,
  },
  {
    name: "serial_number",
    label: "Serial number",
    helper: "Must be unique; pairs with GTIN for the QR link.",
    required: true,
  },
  {
    name: "gtin",
    label: "GTIN",
    helper: "GS1 Digital Link recommended for QR payload.",
    required: true,
  },
  {
    name: "battery_weight_kg",
    label: "Weight (kg)",
    type: "number",
    required: true,
  },
  {
    name: "rated_capacity_kwh",
    label: "Rated capacity (kWh)",
    type: "number",
    required: true,
  },
  {
    name: "carbon_footprint_kg_per_kwh",
    label: "Carbon footprint (kg CO2e/kWh)",
    type: "number",
    required: true,
  },
  {
    name: "carbon_footprint_class",
    label: "Carbon footprint class",
    helper: "A-E classification per Annex XIII.",
  },
  {
    name: "expected_lifetime_cycles",
    label: "Expected lifetime (cycles)",
    type: "number",
  },
  {
    name: "expected_lifetime_years",
    label: "Expected lifetime (years)",
    type: "number",
  },
  {
    name: "hazardous_substances",
    label: "Hazardous substances present",
    helper: "List key substances requiring disclosure.",
  },
  {
    name: "performance_class",
    label: "Performance class",
    helper: "Optional manufacturer performance tier.",
  },
];

type Props = {
  templates?: ProductTemplate[];
  initialTemplateId?: string;
};

export function PassportForm({ templates = [], initialTemplateId = "" }: Props) {
  const [templateId, setTemplateId] = useState<string>(initialTemplateId);
  const router = useRouter();
  const [form, setForm] = useState<CreatePassportPayload>(initialForm);
  const [publicNote, setPublicNote] = useState("");
  const [restrictedNote, setRestrictedNote] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleChange = (
    name: keyof CreatePassportPayload,
    value: string,
    type?: Field["type"],
  ) => {
    if (type === "number") {
      setForm((prev) => ({
        ...prev,
        [name]: value === "" ? undefined : Number(value),
      }));
      return;
    }

    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      const payload = {
        ...form,
        additional_public_data: publicNote ? { note: publicNote } : undefined,
        restricted_data: restrictedNote ? { note: restrictedNote } : undefined,
      };
      const created = templateId
        ? await createPassportFromTemplate({
            template_id: templateId,
            serial_number: form.serial_number,
            manufacturing_date: form.manufacturing_date as unknown as string,
            manufacturing_place: form.manufacturing_place,
            battery_status: form.battery_status,
            additional_public_data: payload.additional_public_data,
            restricted_data: payload.restricted_data,
            gtin: form.gtin,
            battery_weight_kg: form.battery_weight_kg,
            carbon_footprint_kg_per_kwh: form.carbon_footprint_kg_per_kwh,
            rated_capacity_kwh: form.rated_capacity_kwh,
            expected_lifetime_cycles: form.expected_lifetime_cycles,
            expected_lifetime_years: form.expected_lifetime_years,
            carbon_footprint_class: form.carbon_footprint_class,
            hazardous_substances: form.hazardous_substances,
            performance_class: form.performance_class,
            recycled_content_cobalt: form.recycled_content_cobalt,
            recycled_content_lead: form.recycled_content_lead,
            recycled_content_lithium: form.recycled_content_lithium,
            recycled_content_nickel: form.recycled_content_nickel,
          })
        : await createPassport(payload);
      setSuccess("Passport created and QR code ready.");
      router.push(`/passports/${created.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save passport.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form
      onSubmit={onSubmit}
      className="mt-4 grid grid-cols-1 gap-6 rounded-2xl bg-slate-900/60 p-6 backdrop-blur"
    >
      <div className="grid gap-2 rounded-xl border border-white/10 bg-black/20 p-4">
        <p className="text-sm uppercase tracking-[0.18em] text-slate-300">
          Compliance essentials
        </p>
        <p className="text-sm text-slate-300">
          Covers all Annex XIII public fields. Add restricted data later via
          API or admin.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
        {fields.map((field) => (
          <label key={field.name} className="flex flex-col gap-2 text-sm">
            <div className="flex items-center justify-between gap-2">
              <span className="font-medium text-slate-100">{field.label}</span>
              {field.required ? (
                <span className="text-[10px] uppercase tracking-[0.14em] text-emerald-300">
                  Required
                </span>
              ) : null}
            </div>
            {field.type === "select" ? (
              <select
                required={field.required}
                value={form[field.name] as string}
                onChange={(event) =>
                  handleChange(field.name, event.target.value, field.type)
                }
                className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
              >
                {field.options?.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            ) : (
              <input
                required={field.required}
                type={field.type || "text"}
                value={
                  field.type === "number"
                    ? (form[field.name] as number | undefined) ?? ""
                    : (form[field.name] as string)
                }
                onChange={(event) =>
                  handleChange(field.name, event.target.value, field.type)
                }
                className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
              />
            )}
            {field.helper ? (
              <span className="text-xs text-slate-400">{field.helper}</span>
            ) : null}
          </label>
        ))}
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <label className="flex flex-col gap-2 text-sm">
          <span className="font-medium text-slate-100">Template (optional)</span>
          <select
            value={templateId}
            onChange={(event) => setTemplateId(event.target.value)}
            className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          >
            <option value="">No template</option>
            {templates.map((t) => (
              <option key={t.id} value={t.id}>
                {t.name} ({t.battery_model || t.battery_category})
              </option>
            ))}
          </select>
          <span className="text-xs text-slate-400">
            Prefills Annex XIII fields if selected.
          </span>
        </label>
        <label className="flex flex-col gap-2 text-sm">
          <span className="font-medium text-slate-100">Additional notes</span>
          <textarea
            rows={3}
            placeholder="Restricted info, dismantling instructions, or safety notes."
            value={restrictedNote}
            onChange={(event) => setRestrictedNote(event.target.value)}
            className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
          <span className="text-xs text-slate-400">
            Stored in restricted_data; not shown on public QR page.
          </span>
        </label>
        <label className="flex flex-col gap-2 text-sm">
          <span className="font-medium text-slate-100">Public extras</span>
          <textarea
            rows={3}
            placeholder="Consumer-facing notes (e.g., recycling drop-off points)."
            value={publicNote}
            onChange={(event) => setPublicNote(event.target.value)}
            className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
          <span className="text-xs text-slate-400">
            Included on the public /scan page alongside mandated fields.
          </span>
        </label>
      </div>

      {error ? (
        <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}
      {success ? (
        <div className="rounded-lg border border-emerald-400/40 bg-emerald-500/10 p-3 text-sm text-emerald-100">
          {success}
        </div>
      ) : null}

      <button
        type="submit"
        disabled={loading}
        className="inline-flex items-center justify-center gap-2 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 transition hover:brightness-105 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? "Saving..." : "Save passport and generate QR"}
      </button>
    </form>
  );
}
