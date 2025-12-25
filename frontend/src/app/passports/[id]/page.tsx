import Link from "next/link";
import { notFound } from "next/navigation";

import { API_BASE_URL, getPassport } from "@/lib/api";
import type { BatteryPassport } from "@/lib/types";

export const dynamic = "force-dynamic";

type Props = {
  params: { id: string };
};

function infoRow(label: string, value: string | number | undefined) {
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

export default async function PassportDetailPage({ params }: Props) {
  let passport: BatteryPassport | null = null;
  try {
    passport = await getPassport(params.id);
  } catch (err) {
    console.error(err);
  }

  if (!passport) {
    notFound();
  }

  const scanUrl = `${
    process.env.NEXT_PUBLIC_SCAN_BASE || "http://localhost:3000/scan"
  }/${params.id}`;
  const qrUrl = `${API_BASE_URL}/passports/${params.id}/qr`;

  return (
    <main className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
            Passport detail
          </p>
          <h1 className="text-3xl font-semibold text-slate-50">
            {passport.battery_model}
          </h1>
          <p className="text-sm text-slate-300">
            {passport.manufacturer_name} | {passport.battery_category}
          </p>
        </div>
        <Link
          href="/passports"
          className="inline-flex items-center gap-2 rounded-full border border-white/15 px-4 py-2 text-sm font-semibold text-slate-50 transition hover:border-cyan-200/70"
        >
          Back to registry
        </Link>
      </div>

      <div className="grid gap-4 md:grid-cols-[2fr,1fr]">
        <div className="space-y-4 rounded-2xl border border-white/10 bg-slate-900/60 p-5 shadow-lg shadow-cyan-500/10">
          <div className="grid gap-3 sm:grid-cols-2">
            {infoRow("GTIN", passport.gtin)}
            {infoRow("Serial", passport.serial_number)}
            {infoRow("Capacity", `${passport.rated_capacity_kwh} kWh`)}
            {infoRow("Weight", `${passport.battery_weight_kg} kg`)}
            {infoRow(
              "Carbon footprint",
              `${passport.carbon_footprint_kg_per_kwh} kg/kWh`,
            )}
            {infoRow("CF class", passport.carbon_footprint_class)}
            {infoRow("Lifetime (cycles)", passport.expected_lifetime_cycles)}
            {infoRow("Lifetime (years)", passport.expected_lifetime_years)}
          </div>

          <div className="rounded-xl border border-white/10 bg-slate-950/60 p-4">
            <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
              Hazardous substances
            </p>
            <p className="text-sm text-slate-200">
              {passport.hazardous_substances || "None listed"}
            </p>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-xl border border-white/10 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                Additional public data
              </p>
              <pre className="mt-2 whitespace-pre-wrap text-xs text-slate-200">
                {passport.additional_public_data
                  ? JSON.stringify(passport.additional_public_data, null, 2)
                  : "No extra notes"}
              </pre>
            </div>
            <div className="rounded-xl border border-white/10 bg-slate-950/60 p-4">
              <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                Restricted data (server-side)
              </p>
              <pre className="mt-2 whitespace-pre-wrap text-xs text-slate-200">
                {passport.restricted_data
                  ? JSON.stringify(passport.restricted_data, null, 2)
                  : "Empty"}
              </pre>
              <p className="mt-2 text-xs text-slate-400">
                Add conformity docs, test reports, dismantling info here via API
                or a private admin form.
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-slate-900/60 p-5 shadow-lg shadow-cyan-500/10">
          <div className="flex items-center justify-between">
            <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
              QR code
            </p>
            <span className="rounded-full bg-emerald-400/15 px-3 py-1 text-[11px] font-semibold text-emerald-100">
              Public tier
            </span>
          </div>
          <div className="flex items-center justify-center rounded-xl border border-dashed border-white/10 bg-slate-950/60 p-4">
            <img
              src={qrUrl}
              alt="QR code for this passport"
              className="h-48 w-48 rounded-lg bg-white p-2"
            />
          </div>
          <div className="rounded-lg border border-white/10 bg-slate-950/60 p-3 text-sm text-slate-200">
            <p className="font-semibold text-cyan-100">Scan destination</p>
            <p className="font-mono text-xs text-slate-200 break-all">
              {scanUrl}
            </p>
          </div>
          <p className="text-xs text-slate-400">
            The QR is ISO/IEC 18004:2015 compliant and follows a GS1 Digital
            Link friendly URL shape.
          </p>
        </div>
      </div>
    </main>
  );
}
