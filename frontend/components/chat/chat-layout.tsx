"use client"

import { ChatSidebar } from "./chat-sidebar"
import { ChatHeader } from "./chat-header"
import { MessagesList } from "./messages-list"
import { ChatInput } from "./chat-input"
import type { Message } from "@/types"
import type React from "react"

import { Thread } from "@/types"

interface ChatLayoutProps {
  isSidebarOpen: boolean
  onToggleSidebar: () => void
  messages: Message[]
  threads: Thread[]
  activeThreadId: number | null
  tokenUsage: number
  inputValue: string
  isLoading: boolean
  onInputChange: (value: string) => void
  onSubmit: (e: React.FormEvent) => void
  onNewChat: () => void
  onSelectThread: (threadId: number) => void
  onCopyMessage: (content: string) => void
  onSuggestionClick: (suggestion: string) => void
}

export function ChatLayout({
  isSidebarOpen,
  onToggleSidebar,
  messages,
  threads,
  activeThreadId,
  tokenUsage,
  inputValue,
  isLoading,
  onInputChange,
  onSubmit,
  onNewChat,
  onSelectThread,
  onCopyMessage,
  onSuggestionClick,
}: ChatLayoutProps) {
  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <ChatSidebar
        isOpen={isSidebarOpen}
        messages={messages}
        threads={threads}
        activeThreadId={activeThreadId}
        tokenUsage={tokenUsage}
        onNewChat={onNewChat}
        onSelectThread={onSelectThread}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <ChatHeader tokenUsage={tokenUsage} isSidebarOpen={isSidebarOpen} onToggleSidebar={onToggleSidebar} />

        {/* Messages and Input */}
        <MessagesList messages={messages} onCopyMessage={onCopyMessage} onSuggestionClick={onSuggestionClick} />

        {/* Input */}
        <ChatInput value={inputValue} isLoading={isLoading} onValueChange={onInputChange} onSubmit={onSubmit} />
      </div>
    </div>
  )
}
