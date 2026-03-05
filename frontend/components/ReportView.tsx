"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import ShareButton from "./ShareButton";

interface ReportViewProps {
  report: {
    report: string;
    critique: any;
    sources: any[];
    findings: any[];
    report_id?: string;
  };
}

export default function ReportView({ report }: ReportViewProps) {
  const [activeTab, setActiveTab] = useState<"report" | "sources" | "critique" | "findings">("report");

  const downloadMarkdown = () => {
    const blob = new Blob([report.report], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `research-report-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(report.report);
    alert("Report copied to clipboard!");
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="border-b border-gray-200">
        <div className="flex space-x-4 px-6">
          <button
            onClick={() => setActiveTab("report")}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              activeTab === "report"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Report
          </button>
          <button
            onClick={() => setActiveTab("findings")}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              activeTab === "findings"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Findings ({report.findings?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab("sources")}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              activeTab === "sources"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Sources ({report.sources?.length || 0})
          </button>
          <button
            onClick={() => setActiveTab("critique")}
            className={`py-4 px-2 border-b-2 font-medium text-sm ${
              activeTab === "critique"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            Quality Review
          </button>
        </div>
      </div>

      <div className="p-6">
        {activeTab === "report" && (
          <div>
            <div className="flex justify-end gap-2 mb-4">
              <ShareButton reportId={report.report_id} />
              <button
                onClick={copyToClipboard}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 text-sm"
              >
                Copy to Clipboard
              </button>
              <button
                onClick={downloadMarkdown}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                Download Markdown
              </button>
            </div>
            <div className="prose max-w-none prose-headings:text-gray-900 prose-p:text-gray-700 prose-a:text-blue-600">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {report.report}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {activeTab === "findings" && (
          <div className="space-y-4">
            {report.findings?.length > 0 ? (
              report.findings.map((finding, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900 flex-1">{finding.claim}</h3>
                    <span className={`ml-4 px-2 py-1 text-xs rounded ${
                      finding.confidence > 0.7 
                        ? "bg-green-100 text-green-800" 
                        : finding.confidence > 0.5 
                        ? "bg-yellow-100 text-yellow-800" 
                        : "bg-red-100 text-red-800"
                    }`}>
                      {(finding.confidence * 100).toFixed(0)}% confidence
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-2">
                    Sub-question: {finding.sub_question}
                  </p>
                  <div className="text-xs text-gray-500">
                    {finding.sources?.length || 0} sources
                  </div>
                </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No findings available</p>
            )}
          </div>
        )}

        {activeTab === "sources" && (
          <div className="space-y-4">
            {report.sources && report.sources.length > 0 ? (
              report.sources.map((source, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{source.title}</h3>
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-blue-600 hover:underline"
                    >
                      {source.url}
                    </a>
                    <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                      <span>Credibility: {(source.credibility_score * 100).toFixed(0)}%</span>
                      {source.date && <span>Date: {source.date}</span>}
                    </div>
                  </div>
                </div>
              </div>
              ))
            ) : (
              <p className="text-gray-500 text-center py-8">No sources available</p>
            )}
          </div>
        )}

        {activeTab === "critique" && (
          <div className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="font-semibold text-gray-900 mb-2">Quality Score</h3>
              <div className="text-3xl font-bold text-blue-600">
                {((report.critique?.quality_score || 0) * 100).toFixed(0)}%
              </div>
            </div>

            {report.critique?.strengths && report.critique.strengths.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Strengths</h3>
                <ul className="list-disc list-inside space-y-1">
                  {report.critique.strengths.map((s: string, i: number) => (
                    <li key={i} className="text-gray-700">{s}</li>
                  ))}
                </ul>
              </div>
            )}

            {report.critique?.weaknesses && report.critique.weaknesses.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Weaknesses</h3>
                <ul className="list-disc list-inside space-y-1">
                  {report.critique.weaknesses.map((s: string, i: number) => (
                    <li key={i} className="text-gray-700">{s}</li>
                  ))}
                </ul>
              </div>
            )}

            {report.critique?.suggestions && report.critique.suggestions.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Suggestions</h3>
                <ul className="list-disc list-inside space-y-1">
                  {report.critique.suggestions.map((s: string, i: number) => (
                    <li key={i} className="text-gray-700">{s}</li>
                  ))}
                </ul>
              </div>
            )}

            {report.critique?.bias_assessment && (
              <div>
                <h3 className="font-semibold text-gray-900 mb-2">Bias Assessment</h3>
                <p className="text-gray-700">{report.critique.bias_assessment}</p>
              </div>
            )}

            {!report.critique && (
              <p className="text-gray-500 text-center py-8">No quality review available</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
