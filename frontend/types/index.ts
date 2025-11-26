export interface Feature {
  icon: string;
  title: string;
  description: string;
  color: string;
}

export interface PricingPlan {
  name: string;
  tokens: string;
  price: string;
  description: string;
  features: string[];
  highlighted: boolean;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  isStreaming?: boolean;
  created_at?: string;
}

export interface Thread {
  id: number;
  title: string | null;
  created_at: string;
  user_id: number;
}

export interface User {
  id: string;
  email: string;
  display_name: string;
  profile_image: string;
}
