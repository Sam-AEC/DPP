import { listAuditLogs } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const logs = await listAuditLogs().catch(() => []);

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Audit</p>
        <h1 className="text-3xl font-semibold text-slate-50">Recent activity</h1>
        <p className="text-sm text-slate-300">Last 200 entries scoped to your API key.</p>
      </div>
      {logs.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No audit entries yet.
        </div>
      ) : (
        <div className="space-y-3">
          {logs.map((log) => (
            <div
              key={log.id}
              className="rounded-xl border border-white/10 bg-slate-900/70 p-4 text-sm text-slate-200"
            >
              <div className="flex items-center justify-between">
                <div className="font-mono text-xs text-cyan-100">{log.action}</div>
                <div className="text-[11px] text-slate-400">
                  {new Date(log.created_at).toLocaleString()}
                </div>
              </div>
              <p className="text-xs text-slate-300">
                {log.entity} / {log.entity_id}
              </p>
              {log.details ? (
                <pre className="mt-2 whitespace-pre-wrap text-xs text-slate-200">
                  {JSON.stringify(log.details, null, 2)}
                </pre>
              ) : null}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
