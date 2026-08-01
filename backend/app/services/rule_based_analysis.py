from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum

from app.schemas.analysis import (
    ActionItem,
    Agency,
    AnalyzeResponse,
    EmotionalState,
    UrgencyLevel,
    UserIntent,
)
from app.services.institution_catalog import (
    D4U,
    FSS_1332,
    KISA_118,
    POLICE,
    WOMEN_1366,
)


class ScenarioKey(str, Enum):
    physical_threat = "physical_threat"
    digital_sexual_harm = "digital_sexual_harm"
    phishing_impersonation = "phishing_impersonation"
    account_takeover = "account_takeover"
    stalking = "stalking"
    information = "information"
    unknown = "unknown"


@dataclass(frozen=True)
class ScenarioDefinition:
    key: ScenarioKey
    terms: tuple[str, ...]
    strong_terms: tuple[str, ...]
    harm_type: str
    primary_intent: UserIntent
    urgency: UrgencyLevel
    base_confidence: float
    emotional_state: EmotionalState
    emotional_support_message: str
    situation_summary: str
    immediate_actions: tuple[ActionItem, ...]
    safe_search_queries: tuple[str, ...]
    agencies: tuple[Agency, ...]
    requires_human_review: bool


@dataclass(frozen=True)
class ScenarioMatch:
    definition: ScenarioDefinition
    matched_terms: tuple[str, ...]
    matched_strong_terms: tuple[str, ...]
    score: int


URGENCY_RANK = {
    UrgencyLevel.low: 0,
    UrgencyLevel.medium: 1,
    UrgencyLevel.high: 2,
    UrgencyLevel.critical: 3,
}

CRITICAL_PATTERNS = (
    "흉기",
    "칼을 들",
    "죽이겠다",
    "죽여 버리",
    "죽여버리",
    "폭행 중",
    "맞고 있어",
    "감금",
    "납치",
    "문을 부수",
    "집 앞에 찾아왔",
    "지금 따라오",
    "차로 쫓아오",
    "강제로 끌고",
)

DISTRESS_TERMS = (
    "너무 무서",
    "살려",
    "공포",
    "견딜 수 없",
    "잠을 못",
    "숨이 안",
)
FEAR_TERMS = ("무서", "두렵", "겁나")
ANXIETY_TERMS = ("불안", "걱정", "초조")
CONFUSION_TERMS = ("모르겠", "어떻게", "헷갈", "막막")

REPORTING_TERMS = ("신고", "고소", "수사", "경찰")
EVIDENCE_TERMS = ("증거", "캡처", "스크린샷", "기록", "보존")
INFORMATION_TERMS = ("방법", "어디", "알려", "절차", "확인")
INSTITUTION_TERMS = ("기관", "센터", "상담", "지원")


