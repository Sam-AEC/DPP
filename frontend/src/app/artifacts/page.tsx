"use client";

import { useEffect, useState } from "react";

import { listArtifacts } from "@/lib/api";

export default function ArtifactsPage() {
  const [artifacts, setArtifacts] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listArtifacts().then(setArtifacts).catch((err) => setError(err instanceof Error ? err.message : "Failed to load"));
  }, []);

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Artifacts</p>
        <h1 className="text-3xl font-semibold text-slate-50">Restricted artifacts</h1>
        <p className="text-sm text-slate-300">Server-side documents (conformity, test, dismantling, safety).</p>
      </div>
      {error ? (
        <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">
          {error}
        </div>
      ) : null}
      {artifacts.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No artifacts yet. Use the API to upload metadata and files.
        </div>
      ) : (
        <div className="space-y-3">
          {artifacts.map((a) => (
            <div key={a.id} className="rounded-xl border border-white/10 bg-slate-900/70 p-4 text-sm text-slate-200">
              <div className="flex items-center justify-between">
                <p className="font-semibold text-slate-50">{a.title}</p>
                <span className="text-xs text-slate-400">{a.kind}</span>
              </div>
              <p className="text-xs text-slate-300">Passport: {a.passport_id}</p>
              {a.url ? (
                <a className="text-xs text-cyan-100 underline" href={a.url} target="_blank">
                  View
                </a>
              ) : null}
              {a.metadata ? (
                <pre className="mt-2 whitespace-pre-wrap text-xs text-slate-200">
                  {JSON.stringify(a.metadata, null, 2)}
                </pre>
              ) : null}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
