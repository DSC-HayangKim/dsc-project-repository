/**
 * 환경 변수 및 설정 관리 파일
 * process.env 값을 중앙에서 관리하고 타입 안전성을 제공합니다.
 */

export const ENV = {
    /**
     * 현재 실행 모드 (development, production, test)
     * Docker Compose의 environment 설정에 따라 결정됩니다.
     */
    NODE_ENV: process.env.NODE_ENV || "development",

    /**
     * 프로덕션(운영) 환경 여부
     */
    IS_PRODUCTION: process.env.NODE_ENV === "production",

    /**
     * 개발 환경 여부
     */
    IS_DEVELOPMENT: process.env.NODE_ENV === "development" || !process.env.NODE_ENV,

    /**
     * API 기본 URL
     * 클라이언트 사이드에서 접근하려면 환경변수명 앞에 NEXT_PUBLIC_이 붙어야 합니다.
     * 기본값: "/api/v1"
     */
    API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1",
} as const;
