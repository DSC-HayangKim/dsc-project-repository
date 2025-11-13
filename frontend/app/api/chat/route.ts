export async function POST(request: Request) {
  const { query, previousMessages } = await request.json()

  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      try {
        // 여기서 실제 LLM API를 호출합니다 (예: OpenAI, Claude 등)
        // 현재는 데모용 응답을 스트리밍합니다

        const demoResponse = `# 특허 검색 결과

**검색어**: ${query}

## 관련 특허 (상위 3개)

### 1. 특허명: "AI 기반 의료 진단 시스템"
- **특허번호**: 10-2024-001234
- **출원인**: 대학교 공학과
- **출원일**: 2024-01-15
- **분야**: 의료기기, 인공지능
- **요약**: 머신러닝 기술을 활용한 의료 이미지 분석 시스템

### 2. 특허명: "스마트 센서 기반 건강관리 기기"
- **특허번호**: 10-2024-001235
- **출원인**: 의료기기 회사 A
- **출원일**: 2024-01-20
- **분야**: 의료기기, IoT
- **요약**: 실시간 생체신호 모니터링 및 분석

### 3. 특허명: "클라우드 기반 의료 데이터 통합 플랫폼"
- **특허번호**: 10-2024-001236
- **출원인**: 헬스케어 스타트업
- **출원일**: 2024-01-25
- **분야**: 정보통신, 헬스케어
- **요약**: 환자 의료 정보의 안전한 통합 및 공유 플랫폼

## 분석

검색하신 "${query}"와 관련하여 총 **127개의 특허**를 찾았습니다.

- **최근 출원**: 지난 6개월 내 25개
- **주요 출원기관**: 대학 30%, 기업 60%, 개인 10%
- **기술 트렌드**: AI/ML 기술 활용도가 점진적으로 증가 중`

        for (let i = 0; i < demoResponse.length; i++) {
          controller.enqueue(encoder.encode(demoResponse[i]))
          await new Promise((resolve) => setTimeout(resolve, 20))
        }

        controller.close()
      } catch (error) {
        controller.error(error)
      }
    },
  })

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
    },
  })
}
