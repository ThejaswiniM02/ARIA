"use client";
import { useState } from "react";

export default function QueryInput({
  onSubmit,
  loading,
}: {
  onSubmit: (q: string, mode: string) => void;
  loading: boolean;
}) {
  const [query, setQuery] = useState("");
  const [academic, setAcademic] = useState(false);

  const submit = () => {
    if (query.trim()) onSubmit(query, academic ? "academic" : "web");
  };

  return (
    <div className="mb-2">
      <div className="flex items-center gap-3 mb-3">
        <button
          onClick={() => setAcademic(!academic)}
          className={`flex items-center gap-2 font-display font-semibold text-xs px-3 py-1.5 rounded-full border-2 border-ink transition-colors ${
            academic ? "bg-violet text-white" : "bg-white text-ink"
          }`}
        >
          <span
            className={`w-2 h-2 rounded-full ${academic ? "bg-white" : "bg-ink/20"}`}
          />
          Academic mode
        </button>
        <span className="text-xs opacity-45">
          {academic ? "Searching Semantic Scholar + arXiv" : "Searching the general web"}
        </span>
      </div>

      <div className="flex gap-3">
        <input
          className="flex-1 font-body text-base px-5 py-4 border-2 border-ink rounded-2xl bg-white outline-none focus:shadow-hard-sm transition-shadow"
          placeholder={
            academic
              ? "e.g. Effects of early waking on cognitive performance"
              : "e.g. Compare UK scholarships for Indian students"
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !loading && submit()}
        />
        <button
          className="font-display font-bold text-[15px] px-7 border-2 border-ink rounded-2xl bg-coral text-ink shadow-hard-sm hover:-translate-x-0.5 hover:-translate-y-0.5 hover:shadow-hard active:translate-x-0 active:translate-y-0 active:shadow-none transition-all disabled:opacity-50 disabled:pointer-events-none"
          onClick={submit}
          disabled={loading || !query.trim()}
        >
          {loading ? "Researching…" : "Research →"}
        </button>
      </div>
      <p className="text-[13px] opacity-45 mt-3 ml-1">
        {academic
          ? 'Try: "Sleep deprivation effects on memory consolidation"'
          : 'Try: "Best AI internship platforms for students"'}
      </p>
    </div>
  );
}