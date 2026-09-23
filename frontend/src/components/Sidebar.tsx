// this will be the left navigation panel


import {
  MessageSquareText,
  GitCompare,
  Sparkles,
  FileText,
} from "lucide-react";

interface SidebarProps {
  activePage: string;
  setActivePage: (page: string) => void;
}

export default function Sidebar({
  activePage,
  setActivePage,
}: SidebarProps) {
  const menuItems = [
    {
      id: "interview",
      label: "Interview Guide",
      icon: MessageSquareText,
    },
    {
      id: "comparison",
      label: "Compare Experts",
      icon: GitCompare,
    },
    {
      id: "ask",
      label: "Ask AI",
      icon: Sparkles,
    },
  ];

  return (
    <aside className="flex min-h-screen w-64 flex-col border-r border-slate-200 bg-white">
      {/* Logo */}
      <div className="border-b border-slate-200 px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-600 text-white">
            <FileText size={20} />
          </div>

          <div>
            <h1 className="text-lg font-bold text-slate-900">
              ExpertLens
            </h1>
            <p className="text-xs text-slate-500">
              Expert Call Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Analysis
        </p>

        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setActivePage(item.id)}
                className={`flex w-full items-center gap-3 rounded-lg px-3 py-3 text-left text-sm font-medium transition ${
                  isActive
                    ? "bg-violet-50 text-violet-700"
                    : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
                }`}
              >
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </div>
      </nav>

      {/* Sources status */}
      <div className="border-t border-slate-200 p-4">
        <div className="rounded-xl bg-slate-50 p-4">
          <div className="mb-2 flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />

            <span className="text-sm font-semibold text-slate-800">
              Sources Ready
            </span>
          </div>

          <p className="text-xs leading-5 text-slate-500">
            3 expert transcripts
            <br />
            France · Germany · UK
          </p>
        </div>
      </div>
    </aside>
  );
}