// this shows the 6 interview qs
// let u select all/france/germany/uk\
// call your fastapi
// display the grounded answer
// display exact evidence with timestamps


import { useState } from "react";
import { Loader2, Search } from "lucide-react";
import { analyzeQuestion } from "../api";
import type { AnalysisResult } from "../types";
import EvidenceCard from "./EvidenceCard";

const questions = [
  "How would you describe current adoption of robotic surgery in your market?",
  "What are the main barriers to adoption?",
  "How important are hospital budgets and ROI in purchasing decisions?",
  "How important are surgeon training and clinical outcomes?",
  "What adoption trend do you expect over the next 3–5 years?",
  "What is the typical hospital decision-making timeline for purchasing a new robotic system?",
];

const markets = ["All Markets", "France", "Germany", "United Kingdom"];

export default function InterviewGuide() {
  const [selectedQuestion, setSelectedQuestion] = useState(questions[0]);
  const [selectedMarket, setSelectedMarket] = useState("All Markets");

  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const market =
        selectedMarket === "All Markets" ? undefined : selectedMarket;

      const data = await analyzeQuestion(selectedQuestion, market);

      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while analyzing the question."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Controls */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Market */}
        <div>
          <label className="mb-2 block text-sm font-semibold text-slate-700">
            Market
          </label>

          <select
            value={selectedMarket}
            onChange={(e) => setSelectedMarket(e.target.value)}
            className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-100"
          >
            {markets.map((market) => (
              <option key={market} value={market}>
                {market}
              </option>
            ))}
          </select>
        </div>

        {/* Question */}
        <div>
          <label className="mb-2 block text-sm font-semibold text-slate-700">
            Interview Question
          </label>

          <select
            value={selectedQuestion}
            onChange={(e) => setSelectedQuestion(e.target.value)}
            className="w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm text-slate-700 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-100"
          >
            {questions.map((question, index) => (
              <option key={question} value={question}>
                Q{index + 1} — {question}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Analyze button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="flex items-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {loading ? (
          <>
            <Loader2 size={17} className="animate-spin" />
            Analyzing...
          </>
        ) : (
          <>
            <Search size={17} />
            Analyze Question
          </>
        )}
      </button>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-6">
          {/* Answer */}
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-violet-600">
                AI Analysis
              </p>

              <h3 className="mt-1 text-lg font-bold text-slate-900">
                {result.question}
              </h3>
            </div>

            <div className="whitespace-pre-line text-sm leading-7 text-slate-700">
              {result.answer}
            </div>
          </section>

          {/* Evidence */}
          <section>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-slate-900">
                  Supporting Evidence
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Exact transcript excerpts used to generate the answer.
                </p>
              </div>

              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600">
                {result.evidence.length} sources
              </span>
            </div>

            <div className="space-y-4">
              {result.evidence.map((evidence, index) => (
                <EvidenceCard
                  key={`${evidence.market}-${evidence.timestamp}-${index}`}
                  evidence={evidence}
                />
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}