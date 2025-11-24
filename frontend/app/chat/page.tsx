"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { ChatLayout } from "@/components/chat/chat-layout"
import { Message, Thread } from "@/types"
import { fetchThreads, createThread, fetchMessages, sendMessage } from "@/lib/api"

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [threads, setThreads] = useState<Thread[]>([])
  const [activeThreadId, setActiveThreadId] = useState<number | null>(null)
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [tokenUsage, setTokenUsage] = useState(0)

  useEffect(() => {
    loadThreads()
  }, [])

  const loadThreads = async () => {
    try {
      const data = await fetchThreads()
      setThreads(data)
    } catch (error) {
      console.error("Failed to load threads:", error)
    }
  }

  const handleSelectThread = async (threadId: number) => {
    setActiveThreadId(threadId)
    setIsLoading(true)
    try {
      const msgs = await fetchMessages(threadId)
      setMessages(msgs)
    } catch (error) {
      console.error("Failed to load messages:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue,
    }

    setInputValue("")
    setIsLoading(true)

    const assistantMessage: Message = {
      id: (Date.now() + 1).toString(),
      role: "assistant",
      content: "",
      isStreaming: true,
    }

    setMessages((prev) => [...prev, userMessage, assistantMessage])

    try {
      let currentThreadId = activeThreadId

      if (!currentThreadId) {
        const newThread = await createThread()
        currentThreadId = newThread.id
        setActiveThreadId(currentThreadId)
        setThreads((prev) => [newThread, ...prev])
      }

      const reader = await sendMessage(inputValue, currentThreadId)

      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })

        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMessage.id
              ? {
                ...msg,
                content: msg.content + chunk,
              }
              : msg,
          ),
        )
      }

      setMessages((prev) => prev.map((msg) => (msg.id === assistantMessage.id ? { ...msg, isStreaming: false } : msg)))

      setTokenUsage((prev) => prev + Math.ceil(inputValue.length / 4) + 100)
    } catch (error) {
      console.error("[v0] Error sending message:", error)
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessage.id
            ? {
              ...msg,
              content: "요청을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.",
              isStreaming: false,
            }
            : msg,
        ),
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleNewChat = () => {
    setMessages([])
    setActiveThreadId(null)
    setTokenUsage(0)
  }

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content)
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion)
  }

  return (
    <ChatLayout
      isSidebarOpen={isSidebarOpen}
      onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
      messages={messages}
      threads={threads}
      activeThreadId={activeThreadId}
      tokenUsage={tokenUsage}
      inputValue={inputValue}
      isLoading={isLoading}
      onInputChange={setInputValue}
      onSubmit={handleSendMessage}
      onNewChat={handleNewChat}
      onSelectThread={handleSelectThread}
      onCopyMessage={handleCopyMessage}
      onSuggestionClick={handleSuggestionClick}
    />
  )
}
