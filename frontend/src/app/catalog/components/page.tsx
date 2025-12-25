import { listComponents } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function ComponentsPage() {
  const components = await listComponents().catch(() => []);

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
          Catalog
        </p>
        <h1 className="text-3xl font-semibold text-slate-50">
          Components library
        </h1>
        <p className="text-sm text-slate-300">
          Prefill passports/templates from reusable specs and test references.
        </p>
      </div>

      {components.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No components yet. Import via jobs API or add through the backend.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {components.map((component) => (
            <div
              key={component.id}
              className="rounded-xl border border-white/10 bg-slate-900/70 p-4"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                    {component.kind || "component"}
                  </p>
                  <h3 className="text-lg font-semibold text-slate-50">
                    {component.name}
                  </h3>
                </div>
                <span className="text-[11px] text-slate-400">
                  {new Date(component.created_at).toLocaleDateString()}
                </span>
              </div>
              {component.description ? (
                <p className="mt-2 text-sm text-slate-200">
                  {component.description}
                </p>
              ) : null}
              <div className="mt-3 space-y-1 text-xs text-slate-300">
                {component.carbon_footprint_ref ? (
                  <p>
                    CF ref: <span className="font-mono">{component.carbon_footprint_ref}</span>
                  </p>
                ) : null}
                {component.hazardous_substances ? (
                  <p>Hazards: {component.hazardous_substances}</p>
                ) : null}
                {component.test_report_refs?.length ? (
                  <p>Tests: {component.test_report_refs.join(", ")}</p>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
