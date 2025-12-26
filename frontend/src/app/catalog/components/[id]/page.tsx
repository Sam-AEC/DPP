"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";

import { listComponents, updateComponent } from "@/lib/api";
import type { Component } from "@/lib/types";

export default function EditComponentPage() {
  const router = useRouter();
  const params = useParams();
  const id = params?.id as string;
  const [component, setComponent] = useState<Component | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    listComponents()
      .then((list) => {
        const found = list.find((c) => c.id === id) || null;
        setComponent(found);
      })
      .catch(() => setError("Failed to load component"));
  }, [id]);

  const update = (patch: Partial<Component>) => {
    setComponent((prev) => (prev ? { ...prev, ...patch } : prev));
  };

  const submit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!component) return;
    setError(null);
    setLoading(true);
    try {
      await updateComponent(component.id, component);
      router.push("/catalog/components");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setLoading(false);
    }
  };

  if (!component) return <div className="p-6 text-slate-200">Loading...</div>;

  return (
    <main className="space-y-6">
      <div>
        <p className="text-xs uppercase tracking-[0.14em] text-slate-300">Catalog</p>
        <h1 className="text-3xl font-semibold text-slate-50">Edit component</h1>
      </div>
      <form onSubmit={submit} className="space-y-3 rounded-2xl border border-white/10 bg-slate-900/60 p-6">
        <input
          value={component.name}
          onChange={(e) => update({ name: e.target.value })}
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <input
          value={component.kind || ""}
          onChange={(e) => update({ kind: e.target.value })}
          placeholder="Kind"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        <textarea
          value={component.description || ""}
          onChange={(e) => update({ description: e.target.value })}
          placeholder="Description"
          className="w-full rounded-lg border border-white/10 bg-slate-950/70 p-3 text-slate-50"
        />
        {error ? (
          <div className="rounded-lg border border-red-400/40 bg-red-500/10 p-3 text-sm text-red-100">{error}</div>
        ) : null}
        <button
          type="submit"
          disabled={loading}
          className="rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg shadow-emerald-500/20 disabled:opacity-60"
        >
          {loading ? "Saving..." : "Save"}
        </button>
      </form>
    </main>
  );
}
