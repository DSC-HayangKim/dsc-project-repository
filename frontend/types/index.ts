export interface Feature {
  icon: string
  title: string
  description: string
  color: string
}

export interface PricingPlan {
  name: string
  tokens: string
  price: string
  description: string
  features: string[]
  highlighted: boolean
}

export interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  isStreaming?: boolean
}
