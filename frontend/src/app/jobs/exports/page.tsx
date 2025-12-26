"use client";

import { useState } from "react";

import { createExportJob, listExportJobs, runExportJob } from "@/lib/api";

export default function ExportJobsPage() {
  const [kind, setKind] = useState("passports");
  const [jobs, setJobs] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = () => {
    listExportJobs().then(setJobs).catch(() => setJobs([]));
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const job = await createExportJob(kind);
      await runExportJob(job.id);
      refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to export");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Jobs</p>
        <h1 className="text-3xl font-semibold text-slate-50">Export jobs</h1>
        <p className="text-sm text-slate-300">Run exports for passports or CBAM declarations.</p>
      </div>
      <form onSubmit={submit} className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4">
        <select
          value={kind}
          onChange={(e) => setKind(e.target.value)}
          className="rounded-lg border border-white/10 bg-slate-950/70 p-2 text-slate-50"
        >
          <option value="passports">Passports</option>
          <option value="cbam">CBAM</option>
        </select>
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
          {loading ? "Exporting..." : "Run export"}
        </button>
      </form>

      <button
        onClick={refresh}
        className="rounded-full border border-white/15 px-4 py-2 text-xs text-slate-100 hover:border-cyan-200/70"
      >
        Refresh
      </button>

      <div className="space-y-3">
        {jobs.map((job) => (
          <div key={job.id} className="rounded-xl border border-white/10 bg-slate-900/70 p-4 text-sm text-slate-200">
            <div className="flex items-center justify-between">
              <span className="font-semibold">{job.kind}</span>
              <span className="text-xs text-slate-400">{job.status}</span>
            </div>
            {job.result ? (
              <pre className="mt-2 whitespace-pre-wrap text-xs text-slate-200">
                {JSON.stringify(job.result, null, 2)}
              </pre>
            ) : null}
            {job.error ? (
              <p className="text-xs text-red-200">Error: {job.error}</p>
            ) : null}
            {job.result?.csv ? (
              <a
                href={`data:text/csv;charset=utf-8,${encodeURIComponent(job.result.csv)}`}
                download={`${job.kind}.csv`}
                className="mt-2 inline-flex text-xs text-cyan-100 underline"
              >
                Download CSV
              </a>
            ) : null}
            {job.result?.json ? (
              <a
                href={`data:application/json;charset=utf-8,${encodeURIComponent(JSON.stringify(job.result.json))}`}
                download={`${job.kind}.json`}
                className="mt-2 inline-flex text-xs text-cyan-100 underline"
              >
                Download JSON
              </a>
            ) : null}
          </div>
        ))}
      </div>
    </main>
  );
}
