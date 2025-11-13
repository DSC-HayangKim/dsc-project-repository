"use client"

import { FEATURES } from "@/lib/constants"
import { SectionContainer } from "@/components/layouts/section-container"
import { SectionHeader } from "@/components/layouts/section-header"
import { FeatureCard } from "@/components/ui/feature-card"
import { MessageCircle, BarChart3, Zap, Lock, Users, Sparkles } from "lucide-react"

const iconMap = {
  MessageCircle,
  BarChart3,
  Zap,
  Lock,
  Users,
  Sparkles,
}

export default function Features() {
  return (
    <SectionContainer hasBorder>
      <SectionHeader
        title="Patent AI의 핵심 기능"
        subtitle="최첨단 AI 기술로 한국 특허 검색을 완전히 새롭게 경험하세요"
      />

      <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((feature, index) => {
          const Icon = iconMap[feature.icon as keyof typeof iconMap]
          return (
            <FeatureCard
              key={index}
              icon={Icon}
              title={feature.title}
              description={feature.description}
              color={feature.color}
            />
          )
        })}
      </div>
    </SectionContainer>
  )
}
