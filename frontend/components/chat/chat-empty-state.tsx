"use client"

import { CHAT_EMPTY_STATE, CHAT_SUGGESTIONS } from "@/lib/constants"

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void
}

export function ChatEmptyState({ onSuggestionClick }: ChatEmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 flex items-center justify-center mb-6">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600" />
      </div>
      <h2 className="text-2xl font-bold text-foreground mb-2">{CHAT_EMPTY_STATE.title}</h2>
      <p className="text-muted-foreground max-w-md mb-8">{CHAT_EMPTY_STATE.description}</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-md">
        {CHAT_SUGGESTIONS.map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => onSuggestionClick(suggestion)}
            className="text-left p-3 rounded-lg border border-border hover:bg-muted hover:border-blue-500 transition-colors text-sm font-medium text-foreground"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </div>
  )
}
