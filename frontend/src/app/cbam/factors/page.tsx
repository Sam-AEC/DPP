"use client";

import { useEffect, useState } from "react";

import { createCbamFactor, listCbamFactors } from "@/lib/api";

export default function FactorsPage() {
  const [factors, setFactors] = useState<any[]>([]);
  const [prefix, setPrefix] = useState("");
  const [ef, setEf] = useState<number | string>("");
  const [source, setSource] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = () => {
    listCbamFactors().then(setFactors).catch(() => setFactors([]));
  };

  useEffect(() => {
    refresh();
  }, []);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await createCbamFactor({
        cn_prefix: prefix,
        emission_factor: typeof ef === "string" ? Number(ef) : ef,
        source,
      });
      setPrefix("");
      setEf("");
      setSource("");
      refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create factor");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">CBAM</p>
        <h1 className="text-3xl font-semibold text-slate-50">Factor library</h1>
        <p className="text-sm text-slate-300">Override default emission factors per CN prefix.</p>
      </div>
      <form onSubmit={submit} className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            value={prefix}
            onChange={(e) => setPrefix(e.target.value)}
            placeholder="CN prefix (e.g., 7208)"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
          <input
            type="number"
            value={ef}
            onChange={(e) => setEf(e.target.value)}
            placeholder="Emission factor"
            className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
          />
        </div>
        <input
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Source (optional)"
          className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
        />
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
          {loading ? "Saving..." : "Add factor"}
        </button>
      </form>

      <div className="space-y-3">
        {factors.map((f) => (
          <div key={f.id} className="rounded-xl border border-white/10 bg-slate-900/70 p-4 text-sm text-slate-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-slate-50">CN {f.cn_prefix}</p>
                <p className="text-xs text-slate-400">{f.source || "No source"}</p>
              </div>
              <p className="font-mono text-xs text-emerald-200">EF: {f.emission_factor}</p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
