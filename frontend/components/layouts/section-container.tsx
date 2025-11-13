import type React from "react"

interface SectionContainerProps {
  children: React.ReactNode
  className?: string
  hasBorder?: boolean
  hasBg?: boolean
}

export function SectionContainer({
  children,
  className = "",
  hasBorder = false,
  hasBg = false,
}: SectionContainerProps) {
  return (
    <section
      className={`py-20 sm:py-32 ${hasBorder ? "border-t border-border" : ""} ${
        hasBg ? "bg-muted/30" : ""
      } ${className}`}
    >
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">{children}</div>
    </section>
  )
}
