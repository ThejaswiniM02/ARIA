"use client";
import { useEffect, useState } from "react";

type HistoryItem = {
  id: string;
  query: string;
  created_at: string;
};

export default function HistorySidebar({
  onSelect,
  refreshKey,
  open,
  setOpen,
}: {
  onSelect: (id: string) => void;
  refreshKey: number;
  open: boolean;
  setOpen: (v: boolean) => void;
}) {
  const [items, setItems] = useState<HistoryItem[]>([]);

  useEffect(() => {
    fetch("https://aria-9ptz.onrender.com/history")
      .then((res) => res.json())
      .then((data) => setItems(data.items || []))
      .catch(() => setItems([]));
  }, [refreshKey]);

  if (!open) return null;

  return (
    <>
      <div
        className="fixed inset-0 bg-ink/20 z-10"
        onClick={() => setOpen(false)}
      />
      <div className="fixed top-0 right-0 h-full w-80 bg-white border-l-2 border-ink shadow-2xl z-20 pt-8 px-5 overflow-y-auto">
        <div className="flex items-center justify-between mb-5">
          <h3 className="font-display font-bold text-lg">Past research</h3>
          <button
            onClick={() => setOpen(false)}
            className="w-8 h-8 flex items-center justify-center border-2 border-ink rounded-lg hover:bg-ink hover:text-white transition-colors font-display font-bold"
          >
            ×
          </button>
        </div>
        {items.length === 0 && (
          <p className="text-sm opacity-50">Nothing yet — run a query to start building history.</p>
        )}
        <div className="flex flex-col gap-2">
          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                onSelect(item.id);
                setOpen(false);
              }}
              className="text-left text-sm p-3 border-2 border-ink/15 rounded-xl hover:border-violet hover:bg-violet/5 transition-colors"
            >
              <div className="font-medium line-clamp-2">{item.query}</div>
              <div className="text-xs opacity-40 mt-1">
                   {new Date(item.created_at).toLocaleDateString()}
             </div>
            </button>
          ))}
        </div>
      </div>
    </>
  );
}