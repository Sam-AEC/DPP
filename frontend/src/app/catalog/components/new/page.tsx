"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { createComponent } from "@/lib/api";

export default function NewComponentPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [kind, setKind] = useState("");
  const [description, setDescription] = useState("");
  const [hazards, setHazards] = useState("");
  const [cfRef, setCfRef] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await createComponent({
        name,
        kind,
        description,
        hazardous_substances: hazards,
        carbon_footprint_ref: cfRef,
      });
      router.push("/catalog/components");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create component");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Catalog</p>
        <h1 className="text-3xl font-semibold text-slate-50">New component</h1>
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
          Kind
          <input
            value={kind}
            onChange={(e) => setKind(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Description
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Hazardous substances
          <input
            value={hazards}
            onChange={(e) => setHazards(e.target.value)}
            className="rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50 outline-none ring-emerald-400/30 focus:ring-2"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-100">
          Carbon footprint reference
          <input
            value={cfRef}
            onChange={(e) => setCfRef(e.target.value)}
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
          {loading ? "Saving..." : "Save component"}
        </button>
      </form>
    </main>
  );
}
