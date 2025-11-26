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
        <div className="max-w-3xl px-4 py-2 rounded-xl bg-violet-100 text-slate-900 text-lg leading-relaxed">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex justify-start">
      <div className="w-full max-w-3xl">
        <div className="prose prose-base dark:prose-invert max-w-none text-slate-900">
          <ReactMarkdown
            components={{
              h1: ({ ...props }) => (
                <h1 className="text-2xl font-bold mt-6 mb-4 text-slate-900" {...props} />
              ),
              h2: ({ ...props }) => (
                <h2 className="text-xl font-bold mt-5 mb-3 text-slate-900" {...props} />
              ),
              h3: ({ ...props }) => (
                <h3 className="text-lg font-bold mt-4 mb-2 text-slate-900" {...props} />
              ),
              p: ({ ...props }) => (
                <p className="mb-4 leading-7 text-[15px] text-slate-800" {...props} />
              ),
              ul: ({ ...props }) => (
                <ul
                  className="list-disc list-outside ml-5 mb-4 space-y-2 text-slate-800"
                  {...props}
                />
              ),
              ol: ({ ...props }) => (
                <ol
                  className="list-decimal list-outside ml-5 mb-4 space-y-2 text-slate-800"
                  {...props}
                />
              ),
              li: ({ ...props }) => <li className="text-[15px] pl-1" {...props} />,
              code: ({ ...props }) => (
                <code
                  className="bg-slate-100 px-1.5 py-0.5 rounded text-sm font-mono text-slate-900 border border-slate-200"
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
                  className="border-l-4 border-slate-300 pl-4 py-1 italic text-slate-600 mb-4 bg-slate-50 rounded-r"
                  {...props}
                />
              ),
              table: ({ ...props }) => (
                <div className="overflow-x-auto mb-4 rounded-lg border border-slate-200">
                  <table
                    className="w-full border-collapse text-sm text-slate-800"
                    {...props}
                  />
                </div>
              ),
              th: ({ ...props }) => (
                <th
                  className="border-b border-slate-200 px-4 py-2 bg-slate-50 font-semibold text-left text-slate-900"
                  {...props}
                />
              ),
              td: ({ ...props }) => (
                <td className="border-b border-slate-200 px-4 py-2" {...props} />
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {!message.isStreaming && (
          <button
            onClick={handleCopy}
            className="mt-2 inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground transition-colors opacity-0 group-hover:opacity-100 cursor-pointer font-medium"
          >
            {copied ? (
              <>
                <Check className="h-4 w-4 text-green-500" />
                <span className="text-green-500">복사됨</span>
              </>
            ) : (
              <>
                <Copy className="h-4 w-4" />
                복사
              </>
            )}
          </button>
        )}

        {message.isStreaming && (
          <div className="flex items-center gap-1.5 mt-2 h-6 pl-1">
            <div className="w-2.5 h-2.5 bg-violet-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
            <div className="w-2.5 h-2.5 bg-violet-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
            <div className="w-2.5 h-2.5 bg-violet-400 rounded-full animate-bounce" />
          </div>
        )}
      </div>
    </div>
  );
}
