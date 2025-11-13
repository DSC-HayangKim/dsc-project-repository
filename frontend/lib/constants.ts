export const FEATURES = [
  {
    icon: "MessageCircle",
    title: "대화형 특허 검색",
    description: "자연스러운 대화를 통해 필요한 특허를 찾으세요. AI가 당신의 의도를 정확히 이해합니다.",
    color: "from-blue-500 to-blue-600",
  },
  {
    icon: "BarChart3",
    title: "지능형 시각화",
    description: "복잡한 특허 정보를 직관적인 차트와 그래프로 표현하여 빠른 의사결정을 지원합니다.",
    color: "from-purple-500 to-purple-600",
  },
  {
    icon: "Zap",
    title: "토큰 기반 과금",
    description: "필요할 때만 사용하고 요금을 지불하세요. 구독이 아닌 유연한 사용량 기반 결제 시스템.",
    color: "from-amber-500 to-amber-600",
  },
  {
    icon: "Lock",
    title: "높은 보안성",
    description: "정부기관 수준의 보안으로 민감한 특허 정보를 안전하게 보호합니다.",
    color: "from-green-500 to-green-600",
  },
  {
    icon: "Users",
    title: "팀 협업",
    description: "여러 사용자가 함께 특허 검색 결과를 공유하고 협업할 수 있습니다.",
    color: "from-rose-500 to-rose-600",
  },
  {
    icon: "Sparkles",
    title: "AI 기반 분석",
    description: "특허의 혁신성, 시장성, 기술적 가치를 AI가 자동으로 분석해줍니다.",
    color: "from-cyan-500 to-cyan-600",
  },
]

export const PRICING_PLANS = [
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

export const TYPING_HINTS = [
  "우리는 헬스케어 분야에서 진단 정확도 문제를 해결해야 하는데 적절한 방법을 추천해줘",
  "스마트팩토리 사업에 도움이 될만한 적절한 기술이 있을까?",
  "우리는 환경 모니터링 시스템을 구축하려고 하는데 관련 특허가 있을까?",
  "자동차 배터리 기술에서 최신 혁신 기술을 찾아줄 수 있을까?",
  "우리는 음성 인식 기술 개선이 필요한데 참고할 수 있는 특허가 있을까?",
]

export const NAVIGATION_LINKS = [
  { label: "기능", href: "#features" },
  { label: "요금", href: "#pricing" },
  { label: "문서", href: "#" },
]

export const FOOTER_LINKS = {
  product: [
    { label: "기능", href: "#features" },
    { label: "요금", href: "#pricing" },
    { label: "문서", href: "#" },
  ],
  company: [
    { label: "소개", href: "#" },
    { label: "블로그", href: "#" },
    { label: "문의", href: "#" },
  ],
  legal: [
    { label: "개인정보처리방침", href: "#" },
    { label: "이용약관", href: "#" },
    { label: "보안", href: "#" },
  ],
  social: [
    { label: "Twitter", href: "#" },
    { label: "GitHub", href: "#" },
    { label: "LinkedIn", href: "#" },
  ],
}

export const CHAT_SUGGESTIONS = [
  "AI 기반 의료 장비 특허 찾기",
  "배터리 기술 관련 특허 검색",
  "삼성의 최근 특허 조회",
  "신재생 에너지 특허 분석",
]

export const CHAT_EMPTY_STATE = {
  title: "특허 검색을 시작하세요",
  description:
    "AI와 자연스러운 대화를 통해 한국의 특허를 검색하세요. 예를 들어, 기술 분야, 출원인, 또는 특정 키워드로 질문해보세요.",
}

export const CHAT_PLACEHOLDERS = {
  input: "특허를 검색하거나 질문을 입력하세요...",
  tokenInfo: "각 요청마다 토큰이 사용됩니다. 자세히 알아보기",
}

export const SIDEBAR_LABELS = {
  recentChats: "최근 대화",
  tokenUsage: "토큰 사용량",
  newChat: "새 대화",
  chargeToken: "토큰 충전",
}

export const SIDEBAR_LOGO = "Patent AI"
export const HEADER_TITLE = "한국 특허 검색 AI"
