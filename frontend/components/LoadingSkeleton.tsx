export default function LoadingSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mb-6 animate-pulse">
      <div className="flex items-center justify-between mb-4">
        <div className="h-6 bg-gray-200 rounded w-48"></div>
        <div className="h-4 bg-gray-200 rounded w-24"></div>
      </div>
      
      <div className="space-y-3">
        <div className="h-4 bg-gray-200 rounded w-full"></div>
        <div className="h-4 bg-gray-200 rounded w-5/6"></div>
        <div className="h-4 bg-gray-200 rounded w-4/6"></div>
      </div>
    </div>
  );
}
