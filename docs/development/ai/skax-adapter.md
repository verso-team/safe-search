# SKT A.X 모델 어댑터

## 선택한 연결 방식

SKT가 공개한 `skt/A.X-4.0-Light`를 vLLM으로 실행하고 OpenAI 호환
`/v1/chat/completions` API로 연결합니다.

- 공식 모델: https://huggingface.co/skt/A.X-4.0-Light
- A.X 4.0 공식 모델 카드: https://huggingface.co/skt/A.X-4.0

공식 모델 카드가 vLLM의 OpenAI 호환 실행 예시를 제공하므로, 비공개 대회
API 형식을 임의로 가정하지 않습니다. 추후 대회 전용 API가 제공되면 환경변수와
어댑터만 교체합니다.

## 설정

```env
CLICKBAIT_MODEL_PROVIDER=skax
SKAX_BASE_URL=http://127.0.0.1:8000/v1
SKAX_MODEL=skt/A.X-4.0-Light
SKAX_API_KEY=
SKAX_TIMEOUT_SECONDS=30
```

## vLLM 실행 예시

GPU와 모델 라이선스·사용 조건을 확인한 환경에서 실행합니다.

```bash
vllm serve "skt/A.X-4.0-Light" --host 127.0.0.1 --port 8000
```

## 신뢰성 통제

- 온도는 `0`으로 고정합니다.
- JSON 응답을 Pydantic 계약으로 검증합니다.
- 근거는 입력에 실제 존재하는 문구만 생성하도록 지시합니다.
- 응답 검증 또는 연결에 실패하면 규칙 기준선으로 폴백합니다.
- 폴백 시 `fallback_used=true`와 실패 사실을 한계에 기록합니다.
- 입력 해시, 정책 버전, 모델 이름과 판단 근거를 동일한 응답 형식으로 보존합니다.

## 아직 확인할 사항

- 대회에서 지정하는 정확한 A.X 모델 버전
- 대회 제공 API 주소와 인증 방식
- 외부 API로 입력할 수 있는 데이터 범위
- 요청·응답 로그 보존 조건
- 모델 및 데이터 라이선스
