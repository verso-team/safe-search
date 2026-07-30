import json
import os
import re
from hashlib import sha256

import httpx

from app.schemas.clickbait import (
    ClickbaitAnalyzeRequest,
    ClickbaitAnalyzeResponse,
    ClickbaitEvidence,
)


INDICATORS: tuple[tuple[str, str, float], ...] = (
    (r"충격|경악|소름|발칵|난리", "과도한 감정 유발 표현", 0.22),
    (r"절대|무조건|100%|반드시", "단정적·절대적 표현", 0.18),
    (r"당신만|아무도 모르는|비밀|최초 공개", "정보 격차를 과장하는 표현", 0.20),
    (r"지금 확인|클릭|안 보면|놓치면|꼭 보세요", "즉각적인 클릭을 유도하는 표현", 0.24),
    (r"놀라운|전문가도 놀란", "놀라움과 권위를 이용한 호기심 유발", 0.24),
    (r"\d+\s*(일|주|개월)\s*만에", "짧은 기간의 극적인 변화를 강조", 0.24),
    (r"인생이 바뀐|완전히 달라진", "결과를 과도하게 약속하는 표현", 0.22),
    (r"\?{2,}|!{2,}", "반복 문장부호", 0.10),
    (r"\d+\s*(가지|초|분)\s*(만에|안에)?", "목록·시간을 이용한 과장형 표현", 0.24),
)
POLICY_VERSION = "clickbait-policy-2026.07.30-v2"
DECISION_THRESHOLDS = {"suspicious": 0.28, "clickbait": 0.45}


def _enforce_grounded_evidence(
    request: ClickbaitAnalyzeRequest,
    result: ClickbaitAnalyzeResponse,
) -> ClickbaitAnalyzeResponse:
    source_text = f"{request.title}\n{request.body}".casefold()
    grounded = [
        item for item in result.evidence if item.excerpt.strip().casefold() in source_text
    ]
    if len(grounded) == len(result.evidence):
        return result

    return result.model_copy(
        update={
            "evidence": grounded,
            "requires_human_review": True,
            "human_review_reason": "모델이 입력에서 확인되지 않는 근거를 생성해 사람의 확인이 필요합니다.",
            "limitations": result.limitations
            + ["입력에서 확인되지 않은 모델 생성 근거를 제거했습니다."],
        }
    )


def _heuristic_analysis(request: ClickbaitAnalyzeRequest) -> ClickbaitAnalyzeResponse:
    text = f"{request.title}\n{request.body}".strip()
    evidence: list[ClickbaitEvidence] = []
    score = 0.05

    for pattern, indicator, weight in INDICATORS:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if not match:
            continue
        evidence.append(
            ClickbaitEvidence(
                indicator=indicator,
                excerpt=match.group(0)[:80],
                weight=weight,
            )
        )
        score += weight

    score = min(round(score, 3), 1.0)
    if score >= 0.45:
        label = "clickbait"
    elif score >= 0.28:
        label = "suspicious"
    else:
        label = "normal"

    boundary_case = 0.23 <= score <= 0.49
    short_context = len(text) < 20
    requires_review = boundary_case or short_context
    reasons = []
    if boundary_case:
        reasons.append("분류 임계값과 가까운 경계 사례입니다.")
    if short_context:
        reasons.append("판단할 문맥이 충분하지 않습니다.")

    trace_material = f"{request.title}|{request.body}|{request.source_url or ''}"
    input_sha256 = sha256(trace_material.encode("utf-8")).hexdigest()
    trace_id = input_sha256[:16]
    confidence = min(0.95, 0.58 + abs(score - 0.43))

    return ClickbaitAnalyzeResponse(
        trace_id=trace_id,
        input_sha256=input_sha256,
        policy_version=POLICY_VERSION,
        label=label,
        score=score,
        confidence=round(confidence, 3),
        summary={
            "clickbait": "클릭을 유도하는 과장·호기심 표현이 여러 개 확인됐습니다.",
            "suspicious": "일부 클릭 유도 표현이 있어 원문과 출처 확인이 필요합니다.",
            "normal": "뚜렷한 클릭베이트 표현이 확인되지 않았습니다.",
        }[label],
        evidence=evidence,
        model_provider="heuristic",
        model_name="safe-search-rules-v1",
        fallback_used=False,
        decision_thresholds=DECISION_THRESHOLDS,
        requires_human_review=requires_review,
        human_review_reason=" ".join(reasons) or None,
        limitations=[
            "표현 패턴 중심의 1차 분석으로 기사의 사실 여부를 판정하지 않습니다.",
            "풍자·인용·문맥에 따라 오탐이 발생할 수 있습니다.",
        ],
    )


