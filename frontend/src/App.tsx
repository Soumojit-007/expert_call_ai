// this is going to connect sidebar , header and all other three pages


import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import InterviewGuide from "./components/InterviewGuide";
import Comparison from "./components/Comparison";
import AskAI from "./components/AskAI";

const pageConfig = {
  interview: {
    title: "Interview Guide",
    description:
      "Analyze expert responses against the six interview questions.",
  },
  comparison: {
    title: "Compare Experts",
    description:
      "Identify common themes and differences across expert interviews.",
  },
  ask: {
    title: "Ask AI",
    description:
      "Ask questions across all three expert transcripts.",
  },
};

export default function App() {
  const [activePage, setActivePage] = useState("interview");

  const currentPage =
    pageConfig[activePage as keyof typeof pageConfig];

  return (
    <div className="flex min-h-screen bg-slate-50">
      {/* Sidebar */}
      <Sidebar
        activePage={activePage}
        setActivePage={setActivePage}
      />

      {/* Main content */}
      <main className="min-w-0 flex-1">
        <Header
          title={currentPage.title}
          description={currentPage.description}
        />

        <div className="p-8">
          {activePage === "interview" && <InterviewGuide />}

          {activePage === "comparison" && <Comparison />}

          {activePage === "ask" && <AskAI />}
        </div>
      </main>
    </div>
  );
}