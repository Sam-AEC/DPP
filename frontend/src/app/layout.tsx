import Link from "next/link";
import type { Metadata } from "next";
import { IBM_Plex_Mono, Space_Grotesk } from "next/font/google";
import "./globals.css";

const display = Space_Grotesk({
  variable: "--font-display",
  subsets: ["latin"],
});

const mono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Battery Passport Studio",
  description:
    "SME-friendly Digital Product Passport builder with QR codes, public views, and compliance essentials.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${display.variable} ${mono.variable} antialiased`}>
        <div className="min-h-screen bg-slate-950 text-slate-50">
          <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_10%_20%,rgba(94,252,199,0.12),transparent_30%),radial-gradient(circle_at_90%_10%,rgba(18,194,233,0.18),transparent_25%),radial-gradient(circle_at_50%_70%,rgba(50,120,255,0.12),transparent_30%)]" />
          <div className="relative mx-auto max-w-6xl px-6 py-10">
            <nav className="mb-8 flex flex-wrap items-center justify-between gap-4 rounded-full border border-white/10 bg-slate-900/60 px-5 py-3 shadow-lg shadow-cyan-500/10">
              <Link href="/" className="flex items-center gap-3 text-sm font-semibold">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-emerald-400 to-cyan-400 text-slate-950 shadow-inner shadow-emerald-500/40">
                  DPP
                </span>
                Battery Passport Studio
              </Link>
              <div className="flex flex-wrap items-center gap-2 text-sm text-slate-100">
                <Link
                  href="/passports"
                  className="rounded-full px-4 py-2 hover:bg-white/5"
                >
                  Registry
                </Link>
                <Link
                  href="/passports/new"
                  className="rounded-full bg-white/10 px-4 py-2 font-semibold hover:bg-white/20"
                >
                  New passport
                </Link>
              </div>
            </nav>
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
