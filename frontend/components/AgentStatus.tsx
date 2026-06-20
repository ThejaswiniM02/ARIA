const steps = ["Research Agent", "Analysis Agent", "Comparison Agent", "Writer Agent"];

export default function AgentStatus({ status }: { status: string }) {
  return (
    <div className="mb-6 p-4 bg-gray-50 rounded-lg">
      <p className="text-sm text-gray-500 mb-3">Agents running...</p>
      <div className="flex gap-4">
        {steps.map((s) => (
          <div key={s} className="flex items-center gap-2 text-sm">
            <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            {s}
          </div>
        ))}
      </div>
    </div>
  );
}