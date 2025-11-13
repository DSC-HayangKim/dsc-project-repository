"use client"
import { PRICING_PLANS } from "@/lib/constants"
import { SectionContainer } from "@/components/layouts/section-container"
import { SectionHeader } from "@/components/layouts/section-header"
import { PricingCard } from "@/components/ui/pricing-card"

const plans = [
  {
    name: "스타터",
    tokens: "1,000",
    price: "10,000",
    description: "개인 사용자와 소규모 팀을 위한 요금제",
    features: ["최대 1,000 토큰", "기본 특허 검색", "시각화 결과", "이메일 지원", "API 접근 불가"],
    highlighted: false,
  },
  {
    name: "프로페셔널",
    tokens: "10,000",
    price: "80,000",
    description: "정부기관 및 중형 조직을 위한 요금제",
    features: [
      "최대 10,000 토큰",
      "고급 특허 검색 및 필터링",
      "심화 분석 및 시각화",
      "우선 지원 (24시간)",
      "REST API 접근",
      "팀 협업 기능",
      "월간 분석 리포트",
    ],
    highlighted: true,
  },
  {
    name: "엔터프라이즈",
    tokens: "무제한",
    price: "맞춤형",
    description: "대규모 조직 및 정부 기관을 위한 요금제",
    features: [
      "무제한 토큰",
      "전사 규모 배포",
      "VIP 기술 지원",
      "SLA 보장",
      "전용 API 키",
      "커스텀 통합",
      "데이터 마이그레이션",
      "보안 감사 및 컴플라이언스",
    ],
    highlighted: false,
  },
]

export default function PricingSection() {
  return (
    <SectionContainer hasBg>
      <SectionHeader
        title="토큰 기반 요금제"
        subtitle="필요할 때만 사용하고, 사용한 만큼만 지불하세요. 고객의 니즈를 그대로 반영합니다."
      />

      {/* Pricing Cards */}
      <div className="grid gap-8 sm:grid-cols-3">
        {PRICING_PLANS.map((plan, index) => (
          <PricingCard key={index} {...plan} />
        ))}
      </div>

      {/* Additional Info */}
      <div className="mt-16 rounded-xl border border-border bg-white/50 p-8 text-center">
        <h3 className="text-lg font-semibold text-foreground mb-2">토큰은 어떻게 사용되나요?</h3>
        <p className="text-muted-foreground mb-4">
          각 특허 검색에 평균 10-50 토큰이 사용됩니다. 복잡한 분석이나 시각화는 추가 토큰을 사용할 수 있습니다.
        </p>
        <p className="text-sm text-muted-foreground">
          미사용 토큰은 매월 초기화되거나 누적될 수 있습니다. 요금제별로 정책이 다릅니다.
        </p>
      </div>
    </SectionContainer>
  )
}
