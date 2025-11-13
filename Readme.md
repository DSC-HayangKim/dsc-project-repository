## 🛑 이미 추적 중인 파일의 변경 사항 무시하기

이 기능을 위해 Git의 **`assume-unchanged`** 플래그를 사용합니다.

### 1\. `assume-unchanged` 명령어 사용

Git에게 해당 파일의 변경 사항을 무시하고, **변경되지 않은 것처럼 가정**하라고 지시합니다.

```bash
git update-index --assume-unchanged [파일 경로]
```

#### 예시

`.env` 파일을 이미 커밋했고, 이제부터는 로컬 변경 사항을 무시하고 싶다면:

```bash
git update-index --assume-unchanged .env.prod
git update-index --assume-unchanged .env.dev
```


### 2\. 작동 방식

이 명령어를 실행하면, Git은 해당 파일에 **로컬 변경 사항이 생기더라도** `git status`나 `git diff`에서 이를 **보고하지 않습니다**. 따라서 실수로 커밋할 가능성이 사라집니다.

-----

## ↩️ 추적을 다시 시작하는 방법

나중에 해당 파일의 변경 사항을 **다시 추적**하거나 **최신 버전으로 업데이트**하고 싶다면, 다음 명령어를 사용하여 플래그를 해제해야 합니다.

```bash
git update-index --no-assume-unchanged [파일 경로]
```

#### 예시

`.env` 파일 추적을 다시 활성화하고 싶다면:

```bash
git update-index --no-assume-unchanged .env
```

### ⚠️ 주의 사항

1.  **다른 팀원에게 전파되지 않음:** 이 설정은 **로컬 환경**에만 적용되는 설정입니다. 다른 팀원들이 이 파일을 추적하지 않게 하려면, 그들 역시 각자의 로컬 환경에서 위의 `assume-unchanged` 명령어를 실행해야 합니다.
2.  **업데이트 어려움:** 이 플래그가 설정된 상태에서는 원격 저장소에서 파일 내용이 업데이트되어도 **`git pull` 시 충돌이 발생하지 않고 로컬 파일이 업데이트되지 않을 수 있습니다.** 따라서 팀 전체가 중요한 설정 파일을 자주 업데이트해야 한다면 이 방법은 불편할 수 있습니다. (이 경우 `.env.template`을 사용하는 것이 가장 좋습니다.)