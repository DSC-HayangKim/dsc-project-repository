"use client"

import { Send } from "lucide-react"
import { Button } from "@/components/ui/button"
import { CHAT_PLACEHOLDERS } from "@/lib/constants"
import type React from "react"

interface ChatInputProps {
  value: string
  isLoading: boolean
  onValueChange: (value: string) => void
  onSubmit: (e: React.FormEvent) => void
}

export function ChatInput({ value, isLoading, onValueChange, onSubmit }: ChatInputProps) {
  return (
    <div className="border-t border-border bg-background p-4">
      <form onSubmit={onSubmit} className="max-w-5xl mx-auto">
        <div className="flex gap-3 items-end">
          <div className="flex-1">
            <input
              type="text"
              placeholder={CHAT_PLACEHOLDERS.input}
              value={value}
              onChange={(e) => onValueChange(e.target.value)}
              disabled={isLoading}
              className="w-full px-4 py-3 rounded-lg border border-border bg-card text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-500 transition-all disabled:opacity-50"
            />
          </div>
          <Button
            type="submit"
            disabled={isLoading || !value.trim()}
            size="lg"
            className="bg-blue-600 hover:bg-blue-700 text-white px-4"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </form>
    </div>
  )
}
