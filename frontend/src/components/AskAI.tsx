//  this is the cross-transcript q&a screen.It sends the users question to POST /api/chat/


import { useState } from "react";
import { Loader2, Send, Sparkles } from "lucide-react";
import { askAI } from "../api";
import type { ChatResult } from "../types";
import EvidenceCard from "./EvidenceCard";

export default function AskAI() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<ChatResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk() {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await askAI(question.trim());
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while asking the AI."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleAsk();
    }
  }

  return (
    <div className="space-y-6">
      {/* Ask AI panel */}
      <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-6 text-center">
          <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-violet-50 text-violet-600">
            <Sparkles size={24} />
          </div>

          <h3 className="text-xl font-bold text-slate-900">
            Ask Across All Experts
          </h3>

          <p className="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-500">
            Ask a question about the robotic surgery market and get an
            answer grounded in the three expert transcripts.
          </p>
        </div>

        <div className="mx-auto max-w-3xl">
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. What are the biggest barriers to robotic surgery adoption?"
            rows={4}
            className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-violet-500 focus:bg-white focus:ring-2 focus:ring-violet-100"
          />

          <div className="mt-3 flex items-center justify-between">
            <p className="text-xs text-slate-400">
              Press Enter to ask · Shift + Enter for a new line
            </p>

            <button
              onClick={handleAsk}
              disabled={loading || !question.trim()}
              className="flex items-center gap-2 rounded-xl bg-violet-600 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-violet-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 size={17} className="animate-spin" />
                  Thinking...
                </>
              ) : (
                <>
                  <Send size={17} />
                  Ask AI
                </>
              )}
            </button>
          </div>
        </div>
      </section>

      {/* Error */}
      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Answer */}
      {result && (
        <section className="space-y-6">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center gap-2">
              <Sparkles size={18} className="text-violet-600" />

              <h3 className="font-bold text-slate-900">
                AI Answer
              </h3>
            </div>

            <div className="whitespace-pre-line text-sm leading-7 text-slate-700">
              {result.answer}
            </div>
          </div>

          {/* Evidence */}
          <div>
            <div className="mb-4">
              <h3 className="text-lg font-bold text-slate-900">
                Supporting Evidence
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Retrieved transcript excerpts supporting the answer.
              </p>
            </div>

            <div className="space-y-4">
              {result.evidence.map((evidence, index) => (
                <EvidenceCard
                  key={`${evidence.market}-${evidence.timestamp}-${index}`}
                  evidence={evidence}
                />
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}