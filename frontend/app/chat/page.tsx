"use client";

import type React from "react";
import { useState, useEffect } from "react";
import { ChatLayout } from "@/components/chat/chat-layout";
import { Message, Thread } from "@/types";
import {
  fetchThreads,
  createThread,
  fetchMessages,
  sendMessage,
} from "@/lib/api";

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [threads, setThreads] = useState<Thread[]>([]);
  const [activeThreadId, setActiveThreadId] = useState<number | null>(null);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [tokenUsage, setTokenUsage] = useState(0);

  useEffect(() => {
    loadThreads();
  }, []);

  const loadThreads = async () => {
    try {
      const data = await fetchThreads();
      setThreads(data);
    } catch (error) {
      console.error("Failed to load threads:", error);
    }
  };

  const handleSelectThread = async (threadId: number) => {
    setActiveThreadId(threadId);
    setIsLoading(true);
    try {
      const msgs = await fetchMessages(threadId);
      setMessages(msgs);
    } catch (error) {
      console.error("Failed to load messages:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const currentInput = inputValue;
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: currentInput,
    };

    const assistantMessageId = (Date.now() + 1).toString();
    const assistantMessage: Message = {
      id: assistantMessageId,
      role: "assistant",
      content: "",
      isStreaming: true,
    };

    setInputValue("");
    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setIsLoading(true);

    try {
      let currentThreadId = activeThreadId;

      if (!currentThreadId) {
        const newThread = await createThread();
        currentThreadId = newThread.id;
        setActiveThreadId(currentThreadId);
        setThreads((prev) => [newThread, ...prev]);
      }

      const reader = await sendMessage(currentInput, currentThreadId);
      const decoder = new TextDecoder();
      let assistantResponse = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") continue;

            try {
              // Check if it's a JSON object
              if (data.trim().startsWith("{")) {
                const parsed = JSON.parse(data);

                if (parsed.event === "end_stream") {
                  continue;
                }

                if (parsed.content) {
                  assistantResponse += parsed.content;
                }
              } else {
                // Legacy text format fallback
                assistantResponse += data;
              }

              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? {
                        ...msg,
                        content: assistantResponse,
                      }
                    : msg
                )
              );
            } catch (e) {
              console.error("Error parsing stream data:", e);
              // Fallback: treat as raw text if parsing fails
              assistantResponse += data;
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? {
                        ...msg,
                        content: assistantResponse,
                      }
                    : msg
                )
              );
            }
          }
        }
      }

      // Final update to set isStreaming to false
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                isStreaming: false,
              }
            : msg
        )
      );

      setTokenUsage((prev) => prev + Math.ceil(currentInput.length / 4) + 100);
    } catch (error) {
      console.error("[v0] Error sending message:", error);
      setMessages((prev) =>
        prev.map((msg) =>
          msg.id === assistantMessageId
            ? {
                ...msg,
                content:
                  "요청을 처리하는 중 오류가 발생했습니다. 다시 시도해주세요.",
                isStreaming: false,
              }
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setActiveThreadId(null);
    setTokenUsage(0);
  };

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInputValue(suggestion);
  };

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
  );
}
