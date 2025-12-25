"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { createTemplate } from "@/lib/api";

export default function NewTemplatePage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [model, setModel] = useState("");
  const [category, setCategory] = useState("industrial");
  const [gtin, setGtin] = useState("");
  const [capacity, setCapacity] = useState<number | string>("");
  const [weight, setWeight] = useState<number | string>("");
  const [cfClass, setCfClass] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await createTemplate({
        name,
        battery_model: model,
        battery_category: category,
        gtin,
        rated_capacity_kwh: typeof capacity === "string" ? Number(capacity) || undefined : capacity,
        battery_weight_kg: typeof weight === "string" ? Number(weight) || undefined : weight,
        carbon_footprint_class: cfClass,
      });
      router.push("/catalog/templates");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create template");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Catalog</p>
        <h1 className="text-3xl font-semibold text-slate-50">New template</h1>
      </div>
      <form onSubmit={submit} className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Name
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Battery model
          <input
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Category
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          >
            <option value="lmt">LMT</option>
            <option value="industrial">Industrial</option>
            <option value="ev">EV</option>
          </select>
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          GTIN
          <input
            value={gtin}
            onChange={(e) => setGtin(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="flex flex-col gap-2 text-sm text-slate-100">
            Rated capacity (kWh)
            <input
              type="number"
              value={capacity}
              onChange={(e) => setCapacity(e.target.value)}
              className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
            />
          </label>
          <label className="flex flex-col gap-2 text-sm text-slate-100">
            Weight (kg)
            <input
              type="number"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
            />
          </label>
        </div>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Carbon footprint class
          <input
            value={cfClass}
            onChange={(e) => setCfClass(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>

        {error ? (
          <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">
            {error}
          </div>
        ) : null}
        <button
          type="submit"
          disabled={loading}
          className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Saving..." : "Save template"}
        </button>
      </form>
    </main>
  );
}
