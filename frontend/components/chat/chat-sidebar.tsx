"use client"

import { Plus } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { SIDEBAR_LABELS } from "@/lib/constants"
import type { Message } from "@/types"

interface ChatSidebarProps {
  isOpen: boolean
  messages: Message[]
  tokenUsage: number
  onNewChat: () => void
}

export function ChatSidebar({ isOpen, messages, tokenUsage, onNewChat }: ChatSidebarProps) {
  return (
    <div
      className={`${
        isOpen ? "w-64" : "w-0"
      } bg-muted/50 border-r border-border transition-all duration-300 flex flex-col overflow-hidden`}
    >
      {/* Sidebar Header */}
      <div className="p-4 border-b border-border flex items-center justify-between">
        <span className="text-sm font-semibold text-foreground">Patent AI</span>
      </div>

      {/* New Chat Button */}
      <button
        onClick={onNewChat}
        className="m-4 px-4 py-2 rounded-lg border border-border hover:bg-background/80 transition-colors flex items-center justify-center gap-2 text-sm font-medium text-foreground"
      >
        <Plus className="h-4 w-4" />
        {SIDEBAR_LABELS.newChat}
      </button>

      {/* Recent Chats */}
      <div className="flex-1 overflow-y-auto px-4 space-y-2">
        <div className="text-xs text-muted-foreground px-2 py-2 font-semibold uppercase tracking-wider">
          {SIDEBAR_LABELS.recentChats}
        </div>
        {messages.length > 0 && (
          <div className="p-3 rounded-lg bg-background/50 border border-border cursor-pointer hover:bg-background transition-colors">
            <div className="text-sm text-foreground truncate font-medium">
              {messages[0]?.content?.substring(0, 30)}...
            </div>
            <div className="text-xs text-muted-foreground">방금 전</div>
          </div>
        )}
      </div>

      {/* Token Usage */}
      <div className="p-4 border-t border-border space-y-2">
        <div className="text-xs text-muted-foreground uppercase tracking-wider font-semibold">
          {SIDEBAR_LABELS.tokenUsage}
        </div>
        <div className="text-2xl font-bold text-blue-600">{tokenUsage}</div>
        <Link href="/#pricing">
          <Button variant="outline" className="w-full bg-transparent text-sm" size="sm">
            {SIDEBAR_LABELS.chargeToken}
          </Button>
        </Link>
      </div>
    </div>
  )
}
