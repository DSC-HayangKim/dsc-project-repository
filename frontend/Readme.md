# 프로젝트 설정

npm 패키지를 설치할 때 아래와 같이 `--legacy-peer-deps` 옵션을 사용하면 React 16/17/18을 요구하는 `vaul@0.9.9` 의 peer dependency 충돌을 무시하고 설치할 수 있습니다.

```bash
npm install --legacy-peer-deps
```

> **주의**: 이 옵션은 최신 React 버전에서는 지원되지 않는 `vaul` 의 오래된 peer dependency 를 강제로 무시합니다. 프로젝트가 정상적으로 동작하는지 확인하세요.
