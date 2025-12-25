"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { createCbamDeclaration, listCbamSuppliers } from "@/lib/api";
import type { CbamItemPayload } from "@/lib/types";

export default function NewCbamPage() {
  const router = useRouter();
  const [period, setPeriod] = useState("2025-Q4");
  const [items, setItems] = useState<CbamItemPayload[]>([
    { cn_code: "7208", product_description: "Flat-rolled steel", quantity_tonnes: 10 },
  ]);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listCbamSuppliers().then(setSuppliers).catch(() => setSuppliers([]));
  }, []);

  const updateItem = (index: number, patch: Partial<CbamItemPayload>) => {
    setItems((prev) =>
      prev.map((item, i) => (i === index ? { ...item, ...patch } : item)),
    );
  };

  const addItem = () => {
    setItems((prev) => [...prev, { cn_code: "", quantity_tonnes: 0 }]);
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await createCbamDeclaration({ period, items });
      router.push("/cbam");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create declaration");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">CBAM</p>
        <h1 className="text-3xl font-semibold text-slate-50">New declaration</h1>
        <p className="text-sm text-slate-300">Enter CN codes, quantities, and factors.</p>
      </div>
      <form onSubmit={submit} className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Period
          <input
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-cyan-400/30 focus:ring-2"
          />
        </label>

        <div className="space-y-4">
          {items.map((item, idx) => (
            <div key={idx} className="rounded-xl border border-white/10 bg-slate-950/60 p-4 space-y-3">
              <div className="grid gap-3 sm:grid-cols-2">
                <label className="flex flex-col gap-1 text-xs text-slate-200">
                  CN code
                  <input
                    value={item.cn_code}
                    onChange={(e) => updateItem(idx, { cn_code: e.target.value })}
                    className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
                  />
                </label>
                <label className="flex flex-col gap-1 text-xs text-slate-200">
                  Quantity (tonnes)
                  <input
                    type="number"
                    value={item.quantity_tonnes}
                    onChange={(e) => updateItem(idx, { quantity_tonnes: Number(e.target.value) })}
                    className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
                  />
                </label>
                <label className="flex flex-col gap-1 text-xs text-slate-200">
                  Verified EF
                  <input
                    type="number"
                    value={item.verified_emission_factor ?? ""}
                    onChange={(e) =>
                      updateItem(idx, { verified_emission_factor: Number(e.target.value) || undefined })
                    }
                    className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
                  />
                </label>
                <label className="flex flex-col gap-1 text-xs text-slate-200">
                  Supplier
                  <select
                    value={item.supplier_id || ""}
                    onChange={(e) => updateItem(idx, { supplier_id: e.target.value || undefined })}
                    className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
                  >
                    <option value="">None</option>
                    {suppliers.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name} ({s.country || "N/A"})
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              <label className="flex flex-col gap-1 text-xs text-slate-200">
                Description
                <input
                  value={item.product_description || ""}
                  onChange={(e) => updateItem(idx, { product_description: e.target.value })}
                  className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
                />
              </label>
            </div>
          ))}
        </div>

        {error ? (
          <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">
            {error}
          </div>
        ) : null}
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={addItem}
            className="rounded-full border border-white/15 px-4 py-2 text-sm text-slate-100 hover:border-cyan-200/70"
          >
            Add line
          </button>
          <button
            type="submit"
            disabled={loading}
            className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Saving..." : "Save declaration"}
          </button>
        </div>
      </form>
    </main>
  );
}
