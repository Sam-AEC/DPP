import Link from "next/link";

import { PassportCard } from "@/components/passport-card";
import { listPassports } from "@/lib/api";
import type { BatteryPassport } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function PassportsPage() {
  let passports: BatteryPassport[] = [];
  let error: string | null = null;

  try {
    passports = await listPassports();
  } catch (err) {
    error = err instanceof Error ? err.message : "Failed to load passports.";
  }

  return (
    <main className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
            Passport registry
          </p>
          <h1 className="text-3xl font-semibold text-slate-50">
            Battery passports
          </h1>
          <p className="text-sm text-slate-300">
            Public tier is QR-ready. Restricted data stays server-side.
          </p>
        </div>
        <Link
          href="/passports/new"
          className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-5 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 transition hover:brightness-105"
        >
          New passport
        </Link>
      </div>

      {error ? (
        <div className="rounded-xl border border-red-400/40 bg-red-500/10 p-4 text-sm text-red-100">
          {error}
        </div>
      ) : null}

      {passports.length === 0 ? (
        <div className="rounded-xl border border-dashed border-white/15 bg-slate-900/60 p-6 text-slate-300">
          No passports yet. Start with a single record or import via the REST
          API.
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {passports.map((passport) => (
            <PassportCard key={passport.id} passport={passport} />
          ))}
        </div>
      )}
    </main>
  );
}
