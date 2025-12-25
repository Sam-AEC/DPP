import Link from "next/link";

const highlights = [
  {
    title: "Battery passport deadline",
    value: "18 Feb 2027",
    note: "14 months to ship",
  },
  {
    title: "SME ready",
    value: "EUR 99-299/mo",
    note: "pricing placeholder for GTM",
  },
  {
    title: "Data tiers",
    value: "Public + Restricted",
    note: "Annex XIII mapped",
  },
];

const benefits = [
  "QR codes that resolve to public pages instantly",
  "Public vs restricted fields kept separate",
  "Export-ready JSON for regulators and partners",
  "Built for battery importers, assemblers, and installers",
];

export default function Home() {
  return (
    <main className="flex flex-col gap-10">
      <header className="rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900/70 via-slate-900/40 to-slate-800/40 p-8 shadow-2xl shadow-cyan-500/10">
        <div className="flex flex-wrap items-center gap-3 text-xs uppercase tracking-[0.16em] text-slate-300">
          <span className="rounded-full bg-emerald-400/15 px-3 py-1 text-emerald-100">
            Battery passport MVP
          </span>
          <span className="rounded-full bg-cyan-400/15 px-3 py-1 text-cyan-100">
            SME-first
          </span>
          <span className="rounded-full bg-white/10 px-3 py-1 text-slate-200">
            Annex XIII aligned
          </span>
        </div>
        <div className="mt-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div className="max-w-3xl space-y-4">
            <h1 className="text-4xl font-semibold leading-tight text-slate-50 md:text-5xl">
              Launch battery passports without enterprise bloat.
            </h1>
            <p className="text-lg text-slate-300 md:text-xl">
              Capture Annex XIII public fields, keep restricted data guarded,
              and ship QR-ready passports your customers can scan today.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link
                href="/passports/new"
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 transition hover:scale-[1.01] hover:brightness-105"
              >
                Create passport
              </Link>
              <Link
                href="/passports"
                className="inline-flex items-center gap-2 rounded-full border border-white/15 px-6 py-3 text-sm font-semibold text-slate-50 transition hover:border-cyan-200/70 hover:text-cyan-50"
              >
                View registry
              </Link>
            </div>
          </div>
          <div className="grid gap-3 rounded-2xl border border-white/10 bg-slate-900/60 p-4 text-sm text-slate-200 shadow-md shadow-cyan-500/10">
            <div className="flex items-center justify-between">
              <span>Public scan URL</span>
              <span className="font-mono text-xs text-emerald-200">
                /scan/&lt;uuid&gt;
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span>API base</span>
              <span className="font-mono text-xs text-cyan-200">
                /api/passports
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span>Export</span>
              <span className="font-mono text-xs text-slate-200">JSON / QR</span>
            </div>
          </div>
        </div>

        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          {highlights.map((item) => (
            <div
              key={item.title}
              className="rounded-xl border border-white/10 bg-slate-900/60 p-4 text-slate-200 shadow-sm shadow-cyan-500/10"
            >
              <p className="text-xs uppercase tracking-[0.14em] text-slate-400">
                {item.title}
              </p>
              <p className="mt-2 text-xl font-semibold text-slate-50">
                {item.value}
              </p>
              <p className="text-sm text-slate-400">{item.note}</p>
            </div>
          ))}
        </div>
      </header>

      <section className="grid gap-6 md:grid-cols-[2fr,1fr]">
        <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 shadow-lg shadow-cyan-500/10">
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs uppercase tracking-[0.16em] text-cyan-200">
              Build-ready
            </p>
            <span className="rounded-full bg-emerald-400/15 px-3 py-1 text-[11px] font-semibold text-emerald-100">
              API + UI + QR
            </span>
          </div>
          <h2 className="mt-3 text-2xl font-semibold text-slate-50">
            Everything needed for an audit-friendly MVP
          </h2>
          <div className="mt-4 grid gap-3 sm:grid-cols-2">
            {benefits.map((benefit) => (
              <div
                key={benefit}
                className="flex items-start gap-3 rounded-xl border border-white/5 bg-slate-950/60 p-4"
              >
                <span className="mt-1 h-2 w-2 rounded-full bg-emerald-300" />
                <p className="text-sm text-slate-200">{benefit}</p>
              </div>
            ))}
          </div>
          <div className="mt-4 rounded-xl border border-emerald-400/30 bg-emerald-500/5 p-4 text-sm text-emerald-100">
            February 18, 2027 is locked in for battery passports. This starter
            kit maps the Annex XIII public tier and leaves space for restricted
            fields, audit trails, and role-based access.
          </div>
        </div>

        <div className="rounded-3xl border border-white/10 bg-slate-900/60 p-6 shadow-lg shadow-cyan-500/10">
          <p className="text-xs uppercase tracking-[0.16em] text-slate-300">
            Quick start
          </p>
          <ol className="mt-4 space-y-3 text-sm text-slate-200">
            <li className="flex gap-3 rounded-lg border border-white/10 bg-slate-950/60 p-3">
              <span className="font-mono text-emerald-200">1</span>
              <span>Create a passport with mandatory public fields.</span>
            </li>
            <li className="flex gap-3 rounded-lg border border-white/10 bg-slate-950/60 p-3">
              <span className="font-mono text-emerald-200">2</span>
              <span>Share the QR link printed on-pack or engraved.</span>
            </li>
            <li className="flex gap-3 rounded-lg border border-white/10 bg-slate-950/60 p-3">
              <span className="font-mono text-emerald-200">3</span>
              <span>Use /api/passports for bulk imports or ERP sync.</span>
            </li>
          </ol>
          <div className="mt-6 space-y-2 text-xs text-slate-400">
            <p>Tech stack: Next.js 16 + FastAPI + PostgreSQL</p>
            <p>Hosting targets: Vercel (EU), Railway (EU), Supabase (EU)</p>
          </div>
        </div>
      </section>
    </main>
  );
}
