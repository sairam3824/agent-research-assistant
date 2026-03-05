"use client";

import { useState } from "react";

interface CitationPopoverProps {
  number: number;
  source: {
    title: string;
    url: string;
    credibility_score: number;
    date?: string;
  };
}

export default function CitationPopover({ number, source }: CitationPopoverProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <span className="relative inline-block">
      <button
        onMouseEnter={() => setIsOpen(true)}
        onMouseLeave={() => setIsOpen(false)}
        className="text-blue-600 hover:text-blue-800 font-medium cursor-pointer"
      >
        [{number}]
      </button>
      
      {isOpen && (
        <div className="absolute z-10 w-80 p-4 bg-white border border-gray-200 rounded-lg shadow-lg bottom-full left-0 mb-2">
          <h4 className="font-semibold text-sm text-gray-900 mb-2">{source.title}</h4>
          <a
            href={source.url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-600 hover:underline block mb-2 break-all"
          >
            {source.url}
          </a>
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Credibility: {(source.credibility_score * 100).toFixed(0)}%</span>
            {source.date && <span>{source.date}</span>}
          </div>
        </div>
      )}
    </span>
  );
}
