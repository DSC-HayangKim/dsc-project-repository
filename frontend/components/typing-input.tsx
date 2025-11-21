"use client"

import type React from "react"
import { Button } from "@/components/ui/button"
import { Search } from "lucide-react"
import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { TYPING_HINTS } from "@/lib/constants"

interface TypingInputProps {
  onSearch?: (value: string) => void
}

export default function TypingInput({ onSearch }: TypingInputProps) {
  const router = useRouter()
  const [inputValue, setInputValue] = useState("")
  const [displayPlaceholder, setDisplayPlaceholder] = useState("")
  const [currentHintIndex, setCurrentHintIndex] = useState(0)
  const [charIndex, setCharIndex] = useState(0)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const currentHint = TYPING_HINTS[currentHintIndex]
    const typingSpeed = isDeleting ? 30 : 50
    const pauseTime = 3000

    let timer: NodeJS.Timeout

    if (!isDeleting && charIndex < currentHint.length) {
      timer = setTimeout(() => {
        setDisplayPlaceholder(currentHint.slice(0, charIndex + 1))
        setCharIndex(charIndex + 1)
      }, typingSpeed)
    } else if (!isDeleting && charIndex === currentHint.length) {
      timer = setTimeout(() => {
        setIsDeleting(true)
      }, pauseTime)
    } else if (isDeleting && charIndex > 0) {
      timer = setTimeout(() => {
        setDisplayPlaceholder(currentHint.slice(0, charIndex - 1))
        setCharIndex(charIndex - 1)
      }, typingSpeed)
    } else if (isDeleting && charIndex === 0) {
      setIsDeleting(false)
      setCurrentHintIndex((prev) => (prev + 1) % TYPING_HINTS.length)
    }

    return () => clearTimeout(timer)
  }, [charIndex, isDeleting, currentHintIndex])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      router.push(`/chat?query=${encodeURIComponent(inputValue)}`)
      setInputValue("")
    }
  }

  return (
    <form onSubmit={handleSearch} className="mx-auto mb-12 max-w-2xl">
      <div className="flex gap-2">
        <div className="flex-1 relative">
          <input
            type="text"
            placeholder={displayPlaceholder}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="w-full px-4 py-3 pl-12 rounded-lg border border-border bg-white/50 backdrop-blur placeholder:text-muted-foreground text-foreground focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500"
          />
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
        </div>
        <Button
          type="submit"
          size="lg"
          className="bg-gradient-to-r from-blue-600 to-purple-600 hover:cursor-pointer text-white px-8"
        >
          검색
        </Button>
      </div>
    </form>
  )
}
