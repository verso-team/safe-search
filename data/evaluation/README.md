# Clickbait Evaluation Seed

`clickbait-seed.jsonl`은 기능과 Evidence 파이프라인을 확인하기 위한 소규모
수작업 예제입니다. 공식 학습·평가 데이터가 아니며 성능 주장의 근거로 단독
사용하지 않습니다.

재현 실행:

```powershell
cd backend
.\.venv\Scripts\python.exe scripts\evaluate_clickbait.py
```

평가 결과에는 입력 ID, 정답, 예측, 점수, 인간 검토 여부, 정확도와 혼동 항목이
출력됩니다. 데이터 출처와 라벨링 지침이 확정되면 동일한 형식으로 교체합니다.
