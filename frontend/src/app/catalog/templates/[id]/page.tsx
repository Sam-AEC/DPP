"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";

import { listTemplates, updateTemplate } from "@/lib/api";
import type { ProductTemplate } from "@/lib/types";

export default function EditTemplatePage() {
  const params = useParams();
  const id = params?.id as string;
  const router = useRouter();
  const [template, setTemplate] = useState<ProductTemplate | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listTemplates()
      .then((list) => {
        const found = list.find((t) => t.id === id) || null;
        setTemplate(found);
      })
      .catch(() => setError("Failed to load template"));
  }, [id]);

  const update = (patch: Partial<ProductTemplate>) => {
    setTemplate((prev) => (prev ? { ...prev, ...patch } : prev));
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!template) return;
    setError(null);
    setLoading(true);
    try {
      await updateTemplate(template.id, template);
      router.push("/catalog/templates");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setLoading(false);
    }
  };

  if (!template) return <div className="p-6 text-slate-200">Loading...</div>;

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Catalog</p>
        <h1 className="text-3xl font-semibold text-slate-50">Edit template</h1>
      </div>
      <form onSubmit={submit} className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <input
          value={template.name}
          onChange={(e) => update({ name: e.target.value })}
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <input
          value={template.battery_model || ""}
          onChange={(e) => update({ battery_model: e.target.value })}
          placeholder="Battery model"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <select
          value={template.battery_category}
          onChange={(e) => update({ battery_category: e.target.value })}
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        >
          <option value="lmt">LMT</option>
          <option value="industrial">Industrial</option>
          <option value="ev">EV</option>
        </select>
        <input
          value={template.gtin || ""}
          onChange={(e) => update({ gtin: e.target.value })}
          placeholder="GTIN"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <input
          type="number"
          value={template.rated_capacity_kwh || ""}
          onChange={(e) => update({ rated_capacity_kwh: Number(e.target.value) || undefined })}
          placeholder="Capacity kWh"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <input
          type="number"
          value={template.battery_weight_kg || ""}
          onChange={(e) => update({ battery_weight_kg: Number(e.target.value) || undefined })}
          placeholder="Weight kg"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        {error ? (
          <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">{error}</div>
        ) : null}
        <button
          type="submit"
          disabled={loading}
          className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 disabled:opacity-60"
        >
          {loading ? "Saving..." : "Save"}
        </button>
      </form>
    </main>
  );
}