SCENARIOS: tuple[ScenarioDefinition, ...] = (
    ScenarioDefinition(
        key=ScenarioKey.digital_sexual_harm,
        terms=(
            "영상 유포",
            "영상이 퍼지",
            "사진 유포",
            "사진이 퍼지",
            "퍼뜨리",
            "몸캠",
            "촬영물",
            "불법촬영",
            "성착취",
            "딥페이크",
            "합성 사진",
            "나체 사진",
            "유포 협박",
            "온라인 그루밍",
        ),
        strong_terms=(
            "유포 협박",
            "몸캠",
            "불법촬영",
            "성착취",
            "딥페이크",
        ),
        harm_type="디지털 성범죄·촬영물 유포 피해 가능성",
        primary_intent=UserIntent.reporting,
        urgency=UrgencyLevel.high,
        base_confidence=0.76,
        emotional_state=EmotionalState.anxious,
        emotional_support_message=(
            "피해를 혼자 감당할 필요는 없습니다. "
            "상대의 추가 요구에 응하지 말고 증거와 게시물 주소부터 보존하세요."
        ),
        situation_summary=(
            "촬영물 유포 또는 유포 협박과 관련된 신호가 확인되어 "
            "증거 보존과 공식 지원기관 상담을 우선 안내합니다."
        ),
        immediate_actions=(
            ActionItem(
                title="추가 요구에 응하지 않기",
                detail="송금하거나 새로운 사진·영상·개인정보를 보내지 마세요.",
                priority=1,
            ),
            ActionItem(
                title="원본과 URL 보존하기",
                detail="대화, 계정명, 게시물 URL과 피해 촬영물 원본을 삭제하지 말고 보존하세요.",
                priority=2,
            ),
            ActionItem(
                title="전문 지원기관에 상담하기",
                detail="중앙디지털성범죄피해자지원센터 또는 경찰에 상담·신고하세요.",
                priority=3,
            ),
        ),
        safe_search_queries=(
            "중앙디지털성범죄피해자지원센터 상담",
            "디지털 성범죄 피해 촬영물 삭제 지원",
            "경찰청 사이버범죄 신고시스템",
        ),
        agencies=(D4U, POLICE, WOMEN_1366),
        requires_human_review=True,
    ),
    ScenarioDefinition(
        key=ScenarioKey.phishing_impersonation,
        terms=(
            "보이스피싱",
            "스미싱",
            "기관 사칭",
            "검찰 사칭",
            "경찰 사칭",
            "금융감독원 사칭",
            "안전계좌",
            "원격 앱",
            "원격제어 앱",
            "인증번호",
            "송금하라고",
            "계좌로 보내",
            "대출 수수료",
            "택배 링크",
            "과태료 링크",
        ),
        strong_terms=(
            "안전계좌",
            "원격제어 앱",
            "검찰 사칭",
            "경찰 사칭",
            "금융감독원 사칭",
            "인증번호",
        ),
        harm_type="피싱·스미싱 또는 기관 사칭 금융사기 가능성",
        primary_intent=UserIntent.information,
        urgency=UrgencyLevel.high,
        base_confidence=0.72,
        emotional_state=EmotionalState.anxious,
        emotional_support_message=(
            "지금은 상대가 요구한 송금·인증·앱 설치를 멈추는 것이 우선입니다."
        ),
        situation_summary=(
            "기관 사칭, 링크 클릭, 송금 또는 인증정보 요구와 관련된 위험 신호가 확인되었습니다."
        ),
        immediate_actions=(
            ActionItem(
                title="송금·인증·앱 설치 중단하기",
                detail="상대가 요구한 이체, 인증번호 전달, 원격제어 앱 설치를 진행하지 마세요.",
                priority=1,
            ),
            ActionItem(
                title="공식 번호로 별도 확인하기",
                detail="문자나 통화에 표시된 번호가 아닌 기관 공식 대표번호로 직접 확인하세요.",
                priority=2,
            ),
            ActionItem(
                title="피해 발생 시 즉시 신고하기",
                detail="송금이나 정보 제공이 있었다면 경찰과 금융기관에 즉시 알리세요.",
                priority=3,
            ),
        ),
        safe_search_queries=(
            "경찰청 보이스피싱 신고",
            "한국인터넷진흥원 118 스미싱 상담",
            "금융감독원 1332 금융사기 상담",
        ),
        agencies=(POLICE, KISA_118, FSS_1332),
        requires_human_review=True,
    ),
    ScenarioDefinition(
        key=ScenarioKey.account_takeover,
        terms=(
            "계정 해킹",
            "계정 탈취",
            "로그인 알림",
            "로그인 시도",
            "비밀번호 변경",
            "복구 이메일",
            "인증코드",
            "접속 기록",
            "내 계정으로",
            "모르는 기기",
            "2단계 인증",
            "이중 인증",
        ),
        strong_terms=(
            "계정 탈취",
            "비밀번호 변경",
            "모르는 기기",
            "인증코드",
            "복구 이메일",
        ),
        harm_type="온라인 계정 탈취·무단접속 가능성",
        primary_intent=UserIntent.information,
        urgency=UrgencyLevel.medium,
        base_confidence=0.70,
        emotional_state=EmotionalState.confused,
        emotional_support_message=(
            "접속 가능한 안전한 기기에서 계정 보호 조치를 순서대로 진행하세요."
        ),
        situation_summary=(
            "본인이 요청하지 않은 로그인·비밀번호·복구정보 변경 신호가 확인되었습니다."
        ),
        immediate_actions=(
            ActionItem(
                title="공식 앱·사이트에서 비밀번호 변경하기",
                detail="문자 링크가 아니라 서비스의 공식 앱이나 주소를 직접 열어 변경하세요.",
                priority=1,
            ),
            ActionItem(
                title="모든 세션 종료하고 2단계 인증 켜기",
                detail="알 수 없는 기기의 로그인 세션을 종료하고 추가 인증을 설정하세요.",
                priority=2,
            ),
            ActionItem(
                title="피해 기록과 알림 보존하기",
                detail="로그인 알림, 접속 기록, 변경 메일과 계정 활동을 캡처해 두세요.",
                priority=3,
            ),
        ),
        safe_search_queries=(
            "한국인터넷진흥원 118 계정 해킹 상담",
            "계정 탈취 비밀번호 변경 공식 도움말",
            "경찰청 사이버범죄 신고시스템 계정 해킹",
        ),
        agencies=(KISA_118, POLICE),
        requires_human_review=False,
    ),
    ScenarioDefinition(
        key=ScenarioKey.stalking,
        terms=(
            "스토킹",
            "미행",
            "따라와",
            "계속 따라",
            "집 앞에서 기다",
            "회사 앞에서 기다",
            "연락을 계속",
            "위치 추적",
            "몰래 따라",
            "주변을 맴돌",
            "데이트폭력",
        ),
        strong_terms=(
            "스토킹",
            "미행",
            "집 앞에서 기다",
            "위치 추적",
            "데이트폭력",
        ),
        harm_type="스토킹·미행 또는 반복적 접근 위험 가능성",
        primary_intent=UserIntent.emergency,
        urgency=UrgencyLevel.high,
        base_confidence=0.74,
        emotional_state=EmotionalState.fearful,
        emotional_support_message=(
            "혼자 상대를 확인하거나 대면하지 말고, 사람이 있는 안전한 장소로 이동하세요."
        ),
        situation_summary=(
            "반복적인 접근·연락·위치 추적과 관련된 안전 위험 신호가 확인되었습니다."
        ),
        immediate_actions=(
            ActionItem(
                title="밝고 사람이 있는 장소로 이동하기",
                detail="집으로 바로 가지 말고 편의점, 지구대 등 도움을 요청할 수 있는 곳으로 이동하세요.",
                priority=1,
            ),
            ActionItem(
                title="신뢰할 사람에게 위치 알리기",
                detail="현재 위치와 상황을 가족·지인에게 공유하고 혼자 이동하지 마세요.",
                priority=2,
            ),
            ActionItem(
                title="반복 접근 기록 보존하기",
                detail="연락, 방문, 이동 경로, 시간과 장소를 삭제하지 말고 기록하세요.",
                priority=3,
            ),
        ),
        safe_search_queries=(
            "경찰청 스토킹 피해 신고",
            "여성긴급전화 1366 스토킹 상담",
            "스토킹 피해 증거 보존 방법",
        ),
        agencies=(POLICE, WOMEN_1366),
        requires_human_review=True,
    ),
    ScenarioDefinition(
        key=ScenarioKey.information,
        terms=(
            "신고 방법",
            "어디로 신고",
            "어디에 문의",
            "상담 받고",
            "도움 받을",
            "지원 기관",
            "절차가 궁금",
            "알고 싶",
        ),
        strong_terms=("어디로 신고", "지원 기관", "절차가 궁금"),
        harm_type="피해 대응 정보·기관 안내 요청",
        primary_intent=UserIntent.information,
        urgency=UrgencyLevel.low,
        base_confidence=0.64,
        emotional_state=EmotionalState.stable,
        emotional_support_message=(
            "필요한 절차와 공식기관을 차근차근 확인할 수 있도록 안내하겠습니다."
        ),
        situation_summary=(
            "즉각적인 위험 신호보다는 신고·상담·지원 절차에 대한 정보 요청이 중심으로 보입니다."
        ),
        immediate_actions=(
            ActionItem(
                title="현재 상황을 짧게 정리하기",
                detail="발생 시점, 상대방, 피해 내용과 보유한 증거를 메모하세요.",
                priority=1,
            ),
            ActionItem(
                title="관련 공식기관 확인하기",
                detail="피해 유형에 맞는 공식기관의 상담·신고 절차를 확인하세요.",
                priority=2,
            ),
            ActionItem(
                title="민감정보는 최소한만 공유하기",
                detail="공식 접수 전에는 주민번호, 인증번호, 전체 계좌번호를 보내지 마세요.",
                priority=3,
            ),
        ),
        safe_search_queries=(
            "경찰청 사이버범죄 신고시스템",
            "범죄 피해자 공식 상담 기관",
            "한국인터넷진흥원 118 상담",
        ),
        agencies=(POLICE, KISA_118),
        requires_human_review=False,
    ),
)


