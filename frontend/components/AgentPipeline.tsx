"use client";

type AgentKey = "research" | "analysis" | "comparison" | "writer";

const AGENTS: { key: AgentKey; label: string; icon: string }[] = [
  { key: "research", label: "Research", icon: "①" },
  { key: "analysis", label: "Analysis", icon: "②" },
  { key: "comparison", label: "Comparison", icon: "③" },
  { key: "writer", label: "Writer", icon: "④" },
];

const COLORS: Record<AgentKey, string> = {
  research: "bg-coral",
  analysis: "bg-violet",
  comparison: "bg-yellow",
  writer: "bg-mint",
};

export default function AgentPipeline({ currentStep }: { currentStep: AgentKey | "idle" | "done" }) {
  const order: AgentKey[] = ["research", "analysis", "comparison", "writer"];
  const currentIndex = currentStep === "idle" ? -1 : currentStep === "done" ? order.length : order.indexOf(currentStep as AgentKey);

  return (
    <div className="flex items-center bg-white border-2 border-ink rounded-2xl px-7 py-5 shadow-hard mb-9">
      {AGENTS.map((agent, i) => {
        const isDone = currentIndex > i;
        const isActive = currentIndex === i;
        const state = isDone ? "done" : isActive ? "working…" : "waiting";

        return (
          <div className="flex items-center flex-1 last:flex-none" key={agent.key}>
            <div className="flex flex-col items-center gap-2 flex-1">
              <div
                className={`w-12 h-12 rounded-full border-[2.5px] border-ink flex items-center justify-center text-lg transition-all duration-300
                  ${isDone || isActive ? `${COLORS[agent.key]} text-ink` : "bg-paper text-ink"}
                  ${isActive ? "scale-110 ring-4 ring-offset-0" : ""}
                `}
                style={isActive ? { boxShadow: `0 0 0 6px rgba(0,0,0,0.06)` } : {}}
              >
                {agent.icon}
              </div>
              <div className="font-display font-semibold text-[13px] text-center">{agent.label}</div>
              <div className="text-[11px] opacity-50 h-3.5">{state}</div>
            </div>

            {i < AGENTS.length - 1 && (
              <div className="h-[3px] flex-1 bg-ink/10 rounded mx-1 mb-[26px] relative overflow-hidden">
                <div
                  className="absolute inset-0 bg-gradient-to-r from-coral via-violet to-mint transition-all duration-500"
                  style={{ width: isDone ? "100%" : isActive ? "40%" : "0%" }}
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}