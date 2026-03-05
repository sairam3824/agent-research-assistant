"use client";

import { useState, useEffect } from "react";

interface HistoryItem {
  id: string;
  question: string;
  timestamp: number;
}

interface ResearchHistoryProps {
  onSelect: (question: string) => void;
}

export default function ResearchHistory({ onSelect }: ResearchHistoryProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("research_history");
    if (saved) {
      setHistory(JSON.parse(saved));
    }
  }, []);

  const addToHistory = (question: string) => {
    const newItem: HistoryItem = {
      id: Date.now().toString(),
      question,
      timestamp: Date.now(),
    };
    setHistory((prevHistory) => {
      const updated = [newItem, ...prevHistory].slice(0, 10); // Keep last 10
      localStorage.setItem("research_history", JSON.stringify(updated));
      return updated;
    });
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem("research_history");
  };

  // Expose addToHistory for parent component
  useEffect(() => {
    (window as any).addToResearchHistory = addToHistory;
  }, []);

  if (history.length === 0) return null;

  return (
    <div className="mb-6">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="text-sm text-gray-600 hover:text-gray-900 flex items-center gap-2"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        Recent Searches ({history.length})
      </button>

      {isOpen && (
        <div className="mt-2 bg-white rounded-lg shadow-lg border border-gray-200 p-4">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-medium text-gray-900">Recent Searches</h3>
            <button
              onClick={clearHistory}
              className="text-xs text-red-600 hover:text-red-800"
            >
              Clear All
            </button>
          </div>
          <div className="space-y-2">
            {history.map((item: HistoryItem) => (
              <button
                key={item.id}
                onClick={() => {
                  onSelect(item.question);
                  setIsOpen(false);
                }}
                className="w-full text-left p-2 hover:bg-gray-50 rounded text-sm text-gray-700 border border-gray-100"
              >
                <div className="truncate">{item.question}</div>
                <div className="text-xs text-gray-400 mt-1">
                  {new Date(item.timestamp).toLocaleDateString()}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