def analyze_safely(text: str) -> AnalyzeResponse:
    """결정론적 규칙 기반 안전 분석.

    이 함수는 범죄 성립 여부나 법률 결론을 판단하지 않는다.
    입력에서 안전 대응에 필요한 신호를 찾아 정보 우선순위를 정한다.
    """
    normalized = _normalize(text)

    if _contains_any(normalized, CRITICAL_PATTERNS):
        return _critical_result(normalized)

    matches = [_match_scenario(normalized, scenario) for scenario in SCENARIOS]
    candidates = [match for match in matches if match.score > 0]

    if not candidates:
        return _unknown_result(normalized)

    selected = max(
        candidates,
        key=lambda match: (
            URGENCY_RANK[match.definition.urgency],
            match.score,
            len(match.matched_strong_terms),
        ),
    )

    return _build_result(normalized, selected)


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).lower().strip()
    return re.sub(r"\s+", " ", normalized)


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _match_scenario(
    text: str,
    definition: ScenarioDefinition,
) -> ScenarioMatch:
    matched_terms = tuple(term for term in definition.terms if term in text)
    matched_strong_terms = tuple(
        term for term in definition.strong_terms if term in text
    )
    score = len(matched_terms) + (2 * len(matched_strong_terms))

    return ScenarioMatch(
        definition=definition,
        matched_terms=matched_terms,
        matched_strong_terms=matched_strong_terms,
        score=score,
    )


