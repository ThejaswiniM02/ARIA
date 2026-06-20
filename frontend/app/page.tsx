"use client";
import { useState } from "react";
import QueryInput from "@/components/QueryInput";
import AgentPipeline from "@/components/AgentPipeline";
import ReportView from "@/components/ReportView";
import HistorySidebar from "@/components/HistorySidebar";

type Step = "idle" | "research" | "analysis" | "comparison" | "writer" | "done";

export default function Home() {
  const [report, setReport] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<Step>("idle");
  const [historyKey, setHistoryKey] = useState(0);
  const [viewingPast, setViewingPast] = useState(false);
  const [historyOpen, setHistoryOpen] = useState(false);

  const handleQuery = async (query: string, mode: string) => {
    setLoading(true);
    setReport("");
    setStep("research");
    setViewingPast(false);

    const fakeProgress = setTimeout(() => setStep("analysis"), 1800);
    const fakeProgress2 = setTimeout(() => setStep("comparison"), 3600);
    const fakeProgress3 = setTimeout(() => setStep("writer"), 5400);

    try {
      const res = await fetch("https://aria-9ptz.onrender.com/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, mode }),
      });

      const data = await res.json();
      setReport(data.report);
      setSources(data.sources || []);
      setStep("done");
      setHistoryKey((k) => k + 1);
    } catch (err) {
      setReport("Something went wrong reaching the backend. Is FastAPI running on port 8000?");
      setStep("done");
    } finally {
      clearTimeout(fakeProgress);
      clearTimeout(fakeProgress2);
      clearTimeout(fakeProgress3);
      setLoading(false);
    }
  };

  const handleSelectHistory = async (id: string) => {
    setLoading(true);
    try {
      const res = await fetch(`https://aria-9ptz.onrender.com/research/${id}`);
      const data = await res.json();
      setReport(data.report);
      setSources(data.sources || []);
      setStep("done");
      setViewingPast(true);
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setReport("");
    setSources([]);
    setStep("idle");
    setViewingPast(false);
  };

  return (
    <main>
      <div className="flex items-center justify-between px-10 py-5 border-b-2 border-ink">
        <div className="flex items-center gap-2.5 font-display font-bold text-[22px]">
          <span
            className="w-3.5 h-3.5 rounded-full"
            style={{
              background:
                "conic-gradient(from 0deg, #FF6B5B, #7C5CFF, #3DD9B3, #FFC94A, #FF6B5B)",
            }}
          />
          ARIA
        </div>

        <div className="flex items-center gap-5">
          <div className="text-[13px] opacity-55 font-medium hidden sm:block">
            Autonomous Research Intelligence Agent
          </div>
          <button
            onClick={() => setHistoryOpen(true)}
            className="font-display font-semibold text-sm px-4 py-2 border-2 border-ink rounded-xl bg-yellow shadow-hard-sm hover:-translate-y-0.5 transition-transform"
          >
            History
          </button>
        </div>
      </div>

      <HistorySidebar
        onSelect={handleSelectHistory}
        refreshKey={historyKey}
        open={historyOpen}
        setOpen={setHistoryOpen}
      />

      <div className="max-w-[1100px] mx-auto px-8 py-12">
        {viewingPast ? (
          <button
            onClick={handleBack}
            className="font-display font-semibold text-sm mb-6 flex items-center gap-1 opacity-70 hover:opacity-100 transition-opacity"
          >
            ← Back to new search
          </button>
        ) : (
          <>
            <h1 className="font-display font-bold text-[42px] leading-tight mb-2 -tracking-[0.01em]">
              Ask something worth researching.
            </h1>
            <p className="text-base opacity-65 mb-9 max-w-[560px]">
              Four agents go to work: one researches, one analyzes, one compares, one writes the report.
            </p>

            <AgentPipeline currentStep={step} />

            <QueryInput onSubmit={handleQuery} loading={loading} />
          </>
        )}

        {report && <ReportView report={report} sources={sources} />}
      </div>
   </main>
  );
}