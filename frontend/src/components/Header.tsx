// this gives a reuseable header


import { ShieldCheck } from "lucide-react";

interface HeaderProps {
  title: string;
  description: string;
}

export default function Header({
  title,
  description,
}: HeaderProps) {
  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-8 py-5">
      <div>
        <h2 className="text-2xl font-bold text-slate-900">
          {title}
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>

      <div className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-2">
        <ShieldCheck size={16} className="text-emerald-600" />

        <span className="text-xs font-semibold text-emerald-700">
          Grounded in transcripts
        </span>
      </div>
    </header>
  );
}