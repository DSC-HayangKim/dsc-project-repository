"use client";
import { useState } from "react";
import { SectionContainer } from "@/components/layouts/section-container";
import { SectionHeader } from "@/components/layouts/section-header";
import { PricingCard } from "@/components/ui/pricing-card";

const ONE_TIME_PLANS = [
  {
    name: "베이직",
    tokens: "300",
    price: "3,000",
    description: "가벼운 검색을 위한 시작하기 좋은 플랜",
    features: ["최대 300 토큰", "기본 특허 검색", "이메일 지원"],
    highlighted: false,
  },
  {
    name: "스탠다드",
    tokens: "500",
    price: "5,000",
    description: "개인 사용자를 위한 실속형 플랜",
    features: ["최대 500 토큰", "기본 특허 검색", "시각화 결과", "이메일 지원"],
    highlighted: false,
  },
  {
    name: "프리미엄",
    tokens: "1,000",
    price: "10,000",
    description: "가장 인기 있는 표준 플랜",
    features: ["최대 1,000 토큰", "고급 특허 검색", "시각화 결과", "우선 지원"],
    highlighted: true,
  },
  {
    name: "비즈니스",
    tokens: "3,000",
    price: "30,000",
    description: "전문적인 분석을 위한 대용량 플랜",
    features: [
      "최대 3,000 토큰",
      "고급 특허 검색",
      "심화 분석",
      "우선 지원",
      "API 접근",
    ],
    highlighted: false,
  },
  {
    name: "엔터프라이즈",
    tokens: "5,000",
    price: "50,000",
    description: "대규모 프로젝트를 위한 최상위 플랜",
    features: [
      "최대 5,000 토큰",
      "전사적 기능",
      "VIP 지원",
      "API 접근",
      "팀 협업",
    ],
    highlighted: false,
  },
];

const SUBSCRIPTION_PLANS = [
  {
    name: "스타터 구독",
    tokens: "1,200",
    price: "10,000",
    description: "꾸준한 사용을 위한 스마트한 선택",
    features: [
      "매월 1,200 토큰 (+20% 보너스)",
      "기본 특허 검색",
      "시각화 결과",
      "이메일 지원",
      "미사용 토큰 이월",
    ],
    highlighted: false,
  },
  {
    name: "프로 구독",
    tokens: "3,600",
    price: "30,000",
    description: "전문가를 위한 최적의 구독 플랜",
    features: [
      "매월 3,600 토큰 (+20% 보너스)",
      "고급 특허 검색",
      "심화 분석",
      "우선 지원",
      "API 접근",
      "미사용 토큰 이월",
    ],
    highlighted: true,
  },
  {
    name: "비즈니스 구독",
    tokens: "6,000",
    price: "50,000",
    description: "팀과 조직을 위한 강력한 구독 플랜",
    features: [
      "매월 6,000 토큰 (+20% 보너스)",
      "전사적 기능",
      "VIP 지원",
      "API 접근",
      "팀 협업",
      "미사용 토큰 이월",
    ],
    highlighted: false,
  },
];

export default function PricingSection() {
  const [isSubscription, setIsSubscription] = useState(false);
  const plans = isSubscription ? SUBSCRIPTION_PLANS : ONE_TIME_PLANS;

  return (
    <SectionContainer hasBg>
      <SectionHeader
        title="토큰 기반 요금제"
        subtitle="필요할 때만 사용하고, 사용한 만큼만 지불하세요. 구독하면 더 많은 혜택을 드립니다."
      />

      {/* Toggle */}
      <div className="flex justify-center mb-12">
        <div className="bg-white/50 backdrop-blur border border-border p-1 rounded-xl inline-flex relative">
          <button
            onClick={() => setIsSubscription(false)}
            className={`px-6 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              !isSubscription
                ? "bg-white shadow-sm text-blue-600"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            일회성 결제
          </button>
          <button
            onClick={() => setIsSubscription(true)}
            className={`px-6 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
              isSubscription
                ? "bg-white shadow-sm text-blue-600"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            월간 구독
            <span className="ml-2 text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full">
              +20%
            </span>
          </button>
        </div>
      </div>

      {/* Pricing Cards */}
      <div
        className={`grid gap-8 ${isSubscription ? "sm:grid-cols-3" : "sm:grid-cols-3 lg:grid-cols-5"}`}
      >
        {plans.map((plan, index) => (
          <PricingCard
            key={index}
            {...plan}
            period={isSubscription ? "/월" : undefined}
          />
        ))}
      </div>

      {/* Additional Info */}
      <div className="mt-16 rounded-xl border border-border bg-white/50 p-8 text-center">
        <h3 className="text-lg font-semibold text-foreground mb-2">
          토큰은 어떻게 사용되나요?
        </h3>
        <p className="text-muted-foreground mb-4">
          각 특허 검색에 평균 10-50 토큰이 사용됩니다. 복잡한 분석이나 시각화는
          추가 토큰을 사용할 수 있습니다.
        </p>
        <p className="text-sm text-muted-foreground">
          미사용 토큰은 매월 초기화되거나 누적될 수 있습니다. 요금제별로 정책이
          다릅니다.
        </p>
      </div>
    </SectionContainer>
  );
}
