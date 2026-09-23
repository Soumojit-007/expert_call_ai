// this connect to : GET /api/analysis/compare
// and shows the common themes , agreements,differenceand exper/market informat=ion


import { useState } from "react";
import { GitCompare, Loader2 } from "lucide-react";
import { compareExperts } from "../api";
import type { ComparisonResult } from "../types";

export default function Comparison() {
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleCompare() {
    setLoading(true);
    setError("");

    try {
      const data = await compareExperts();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while comparing the experts."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Intro */}
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex flex-col gap-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-violet-600">
              Cross-Transcript Analysis
            </p>

            <h3 className="mt-1 text-xl font-bold text-slate-900">
              Compare Expert Perspectives
            </h3>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              Identify common themes, areas of agreement, and meaningful
              differences across the France, Germany, and UK interviews.
            </p>
          </div>

          <button
            onClick={handleCompare}
            disabled={loading}
            className="flex shrink-0 items-center justify-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 size={17} className="animate-spin" />
                Comparing...
              </>
            ) : (
              <>
                <GitCompare size={17} />
                Compare Experts
              </>
            )}
          </button>
        </div>
      </section>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Expert cards */}
      {result && (
        <>
          <section>
            <h3 className="mb-4 text-lg font-bold text-slate-900">
              Expert Sources
            </h3>

            <div className="grid gap-4 md:grid-cols-3">
              {result.experts.map((expert) => (
                <div
                  key={expert.market}
                  className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
                >
                  <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-violet-50 text-violet-600">
                    <GitCompare size={19} />
                  </div>

                  <h4 className="font-semibold text-slate-900">
                    {expert.expert}
                  </h4>

                  <p className="mt-1 text-sm text-slate-500">
                    {expert.role}
                  </p>

                  <span className="mt-4 inline-block rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">
                    {expert.market}
                  </span>
                </div>
              ))}
            </div>
          </section>

          {/* Comparison */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-5">
              <p className="text-xs font-semibold uppercase tracking-wider text-violet-600">
                Synthesis
              </p>

              <h3 className="mt-1 text-lg font-bold text-slate-900">
                Cross-Expert Analysis
              </h3>
            </div>

            <div className="whitespace-pre-line text-sm leading-7 text-slate-700">
              {result.comparison}
            </div>
          </section>
        </>
      )}

      {/* Empty state */}
      {!result && !loading && !error && (
        <div className="flex min-h-[300px] items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50">
          <div className="text-center">
            <GitCompare
              size={32}
              className="mx-auto mb-3 text-slate-400"
            />

            <h3 className="font-semibold text-slate-700">
              Ready to compare
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Click "Compare Experts" to analyze all three transcripts.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}