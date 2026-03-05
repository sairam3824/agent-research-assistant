"use client";

import { useState } from "react";
import ProgressFeed from "@/components/ProgressFeed";
import ReportView from "@/components/ReportView";
import ResearchHistory from "@/components/ResearchHistory";
import { API_BASE_URL } from "@/lib/api";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [isResearching, setIsResearching] = useState(false);
  const [progress, setProgress] = useState<string[]>([]);
  const [currentPhase, setCurrentPhase] = useState("");
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string>("");

  const startResearch = async () => {
    if (!question.trim()) return;

    // Add to history
    if ((window as any).addToResearchHistory) {
      (window as any).addToResearchHistory(question);
    }

    setIsResearching(true);
    setProgress([]);
    setReport(null);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, depth: "advanced" }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Failed to get response reader");
      }

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const blocks = buffer.split(/\r?\n\r?\n/);
        buffer = blocks.pop() || "";

        for (const block of blocks) {
          if (!block.trim()) continue;

          try {
            const event = block
              .split(/\r?\n/)
              .find((entry) => entry.startsWith("event:"))
              ?.replace("event:", "")
              .trim();
            const dataText = block
              .split(/\r?\n/)
              .filter((entry) => entry.startsWith("data:"))
              .map((entry) => entry.replace("data:", "").trim())
              .join("\n");

            if (dataText) {
              const data = JSON.parse(dataText);

              if (event === "progress") {
                if (data.phase) setCurrentPhase(data.phase);
                if (data.logs) setProgress(data.logs);
              } else if (event === "complete") {
                setReport(data);
                // Store report ID if available
                if (data.report_id) {
                  sessionStorage.setItem('last_report_id', data.report_id);
                }
              } else if (event === "error") {
                setError(data.error || "An error occurred");
              }
            }
          } catch (parseError) {
            console.warn("Failed to parse SSE block:", block, parseError);
          }
        }
      }
    } catch (error) {
      console.error("Research error:", error);
      setError(error instanceof Error ? error.message : "An unexpected error occurred");
    } finally {
      setIsResearching(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Research Agent
        </h1>
        <p className="text-gray-600 mb-8">
          Autonomous deep research with web search and analysis
        </p>

        <ResearchHistory onSelect={(q) => setQuestion(q)} />

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Research Question
          </label>
          <textarea
            value={question}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setQuestion(e.target.value)}
            placeholder="What would you like to research? e.g., 'What are the latest developments in quantum computing?'"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
            disabled={isResearching}
          />
          <button
            onClick={startResearch}
            disabled={isResearching || !question.trim()}
            className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isResearching ? "Researching..." : "Start Research"}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="text-sm text-red-700 mt-1">{error}</p>
              </div>
              <button
                onClick={() => setError("")}
                className="ml-auto text-red-400 hover:text-red-600"
              >
                ×
              </button>
            </div>
          </div>
        )}

        {(isResearching || progress.length > 0) && (
          <ProgressFeed
            phase={currentPhase}
            logs={progress}
            isActive={isResearching}
          />
        )}

        {report && <ReportView report={report} />}
      </div>
    </main>
  );
}
