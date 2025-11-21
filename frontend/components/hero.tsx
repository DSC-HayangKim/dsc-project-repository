"use client";
import TypingInput from "./typing-input";
import { Button } from "@/components/ui/button";
import { ArrowRight, MessageCircle, Zap } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

export default function Hero() {
  const [inputValue, setInputValue] = useState("");

  return (
    <section className="relative overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute left-1/2 top-0 h-96 w-96 -translate-x-1/2 rounded-full bg-gradient-to-b from-blue-500/20 to-transparent blur-3xl" />
        <div className="absolute right-0 top-1/4 h-72 w-72 rounded-full bg-gradient-to-b from-purple-500/20 to-transparent blur-3xl" />
        {/* Lightbrain Image */}
      </div>

      <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 sm:py-32">
        <div className="text-center">
          {/* Badge */}
          <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-border bg-white/50 px-4 py-2 backdrop-blur">
            <Zap className="h-4 w-4 text-blue-600" />
            <span className="text-sm font-medium text-foreground">
              AI 기반 한국 특허 검색 플랫폼
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="mb-6 text-4xl font-bold text-foreground sm:text-5xl lg:text-6xl text-balance">
            당신의{" "}
            <div className="relative inline-block">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                특허 발굴을
              </span>
              <img
                src="/hero/hero_lightbrain.png"
                alt="Lightbrain"
                className="absolute"
                style={{
                  top: "-50px",
                  left: "100%",
                  marginLeft: "30px",
                  width: "200px",
                  height: "auto",
                }}
              />
            </div>
            <br />
            AI로 혁신하세요
          </h1>

          {/* Description */}
          <p className="mx-auto mb-12 max-w-2xl text-lg text-muted-foreground">
            자연스러운 대화를 통해 한국의 특허를 지능적으로 검색하고, 시각화된
            결과로 최적의 선택을 하세요. 필요할 때만 토큰을 사용하는 유연한 가격
            정책.
          </p>

          {/* Typing Input Component */}
          <TypingInput />

          {/* CTA Buttons */}
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Link href="/chat">
              <Button
                size="lg"
                className="w-full sm:w-auto bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:cursor-pointer"
              >
                <MessageCircle className="mr-2 h-5 w-5" />
                지금 시작하기
              </Button>
            </Link>
            <Link href="#features">
              <Button
                size="lg"
                variant="outline"
                className="w-full sm:w-auto border-border hover:bg-muted bg-transparent hover:cursor-pointer"
              >
                더 알아보기
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