def _build_result(
    text: str,
    match: ScenarioMatch,
) -> AnalyzeResponse:
    definition = match.definition
    confidence = min(
        0.90,
        definition.base_confidence
        + min(match.score, 4) * 0.035,
    )
    emotional_state = _detect_emotional_state(
        text,
        default=definition.emotional_state,
    )
    secondary_intents = _detect_secondary_intents(
        text,
        primary=definition.primary_intent,
    )

    requires_human_review = (
        definition.requires_human_review
        or definition.urgency in {UrgencyLevel.high, UrgencyLevel.critical}
        or confidence < 0.65
    )

    safety_notice = (
        "이 결과는 규칙과 표현 일치에 따른 안전 안내이며, "
        "범죄 확정·법률 판단·수사기관의 최종 판단을 의미하지 않습니다."
    )

    return AnalyzeResponse(
        primary_intent=definition.primary_intent,
        secondary_intents=secondary_intents,
        emotional_state=emotional_state,
        urgency=definition.urgency,
        confidence=round(confidence, 2),
        suspected_harm_type=definition.harm_type,
        emotional_support_message=definition.emotional_support_message,
        situation_summary=definition.situation_summary,
        immediate_actions=list(definition.immediate_actions),
        safe_search_queries=list(definition.safe_search_queries),
        recommended_agencies=list(definition.agencies),
        requires_human_review=requires_human_review,
        safety_notice=safety_notice,
    )


def _detect_secondary_intents(
    text: str,
    *,
    primary: UserIntent,
) -> list[UserIntent]:
    candidates: list[UserIntent] = []

    if _contains_any(text, REPORTING_TERMS):
        candidates.append(UserIntent.reporting)
    if _contains_any(text, EVIDENCE_TERMS):
        candidates.append(UserIntent.evidence)
    if _contains_any(text, INFORMATION_TERMS):
        candidates.append(UserIntent.information)
    if _contains_any(text, INSTITUTION_TERMS):
        candidates.append(UserIntent.institution)
    if _contains_any(
        text,
        DISTRESS_TERMS + FEAR_TERMS + ANXIETY_TERMS,
    ):
        candidates.append(UserIntent.emotional_support)

    if primary == UserIntent.reporting:
        candidates.extend([UserIntent.information, UserIntent.evidence])
    elif primary == UserIntent.emergency:
        candidates.append(UserIntent.reporting)
    elif primary == UserIntent.information:
        candidates.append(UserIntent.institution)

    unique: list[UserIntent] = []
    for intent in candidates:
        if intent != primary and intent not in unique:
            unique.append(intent)

    return unique[:3]


