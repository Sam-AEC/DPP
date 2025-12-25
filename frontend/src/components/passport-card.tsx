import Link from "next/link";

import type { BatteryPassport } from "@/lib/types";

type Props = {
  passport: BatteryPassport;
};

export function PassportCard({ passport }: Props) {
  return (
    <div className="group flex flex-col gap-3 rounded-xl border border-white/10 bg-slate-900/70 p-4 shadow-sm shadow-cyan-500/5 transition hover:-translate-y-1 hover:border-cyan-300/50 hover:shadow-lg hover:shadow-cyan-500/20">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.15em] text-slate-400">
              {passport.battery_category} | {passport.battery_status}
            </p>
          <h3 className="mt-1 text-lg font-semibold text-slate-50">
            {passport.battery_model}
          </h3>
          <p className="text-sm text-slate-300">{passport.manufacturer_name}</p>
        </div>
        <div className="rounded-full bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-200">
          QR ready
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm text-slate-200 sm:grid-cols-4">
        <div>
          <p className="text-xs text-slate-400">Capacity</p>
          <p className="font-semibold">{passport.rated_capacity_kwh} kWh</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Weight</p>
          <p className="font-semibold">{passport.battery_weight_kg} kg</p>
        </div>
        <div>
          <p className="text-xs text-slate-400">CO2e</p>
          <p className="font-semibold">
            {passport.carbon_footprint_kg_per_kwh} kg/kWh
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-400">Created</p>
          <p className="font-semibold">
            {new Date(passport.created_at).toLocaleDateString()}
          </p>
        </div>
      </div>

      <Link
        href={`/passports/${passport.id}`}
        className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-800 px-4 py-2 text-sm font-semibold text-cyan-200 transition hover:bg-slate-700 group-hover:text-cyan-50"
      >
        View passport
      </Link>
    </div>
  );
}
