import { notFound } from "next/navigation";

import { getPublicPassport } from "@/lib/api";
import type { PublicPassport } from "@/lib/types";

export const dynamic = "force-dynamic";

type Props = {
  params: { id: string };
};

function publicRow(label: string, value: string | number | undefined) {
  return (
    <div className="rounded-lg border border-white/10 bg-slate-950/60 p-3">
      <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
        {label}
      </p>
      <p className="text-sm font-semibold text-slate-100">
        {value ?? "N/A"}
      </p>
    </div>
  );
}

export default async function PublicScanPage({ params }: Props) {
  let passport: PublicPassport | null = null;

  try {
    passport = await getPublicPassport(params.id);
  } catch (err) {
    console.error(err);
  }

  if (!passport) {
    notFound();
  }

  return (
    <main className="space-y-5 rounded-3xl border border-white/10 bg-slate-900/70 p-6 shadow-xl shadow-emerald-500/10">
      <div className="space-y-2">
        <p className="text-xs uppercase tracking-[0.14em] text-emerald-200">
          Public passport
        </p>
        <h1 className="text-3xl font-semibold text-slate-50">
          {passport.battery_model}
        </h1>
        <p className="text-sm text-slate-300">
          {passport.manufacturer_name} | {passport.manufacturing_place}
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-3">
        {publicRow("GTIN", passport.gtin)}
        {publicRow("Serial", passport.serial_number)}
        {publicRow("Capacity", `${passport.rated_capacity_kwh} kWh`)}
        {publicRow(
          "Carbon footprint",
          `${passport.carbon_footprint_kg_per_kwh} kg/kWh`,
        )}
        {publicRow("Recycled cobalt", passport.recycled_content_cobalt)}
        {publicRow("Recycled nickel", passport.recycled_content_nickel)}
        {publicRow("Weight", `${passport.battery_weight_kg} kg`)}
        {publicRow("Performance class", passport.performance_class)}
        {publicRow("Status", passport.battery_status)}
      </div>

      <div className="rounded-xl border border-white/10 bg-slate-950/60 p-4 text-sm text-slate-200">
        <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
          Carbon footprint class
        </p>
        <p className="text-lg font-semibold text-emerald-100">
          {passport.carbon_footprint_class || "Not provided"}
        </p>
        <p className="mt-1 text-xs text-slate-400">
          This page only shows Annex XIII public fields. Dismantling and safety
          data is available to authorized operators through the restricted API.
        </p>
      </div>

      <div className="rounded-xl border border-emerald-400/30 bg-emerald-500/5 p-4 text-sm text-emerald-100">
        Verified public snapshot generated{" "}
        {new Date(passport.created_at).toLocaleDateString()}.
      </div>
    </main>
  );
}
