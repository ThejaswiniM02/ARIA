import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
export default function ReportView({
  report,
  sources,
}: {
  report: string;
  sources: string[];
}) {
  return (
    <div className="bg-white border-2 border-ink rounded-2xl p-9 shadow-hard mt-10">
      <span className="inline-block font-display font-semibold text-xs px-3 py-1 rounded-full bg-mint border-2 border-ink mb-5">
        Report ready
      </span>

      <div className="prose max-w-none prose-headings:font-display">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{report}</ReactMarkdown>
      </div>

      {sources.length > 0 && (
        <div className="mt-7 pt-5 border-t-2 border-dashed border-ink/10">
          <h3 className="font-display text-sm mb-3">Sources</h3>
          <ul className="text-sm space-y-1.5">
            {sources.map((s, i) => (
              <li key={i}><a href={s} target="_blank" rel="noopener noreferrer" className="text-violet break-all hover:underline">{s}</a></li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}