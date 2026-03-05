interface ProgressFeedProps {
  phase: string;
  logs: string[];
  isActive: boolean;
}

export default function ProgressFeed({ phase, logs, isActive }: ProgressFeedProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Research Progress</h2>
        {isActive && (
          <div className="flex items-center space-x-2">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
            <span className="text-sm text-blue-600 font-medium">{phase}</span>
          </div>
        )}
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {logs.map((log, index) => (
          <div
            key={index}
            className="text-sm text-gray-700 py-1 px-3 bg-gray-50 rounded border-l-2 border-blue-400"
          >
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}
