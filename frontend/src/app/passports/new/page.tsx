import { PassportForm } from "@/components/passport-form";
import { listTemplates } from "@/lib/api";

export default async function NewPassportPage({ searchParams }: { searchParams: Record<string, string | string[] | undefined> }) {
  const templates = await listTemplates().catch(() => []);
  const preselect = typeof searchParams.template === "string" ? searchParams.template : "";
  return (
    <main className="space-y-6">
      <div className="space-y-2">
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">
          Create
        </p>
        <h1 className="text-3xl font-semibold text-slate-50">
          New battery passport
        </h1>
        <p className="text-sm text-slate-300">
          Mandatory Annex XIII public fields are required. QR code is generated
          automatically and points to the /scan public page.
        </p>
      </div>
      <PassportForm templates={templates} initialTemplateId={preselect} />
    </main>
  );
}
