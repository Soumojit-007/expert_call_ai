// This is the resuable component that displays the most important evidence from the transcripts



import type { Evidence } from "../types";
interface EvidenceCardProps {
  evidence: Evidence;
}

export default function EvidenceCard({ evidence }: EvidenceCardProps) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md">
      {/* Expert information */}
      <div className="mb-4 flex flex-wrap items-start justify-between gap-3">
        <div>
          <h3 className="font-semibold text-slate-900">
            {evidence.expert}
          </h3>

          <p className="text-sm text-slate-500">
            {evidence.role}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="rounded-full bg-violet-50 px-3 py-1 text-xs font-medium text-violet-700">
            {evidence.market}
          </span>

          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            {evidence.timestamp}
          </span>
        </div>
      </div>

      {/* Speaker */}
      <div className="mb-3 text-xs font-medium uppercase tracking-wide text-slate-400">
        {evidence.speaker}
      </div>

      {/* Exact quote */}
      <div className="border-l-4 border-violet-500 bg-slate-50 px-4 py-3">
        <p className="text-sm leading-6 text-slate-700">
          "{evidence.quote}"
        </p>
      </div>
    </div>
  );
}