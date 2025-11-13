"use client"

import { Button } from "@/components/ui/button"
import { MessageCircle, ArrowRight } from "lucide-react"
import Link from "next/link"
import { SectionContainer } from "@/components/layouts/section-container"

export default function CTA() {
  return (
    <SectionContainer hasBorder className="!py-20 sm:!py-32">
      <div className="mx-auto max-w-4xl">
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-600 to-purple-600 p-8 sm:p-16">
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0 bg-[linear-gradient(45deg,transparent_25%,rgba(255,255,255,.2)_25%,rgba(255,255,255,.2)_50%,transparent_50%,transparent_75%,rgba(255,255,255,.2)_75%,rgba(255,255,255,.2))] bg-[length:40px_40px]" />
          </div>

          {/* Content */}
          <div className="relative text-center">
            <h2 className="text-3xl font-bold text-white sm:text-4xl mb-4">지금 바로 특허 검색을 시작하세요</h2>
            <p className="text-lg text-white/90 max-w-2xl mx-auto mb-8">
              AI와의 대화만으로 한국의 특허를 효과적으로 찾아보세요. 정부기관의 선택, Patent AI와 함께하세요.
            </p>

            <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Link href="/chat">
                <Button size="lg" className="w-full sm:w-auto bg-white text-blue-600 hover:bg-white/90 font-semibold">
                  <MessageCircle className="mr-2 h-5 w-5" />
                  채팅 시작하기
                </Button>
              </Link>
              <Link href="#pricing">
                <Button
                  size="lg"
                  variant="outline"
                  className="w-full sm:w-auto border-white text-white hover:bg-white/10 bg-transparent"
                >
                  요금 확인하기
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </SectionContainer>
  )
}
