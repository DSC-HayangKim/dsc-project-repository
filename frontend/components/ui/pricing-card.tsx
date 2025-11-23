import { Check } from "lucide-react";
import Link from "next/link";
import { Button } from "./button";
import type { PricingPlan } from "@/types";

interface PricingCardProps extends PricingPlan {
  period?: string;
}

export function PricingCard({
  name,
  tokens,
  price,
  description,
  features,
  highlighted,
}: PricingCardProps) {
  return (
    <div
      className={`relative rounded-2xl border transition-all ${
        highlighted
          ? "border-blue-500 bg-white/70 shadow-xl scale-105"
          : "border-border bg-white/50"
      } p-8`}
    >
      {highlighted && (
        <div className="absolute -top-4 left-1/2 -translate-x-1/2">
          <span className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-semibold px-4 py-1 rounded-full">
            인기 상품
          </span>
        </div>
      )}

      <h3 className="text-2xl font-bold text-foreground mb-2">{name}</h3>
      <p className="text-sm text-muted-foreground mb-6">{description}</p>

      <div className="mb-6">
        <div className="flex items-baseline gap-2">
          <span className="text-4xl font-bold text-foreground">{tokens}</span>
          <span className="text-muted-foreground">토큰</span>
        </div>
        <div className="mt-2 text-2xl font-bold text-foreground">
          {price === "맞춤형" ? (
            price
          ) : (
            <>
              ₩{price}
              {period && (
                <span className="text-sm text-muted-foreground font-normal">
                  {period}
                </span>
              )}
            </>
          )}
        </div>
      </div>

      <Link href="/chat" className="block mb-8">
        <Button
          className="w-full"
          variant={highlighted ? "default" : "outline"}
        >
          시작하기
        </Button>
      </Link>

      <ul className="space-y-3 border-t border-border pt-6">
        {features.map((feature, idx) => (
          <li key={idx} className="flex items-center gap-3">
            <Check className="h-5 w-5 text-green-600 flex-shrink-0" />
            <span className="text-sm text-foreground">{feature}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