def _detect_emotional_state(
    text: str,
    *,
    default: EmotionalState,
) -> EmotionalState:
    if _contains_any(text, DISTRESS_TERMS):
        return EmotionalState.high_distress
    if _contains_any(text, FEAR_TERMS):
        return EmotionalState.fearful
    if _contains_any(text, ANXIETY_TERMS):
        return EmotionalState.anxious
    if _contains_any(text, CONFUSION_TERMS):
        return EmotionalState.confused
    return default


def _critical_result(text: str) -> AnalyzeResponse:
    secondary_intents = _detect_secondary_intents(
        text,
        primary=UserIntent.emergency,
    )

    return AnalyzeResponse(
        primary_intent=UserIntent.emergency,
        secondary_intents=secondary_intents,
        emotional_state=EmotionalState.panic,
        urgency=UrgencyLevel.critical,
        confidence=0.93,
        suspected_harm_type="즉각적인 신체 안전 위협 가능성",
        emotional_support_message=(
            "지금은 상황을 분석하는 것보다 안전한 장소로 이동하고 "
            "주변 사람과 긴급기관에 도움을 요청하는 것이 우선입니다."
        ),
        situation_summary=(
            "현재 위치에서 즉각적인 신체 위험으로 이어질 수 있는 표현이 확인되었습니다."
        ),
        immediate_actions=[
            ActionItem(
                title="안전한 장소로 즉시 이동하기",
                detail="문을 잠글 수 있거나 주변 사람이 있는 장소로 이동하세요.",
                priority=1,
            ),
            ActionItem(
                title="112에 연락하기",
                detail="직접 통화하기 어렵다면 주변 사람에게 신고를 요청하세요.",
                priority=2,
            ),
            ActionItem(
                title="신뢰할 사람에게 위치 공유하기",
                detail="현재 위치와 이동 방향을 가족·지인에게 알리세요.",
                priority=3,
            ),
        ],
        safe_search_queries=[
            "경찰청 긴급 신고 112",
            "여성긴급전화 1366",
        ],
        recommended_agencies=[POLICE, WOMEN_1366],
        requires_human_review=True,
        safety_notice=(
            "지금 생명이나 신체가 위험하다면 앱 안내보다 "
            "안전한 장소 이동과 112 신고를 우선하세요."
        ),
    )


def _unknown_result(text: str) -> AnalyzeResponse:
    emotional_state = _detect_emotional_state(
        text,
        default=EmotionalState.confused,
    )

    return AnalyzeResponse(
        primary_intent=UserIntent.unknown,
        secondary_intents=[UserIntent.information],
        emotional_state=emotional_state,
        urgency=UrgencyLevel.medium,
        confidence=0.42,
        suspected_harm_type="구체적인 피해 유형 추가 확인 필요",
        emotional_support_message=(
            "현재 문장만으로 피해 유형을 단정하지 않고, "
            "필요한 정보를 조금 더 확인하겠습니다."
        ),
        situation_summary=(
            "규칙 기반 분석에서 충분한 상황 신호가 확인되지 않았습니다."
        ),
        immediate_actions=[
            ActionItem(
                title="발생한 일을 시간순으로 정리하기",
                detail="언제, 어디서, 누가, 무엇을 요구하거나 했는지 적어보세요.",
                priority=1,
            ),
            ActionItem(
                title="민감정보는 추가로 보내지 않기",
                detail="인증번호, 비밀번호, 주민번호와 전체 계좌번호는 입력하지 마세요.",
                priority=2,
            ),
            ActionItem(
                title="긴급한 위험이면 112에 연락하기",
                detail="현재 신체 위험이 있다면 추가 입력보다 긴급신고를 우선하세요.",
                priority=3,
            ),
        ],
        safe_search_queries=[
            "경찰청 사이버범죄 상담",
            "한국인터넷진흥원 118 상담",
        ],
        recommended_agencies=[POLICE, KISA_118],
        requires_human_review=True,
        safety_notice=(
            "낮은 규칙 일치도는 안전하다는 뜻이 아닙니다. "
            "이 결과는 범죄 확정이나 법률 판단을 의미하지 않습니다."
        ),
    )
