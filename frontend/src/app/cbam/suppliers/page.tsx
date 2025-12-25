"use client";

import { useEffect, useState } from "react";

import { createCbamSupplier, listCbamSuppliers } from "@/lib/api";

export default function SuppliersPage() {
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [country, setCountry] = useState("");
  const [ef, setEf] = useState<number | string>("");
  const [contact, setContact] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = () => {
    listCbamSuppliers().then(setSuppliers).catch(() => setSuppliers([]));
  };

  useEffect(() => {
    refresh();
  }, []);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await createCbamSupplier({
        name,
        country,
        default_emission_factor: typeof ef === "string" ? Number(ef) || undefined : ef,
        contact,
      });
      setName("");
      setCountry("");
      setEf("");
      setContact("");
      refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create supplier");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">CBAM</p>
        <h1 className="text-3xl font-semibold text-slate-50">Suppliers</h1>
        <p className="text-sm text-slate-300">Manage supplier default emission factors.</p>
      </div>
      <form onSubmit={submit} className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Supplier name"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
          <input
            value={country}
            onChange={(e) => setCountry(e.target.value)}
            placeholder="Country"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
        </div>
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            type="number"
            value={ef}
            onChange={(e) => setEf(e.target.value)}
            placeholder="Default emission factor"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
          <input
            value={contact}
            onChange={(e) => setContact(e.target.value)}
            placeholder="Contact"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
        </div>
        {error ? (
          <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-2 text-sm text-red-100">
            {error}
          </div>
        ) : null}
        <button
            type="submit"
            disabled={loading}
            className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-4 py-2 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? "Saving..." : "Add supplier"}
          </button>
      </form>

      <div className="space-y-3">
        {suppliers.map((s) => (
          <div key={s.id} className="rounded-xl border border-white/10 bg-slate-900/70 p-4 text-sm text-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-slate-50">{s.name}</p>
                <p className="text-xs text-slate-400">{s.country || "N/A"}</p>
              </div>
              <p className="font-mono text-xs text-emerald-200">
                EF: {s.default_emission_factor ?? "N/A"}
              </p>
            </div>
            {s.contact ? <p className="text-xs text-slate-300">Contact: {s.contact}</p> : null}
          </div>
        ))}
      </div>
    </main>
  );
}
