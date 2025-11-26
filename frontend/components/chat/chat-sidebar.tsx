"use client"

import { Plus, Lightbulb } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { SIDEBAR_LABELS } from "@/lib/constants"
import { Thread, Message } from "@/types"
import { format } from "date-fns"
import { ko } from "date-fns/locale"

interface ChatSidebarProps {
  isOpen: boolean
  messages: Message[] // Keep for backward compatibility if needed, or remove if unused
  threads: Thread[]
  activeThreadId: number | null
  tokenUsage: number
  onNewChat: () => void
  onSelectThread: (threadId: number) => void
}

export function ChatSidebar({
  isOpen,
  messages,
  threads,
  activeThreadId,
  tokenUsage,
  onNewChat,
  onSelectThread
}: ChatSidebarProps) {
  return (
    <div
      className={`${isOpen ? "w-64" : "w-0"
        } bg-violet-50 border-r border-violet-100 transition-all duration-300 flex flex-col overflow-hidden`}
    >
      {/* Sidebar Header */}
      <div className="p-4 border-b border-violet-100 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <Lightbulb className="h-6 w-6 text-blue-400" />
          <span className="text-lg font-bold text-violet-900">Patent AI</span>
        </Link>
      </div>

      {/* New Chat Button */}
      <button
        onClick={onNewChat}
        className="m-4 px-4 py-2 rounded-lg border border-violet-100 bg-white hover:bg-violet-100 transition-colors flex items-center justify-center gap-2 text-sm font-medium text-violet-900"
      >
        <Plus className="h-4 w-4" />
        {SIDEBAR_LABELS.newChat}
      </button>

      {/* Recent Chats */}
      <div className="flex-1 overflow-y-auto px-4 space-y-2">
        <div className="text-xs text-violet-500 px-2 py-2 font-semibold uppercase tracking-wider">
          {SIDEBAR_LABELS.recentChats}
        </div>
        {threads.map((thread) => (
          <div
            key={thread.id}
            onClick={() => onSelectThread(thread.id)}
            className={`p-3 rounded-lg border cursor-pointer transition-colors ${activeThreadId === thread.id
              ? "bg-violet-200 border-violet-300"
              : "bg-white/60 border-violet-100 hover:bg-violet-100"
              }`}
          >
            <div className="text-sm text-violet-900 truncate font-medium">
              {thread.title || "새로운 대화"}
            </div>
            <div className="text-xs text-violet-400">
              {format(new Date(thread.created_at), "M월 d일 a h:mm", { locale: ko })}
            </div>
          </div>
        ))}
      </div>

      {/* Token Usage */}
      <div className="p-4 border-t border-violet-200 space-y-2">
        <div className="text-xs text-violet-500 uppercase tracking-wider font-semibold">
          {SIDEBAR_LABELS.tokenUsage}
        </div>
        <div className="text-2xl font-bold text-violet-600">{tokenUsage}</div>
        <Link href="/#pricing">
          <Button variant="outline" className="w-full bg-white border-violet-200 text-violet-700 hover:bg-violet-50" size="sm">
            {SIDEBAR_LABELS.chargeToken}
          </Button>
        </Link>
      </div>
    </div>
  )
}
