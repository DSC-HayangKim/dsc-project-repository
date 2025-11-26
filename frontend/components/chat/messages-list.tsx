"use client";

import { useRef, useEffect } from "react";
import { MessageItem } from "./message-item";
import type { Message } from "@/types";

interface MessagesListProps {
  messages: Message[];
  onCopyMessage: (content: string) => void;
  onSuggestionClick: (suggestion: string) => void;
}

export function MessagesList({
  messages,
  onCopyMessage,
  onSuggestionClick,
}: MessagesListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-5xl mx-auto px-8 py-8 space-y-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className="group animate-in fade-in slide-in-from-bottom-4 duration-500 ease-out"
          >
            <MessageItem message={message} onCopy={onCopyMessage} />
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
