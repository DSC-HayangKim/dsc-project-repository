"use client";

import { Copy, Check } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useState } from "react";
import type { Message } from "@/types";

interface MessageItemProps {
  message: Message;
  onCopy: (content: string) => void;
}

export function MessageItem({ message, onCopy }: MessageItemProps) {
  const isUser = message.role === "user";
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    onCopy(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-3xl px-4 py-2 rounded-xl bg-violet-100 text-violet-900 text-lg leading-relaxed">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="w-full max-w-3xl">
        <div className="prose prose-base dark:prose-invert max-w-none text-foreground">
          <ReactMarkdown
            components={{
              h1: ({ ...props }) => (
                <h1 className="text-2xl font-bold mt-6 mb-4" {...props} />
              ),
              h2: ({ ...props }) => (
                <h2 className="text-xl font-bold mt-5 mb-3" {...props} />
              ),
              h3: ({ ...props }) => (
                <h3 className="text-lg font-bold mt-4 mb-2" {...props} />
              ),
              p: ({ ...props }) => (
                <p className="mb-4 leading-7 text-[15px]" {...props} />
              ),
              ul: ({ ...props }) => (
                <ul
                  className="list-disc list-outside ml-5 mb-4 space-y-2"
                  {...props}
                />
              ),
              ol: ({ ...props }) => (
                <ol
                  className="list-decimal list-outside ml-5 mb-4 space-y-2"
                  {...props}
                />
              ),
              li: ({ ...props }) => <li className="text-[15px] pl-1" {...props} />,
              code: ({ ...props }) => (
                <code
                  className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono text-pink-600 dark:text-pink-400"
                  {...props}
                />
              ),
              pre: ({ ...props }) => (
                <pre
                  className="bg-slate-950 dark:bg-slate-900 p-4 rounded-lg overflow-x-auto mb-4 text-slate-50 border border-slate-800"
                  {...props}
                />
              ),
              blockquote: ({ ...props }) => (
                <blockquote
                  className="border-l-4 border-violet-500 pl-4 py-1 italic text-muted-foreground mb-4 bg-violet-50/50 dark:bg-violet-900/10 rounded-r"
                  {...props}
                />
              ),
              table: ({ ...props }) => (
                <div className="overflow-x-auto mb-4 rounded-lg border border-border">
                  <table
                    className="w-full border-collapse text-sm"
                    {...props}
                  />
                </div>
              ),
              th: ({ ...props }) => (
                <th
                  className="border-b border-border px-4 py-2 bg-muted/50 font-semibold text-left"
                  {...props}
                />
              ),
              td: ({ ...props }) => (
                <td className="border-b border-border px-4 py-2" {...props} />
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {!message.isStreaming && (
          <button
            onClick={handleCopy}
            className="mt-2 inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors opacity-0 group-hover:opacity-100 cursor-pointer"
          >
            {copied ? (
              <>
                <Check className="h-3 w-3" />
                복사됨
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                복사
              </>
            )}
          </button>
        )}

        {message.isStreaming && (
          <div className="flex gap-1 mt-2">
            <div className="w-2 h-2 rounded-full bg-current opacity-60 animate-pulse" />
            <div className="w-2 h-2 rounded-full bg-current opacity-40 animate-pulse" />
            <div className="w-2 h-2 rounded-full bg-current opacity-20 animate-pulse" />
          </div>
        )}
      </div>
    </div>
  );
}
