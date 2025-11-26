"use client"

import { Copy, Check } from "lucide-react"
import ReactMarkdown from "react-markdown"
import { useState } from "react"
import type { Message } from "@/types"

interface MessageItemProps {
  message: Message
  onCopy: (content: string) => void
}

export function MessageItem({ message, onCopy }: MessageItemProps) {
  const isUser = message.role === "user"
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    onCopy(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  if (isUser) {
    return (
      <div className="flex justify-end">
        <div className="max-w-3xl px-4 py-2 rounded-xl bg-violet-100 text-violet-900 text-sm leading-relaxed">
          <p className="whitespace-pre-wrap">{message.content}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex justify-start">
      <div className="w-full max-w-3xl">
        <div className="prose prose-sm dark:prose-invert max-w-none text-foreground">
          <ReactMarkdown
            components={{
              h1: ({ ...props }) => <h1 className="text-lg font-bold mt-4 mb-2" {...props} />,
              h2: ({ ...props }) => <h2 className="text-base font-bold mt-3 mb-1" {...props} />,
              h3: ({ ...props }) => <h3 className="text-sm font-bold mt-2" {...props} />,
              p: ({ ...props }) => <p className="mb-2 leading-relaxed" {...props} />,
              ul: ({ ...props }) => <ul className="list-disc list-inside mb-2 space-y-1" {...props} />,
              ol: ({ ...props }) => <ol className="list-decimal list-inside mb-2 space-y-1" {...props} />,
              li: ({ ...props }) => <li className="text-sm" {...props} />,
              code: ({ ...props }) => <code className="bg-muted px-1.5 py-0.5 rounded text-xs font-mono" {...props} />,
              pre: ({ ...props }) => <pre className="bg-muted p-3 rounded-lg overflow-x-auto mb-2" {...props} />,
              blockquote: ({ ...props }) => (
                <blockquote className="border-l-4 border-blue-500 pl-3 italic text-muted-foreground mb-2" {...props} />
              ),
              table: ({ ...props }) => (
                <table className="border-collapse border border-border w-full text-xs mb-2" {...props} />
              ),
              th: ({ ...props }) => <th className="border border-border px-2 py-1 bg-muted font-bold" {...props} />,
              td: ({ ...props }) => <td className="border border-border px-2 py-1" {...props} />,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {!message.isStreaming && (
          <button
            onClick={handleCopy}
            className="mt-2 inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors opacity-0 group-hover:opacity-100"
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
  )
}
