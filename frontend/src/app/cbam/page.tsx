import Link from "next/link";

import { listCbamDeclarations } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function CbamPage() {
  const declarations = await listCbamDeclarations().catch(() => []);

  return (
    <main className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
            CBAM
          </p>
          <h1 className="text-3xl font-semibold text-slate-50">
            Declarations
          </h1>
          <p className="text-sm text-slate-300">
            Manage CBAM reports with default vs verified emission factors.
          </p>
        </div>
        <Link
          href="/cbam/new"
          className="rounded-full bg-white/10 px-4 py-2 text-sm font-semibold text-slate-50 hover:bg-white/20"
        >
          New declaration
        </Link>
      </div>
      <Link
        href="/cbam/suppliers"
        className="inline-flex text-xs text-cyan-100 underline"
      >
        Manage suppliers
      </Link>

      {declarations.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No declarations yet. Create one with CN codes, quantities, and factors.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {declarations.map((decl) => (
            <div
              key={decl.id}
              className="rounded-xl border border-white/10 bg-slate-900/70 p-4"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                    {decl.period}
                  </p>
                  <h3 className="text-lg font-semibold text-slate-50">
                    {decl.total_emissions ?? 0} tCO2e
                  </h3>
                  <p className="text-sm text-slate-300">
                    Cost est.: €{decl.certificate_cost_estimate ?? 0}
                  </p>
                </div>
                <span className="text-[11px] text-slate-400">
                  {decl.status}
                </span>
              </div>
              <div className="mt-3 flex flex-wrap gap-2 text-xs text-cyan-100">
                <a
                  className="underline"
                  href={`/api/cbam/declarations/${decl.id}/export/csv`}
                  target="_blank"
                >
                  CSV
                </a>
                <a
                  className="underline"
                  href={`/api/cbam/declarations/${decl.id}/export/pdf`}
                  target="_blank"
                >
                  PDF
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
