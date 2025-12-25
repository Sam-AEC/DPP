"use client";

import { useEffect, useState } from "react";

import {
  createAiSystem,
  createCraProduct,
  createEpdRecord,
  createEudrSupplier,
  createNis2Attestation,
  listAiSystems,
  listCraProducts,
  listEpdRecords,
  listEudrSuppliers,
  listNis2Attestations,
} from "@/lib/api";

export default function CompliancePage() {
  const [cra, setCra] = useState<any[]>([]);
  const [eudr, setEudr] = useState<any[]>([]);
  const [ai, setAi] = useState<any[]>([]);
  const [epd, setEpd] = useState<any[]>([]);
  const [nis2, setNis2] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const load = () => {
    listCraProducts().then(setCra).catch(() => setCra([]));
    listEudrSuppliers().then(setEudr).catch(() => setEudr([]));
    listAiSystems().then(setAi).catch(() => setAi([]));
    listEpdRecords().then(setEpd).catch(() => setEpd([]));
    listNis2Attestations().then(setNis2).catch(() => setNis2([]));
  };

  useEffect(() => {
    load();
  }, []);

  const handle = async (fn: () => Promise<any>) => {
    setError(null);
    try {
      await fn();
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    }
  };

  return (
    <main className="space-y-8">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Compliance</p>
        <h1 className="text-3xl font-semibold text-slate-50">Other modules</h1>
        <p className="text-sm text-slate-300">
          Minimal scaffolds for CRA, EUDR, AI Act, EPD, and NIS2 attestations.
        </p>
      </div>
      {error ? (
        <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}
      <div className="grid gap-4 md:grid-cols-2">
        <section className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
          <h2 className="text-lg font-semibold text-slate-50">CRA products</h2>
          <button
            onClick={() => handle(() => createCraProduct({ name: "New product", classification: "default" }))}
            className="rounded-full bg-white/10 px-3 py-2 text-xs text-slate-50 hover:bg-white/20"
          >
            Add CRA product
          </button>
          <div className="space-y-2 text-sm text-slate-200">
            {cra.map((p) => (
              <div key={p.id} className="rounded-lg border border-white/10 bg-slate-950/60 p-2">
                {p.name} ({p.classification || "default"})
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
          <h2 className="text-lg font-semibold text-slate-50">EUDR suppliers</h2>
          <button
            onClick={() => handle(() => createEudrSupplier({ name: "Supplier", country: "NL" }))}
            className="rounded-full bg-white/10 px-3 py-2 text-xs text-slate-50 hover:bg-white/20"
          >
            Add EUDR supplier
          </button>
          <div className="space-y-2 text-sm text-slate-200">
            {eudr.map((s) => (
              <div key={s.id} className="rounded-lg border border-white/10 bg-slate-950/60 p-2">
                {s.name} ({s.country || "N/A"})
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
          <h2 className="text-lg font-semibold text-slate-50">AI systems</h2>
          <button
            onClick={() => handle(() => createAiSystem({ name: "AI System", risk_level: "low" }))}
            className="rounded-full bg-white/10 px-3 py-2 text-xs text-slate-50 hover:bg-white/20"
          >
            Add AI system
          </button>
          <div className="space-y-2 text-sm text-slate-200">
            {ai.map((s) => (
              <div key={s.id} className="rounded-lg border border-white/10 bg-slate-950/60 p-2">
                {s.name} ({s.risk_level || "unknown"})
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
          <h2 className="text-lg font-semibold text-slate-50">EPD records</h2>
          <button
            onClick={() => handle(() => createEpdRecord({ product_name: "Product", pcr_reference: "EN 15804" }))}
            className="rounded-full bg-white/10 px-3 py-2 text-xs text-slate-50 hover:bg-white/20"
          >
            Add EPD record
          </button>
          <div className="space-y-2 text-sm text-slate-200">
            {epd.map((r) => (
              <div key={r.id} className="rounded-lg border border-white/10 bg-slate-950/60 p-2">
                {r.product_name} ({r.pcr_reference || "N/A"})
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
          <h2 className="text-lg font-semibold text-slate-50">NIS2 attestations</h2>
          <button
            onClick={() => handle(() => createNis2Attestation({ supplier_name: "Supplier", status: "pending" }))}
            className="rounded-full bg-white/10 px-3 py-2 text-xs text-slate-50 hover:bg-white/20"
          >
            Add attestation
          </button>
          <div className="space-y-2 text-sm text-slate-200">
            {nis2.map((n) => (
              <div key={n.id} className="rounded-lg border border-white/10 bg-slate-950/60 p-2">
                {n.supplier_name} ({n.status || "unknown"})
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
