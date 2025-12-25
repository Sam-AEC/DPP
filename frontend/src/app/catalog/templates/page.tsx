import Link from "next/link";

import { listTemplates } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function TemplatesPage() {
  const templates = await listTemplates().catch(() => []);

  return (
    <main className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
            Catalog
          </p>
          <h1 className="text-3xl font-semibold text-slate-50">
            Product templates
          </h1>
          <p className="text-sm text-slate-300">
            Prefill passports with defaults for each battery model.
          </p>
        </div>
        <Link
          href="/passports/new"
          className="rounded-full bg-white/10 px-4 py-2 text-sm font-semibold text-slate-50 hover:bg-white/20"
        >
          Create passport
        </Link>
      </div>

      {templates.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No templates yet. Import via jobs API or create through backend.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {templates.map((template) => (
            <div
              key={template.id}
              className="rounded-xl border border-white/10 bg-slate-900/70 p-4"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                    {template.battery_category}
                  </p>
                  <h3 className="text-lg font-semibold text-slate-50">
                    {template.battery_model || template.name}
                  </h3>
                  <p className="text-sm text-slate-300">
                    {template.manufacturer_name || "Manufacturer N/A"}
                  </p>
                </div>
                <span className="text-[11px] text-slate-400">
                  {new Date(template.created_at).toLocaleDateString()}
                </span>
              </div>
              <div className="mt-3 grid grid-cols-2 gap-2 text-xs text-slate-300">
                <div>
                  <p className="text-slate-400">GTIN</p>
                  <p className="font-mono">{template.gtin || "N/A"}</p>
                </div>
                <div>
                  <p className="text-slate-400">Capacity</p>
                  <p className="font-mono">{template.rated_capacity_kwh ?? "N/A"} kWh</p>
                </div>
                <div>
                  <p className="text-slate-400">Weight</p>
                  <p className="font-mono">{template.battery_weight_kg ?? "N/A"} kg</p>
                </div>
                <div>
                  <p className="text-slate-400">CF class</p>
                  <p className="font-mono">{template.carbon_footprint_class || "N/A"}</p>
                </div>
              </div>
              <div className="mt-3 flex flex-wrap gap-3 text-xs text-cyan-100">
                <a
                  className="underline"
                  href={`/api/dop/templates/${template.id}/pdf`}
                  target="_blank"
                >
                  Download DoP PDF
                </a>
              </div>
              <p className="mt-2 text-xs text-slate-400">
                Use this template in the passport creator to prefill Annex XIII fields.
              </p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
