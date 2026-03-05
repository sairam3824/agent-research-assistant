"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import ReportView from "@/components/ReportView";
import { API_BASE_URL } from "@/lib/api";

interface LoadedReport {
  id?: string;
  question?: string;
  timestamp?: string;
  report: string;
  critique: any;
  sources: any[];
  findings: any[];
  report_id?: string;
}

export default function SharedReportPage() {
  const params = useParams<{ reportId: string }>();
  const routeId = useMemo(() => {
    const value = params?.reportId;
    return Array.isArray(value) ? value[0] : value;
  }, [params]);

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [report, setReport] = useState<LoadedReport | null>(null);

  useEffect(() => {
    const loadReport = async () => {
      if (!routeId) {
        setError("Missing report ID.");
        setIsLoading(false);
        return;
      }

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/report/${encodeURIComponent(routeId)}`
        );
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        setReport({
          ...data,
          report_id: data.id || routeId,
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load report.");
      } finally {
        setIsLoading(false);
      }
    };

    loadReport();
  }, [routeId]);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <Link href="/" className="text-blue-700 hover:underline text-sm">
            ← Back to Research
          </Link>
        </div>

        {isLoading && (
          <div className="bg-white rounded-lg shadow-lg p-6 text-gray-700">
            Loading report...
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            Failed to load report: {error}
          </div>
        )}

        {report && <ReportView report={report} />}
      </div>
    </main>
  );
}