def _analyze_with_ollama(
    request: ClickbaitAnalyzeRequest,
    fallback: ClickbaitAnalyzeResponse,
) -> ClickbaitAnalyzeResponse:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
    prompt = {
        "task": "한국어 뉴스 제목의 클릭베이트 여부를 분석하세요.",
        "rules": [
            "label은 normal, suspicious, clickbait 중 하나",
            "score와 confidence는 0부터 1 사이",
            "근거는 입력에 실제 존재하는 짧은 문구만 사용",
            "불확실하거나 문맥이 부족하면 requires_human_review를 true로 설정",
        ],
        "input": request.model_dump(),
        "fallback_signal": {
            "score": fallback.score,
            "evidence": [item.model_dump() for item in fallback.evidence],
        },
    }
    response = httpx.post(
        f"{base_url}/api/generate",
        json={
            "model": model,
            "prompt": json.dumps(prompt, ensure_ascii=False),
            "format": ClickbaitAnalyzeResponse.model_json_schema(),
            "stream": False,
        },
        timeout=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "20")),
    )
    response.raise_for_status()
    payload = response.json()
    result_payload = json.loads(payload["response"])
    result_payload.update(
        {
            "trace_id": fallback.trace_id,
            "input_sha256": fallback.input_sha256,
            "policy_version": fallback.policy_version,
            "model_provider": "ollama",
            "model_name": model,
            "fallback_used": False,
            "decision_thresholds": fallback.decision_thresholds,
        }
    )
    result = ClickbaitAnalyzeResponse.model_validate(result_payload)
    result = result.model_copy(
        update={
            "trace_id": fallback.trace_id,
            "input_sha256": fallback.input_sha256,
            "policy_version": fallback.policy_version,
            "model_provider": "ollama",
            "model_name": model,
            "fallback_used": False,
            "decision_thresholds": fallback.decision_thresholds,
        }
    )
    return _enforce_grounded_evidence(request, result)


def _analyze_with_skax(
    request: ClickbaitAnalyzeRequest,
    fallback: ClickbaitAnalyzeResponse,
) -> ClickbaitAnalyzeResponse:
    base_url = os.getenv("SKAX_BASE_URL", "http://127.0.0.1:8000/v1").rstrip("/")
    model = os.getenv("SKAX_MODEL", "skt/A.X-4.0-Light")
    api_key = os.getenv("SKAX_API_KEY")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    prompt = {
        "task": "한국어 뉴스 제목의 클릭베이트 여부를 JSON으로 분석하세요.",
        "output": {
            "label": "normal | suspicious | clickbait",
            "score": "0~1",
            "confidence": "0~1",
            "summary": "짧은 한국어 설명",
            "evidence": [
                {"indicator": "근거 유형", "excerpt": "입력에 실제 있는 문구", "weight": "0~1"}
            ],
            "requires_human_review": "boolean",
            "human_review_reason": "문자열 또는 null",
            "limitations": ["한계"],
        },
        "rules": [
            "JSON 이외의 텍스트는 출력하지 마세요.",
            "근거 문구를 입력에 없는 내용으로 만들지 마세요.",
            "불확실하거나 문맥이 부족하면 인간 검토를 요청하세요.",
        ],
        "input": request.model_dump(),
        "baseline_signal": {
            "score": fallback.score,
            "evidence": [item.model_dump() for item in fallback.evidence],
        },
    }
    response = httpx.post(
        f"{base_url}/chat/completions",
        headers=headers,
        json={
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "당신은 근거를 공개하고 불확실성을 인정하는 AI 신뢰성 분석가입니다.",
                },
                {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=float(os.getenv("SKAX_TIMEOUT_SECONDS", "30")),
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    result_payload = json.loads(content)
    result_payload.update(
        {
            "trace_id": fallback.trace_id,
            "input_sha256": fallback.input_sha256,
            "policy_version": fallback.policy_version,
            "model_provider": "skax",
            "model_name": model,
            "fallback_used": False,
            "decision_thresholds": fallback.decision_thresholds,
        }
    )
    result = ClickbaitAnalyzeResponse.model_validate(result_payload)
    return _enforce_grounded_evidence(request, result)


def analyze_clickbait(request: ClickbaitAnalyzeRequest) -> ClickbaitAnalyzeResponse:
    fallback = _heuristic_analysis(request)
    provider = os.getenv("CLICKBAIT_MODEL_PROVIDER", "heuristic").lower()
    if provider == "heuristic":
        return fallback

    try:
        if provider == "ollama":
            return _analyze_with_ollama(request, fallback)
        if provider == "skax":
            return _analyze_with_skax(request, fallback)
        return fallback.model_copy(
            update={
                "fallback_used": True,
                "limitations": fallback.limitations
                + [f"지원하지 않는 모델 제공자 '{provider}'로 기준선을 사용했습니다."],
            }
        )
    except (httpx.HTTPError, KeyError, ValueError):
        return fallback.model_copy(
            update={
                "fallback_used": True,
                "limitations": fallback.limitations
                + [f"{provider} 연결 또는 응답 검증에 실패해 규칙 기반 분석으로 대체했습니다."]
            }
        )
