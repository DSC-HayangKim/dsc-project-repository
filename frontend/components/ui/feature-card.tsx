import type { LucideIcon } from "lucide-react"

interface FeatureCardProps {
  icon: LucideIcon
  title: string
  description: string
  color: string
}

export function FeatureCard({ icon: Icon, title, description, color }: FeatureCardProps) {
  return (
    <div className="group relative rounded-xl border border-border bg-white/50 backdrop-blur p-6 hover:border-blue-500/50 transition-all hover:shadow-lg hover:-translate-y-1">
      <div className={`inline-flex h-12 w-12 items-center justify-center rounded-lg bg-gradient-to-br ${color} mb-4`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  )
}
