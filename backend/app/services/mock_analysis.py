from app.schemas.analysis import (
    ActionItem,
    Agency,
    AnalyzeResponse,
    EmotionalState,
    UrgencyLevel,
    UserIntent,
)


POLICE = Agency(
    id="police",
    name="경찰청",
    role="긴급 신고 및 사이버범죄 신고",
    phone="112",
    website="https://ecrm.police.go.kr",
)

D4U = Agency(
    id="d4u",
    name="디지털성범죄피해자지원센터",
    role="상담, 삭제 지원, 수사·법률·의료 연계",
    phone="02-735-8994",
    website="https://d4u.stop.or.kr",
)


def analyze_safely(text: str) -> AnalyzeResponse:
    """결정론적 Mock 분석기.

    긴급 신호의 정보 우선순위와 구조화 응답 계약을 검증하기 위한 구현이며,
    범죄 여부나 법률 결론을 확정하지 않는다.
    """
    normalized = text.strip()
    critical_terms = ("죽", "흉기", "찾아왔", "위협", "다칠")
    if any(term in normalized for term in critical_terms):
        return _critical_result()
    return _high_risk_result()


def _critical_result() -> AnalyzeResponse:
    return AnalyzeResponse(
        primary_intent=UserIntent.emergency,
        secondary_intents=[UserIntent.reporting],
        emotional_state=EmotionalState.panic,
        urgency=UrgencyLevel.critical,
        confidence=0.93,
        suspected_harm_type="즉각적인 신체 안전 위협 가능성",
        emotional_support_message="지금은 안전을 확보하는 것이 가장 중요합니다.",
        situation_summary="즉각적인 대응이 필요한 신체 위험 신호가 감지되었습니다.",
        immediate_actions=[
            ActionItem(title="안전한 장소로 이동하기", detail="주변 사람이나 열린 공공장소로 이동하세요.", priority=1),
            ActionItem(title="112에 연락하기", detail="통화가 어렵다면 주변 사람에게 도움을 요청하세요.", priority=2),
            ActionItem(title="위치 공유하기", detail="신뢰할 수 있는 사람에게 현재 위치를 알리세요.", priority=3),
        ],
        safe_search_queries=["경찰청 긴급 신고", "범죄피해자 안전 지원"],
        recommended_agencies=[POLICE],
        requires_human_review=True,
        safety_notice="지금 생명이나 신체가 위험하다면 안전한 장소로 이동하고 112에 연락하세요.",
    )


def _high_risk_result() -> AnalyzeResponse:
    return AnalyzeResponse(
        primary_intent=UserIntent.reporting,
        secondary_intents=[UserIntent.information, UserIntent.evidence],
        emotional_state=EmotionalState.anxious,
        urgency=UrgencyLevel.high,
        confidence=0.87,
        suspected_harm_type="디지털 성범죄·유포 위협 가능성",
        emotional_support_message="혼자 해결하려고 하지 않아도 됩니다. 지금 할 수 있는 안전한 조치부터 확인해볼게요.",
        situation_summary="신속한 증거 보존과 공식기관 상담이 필요한 상황으로 보입니다.",
        immediate_actions=[
            ActionItem(title="추가 요구에 응하지 않기", detail="송금하거나 새로운 정보를 보내지 마세요.", priority=1),
            ActionItem(title="대화와 계정 정보 보존하기", detail="메시지, URL, 계정명과 송금 내역을 보존하세요.", priority=2),
            ActionItem(title="공식기관에 상담·신고하기", detail="지원센터 또는 경찰에 현재 상황을 알려주세요.", priority=3),
        ],
        safe_search_queries=["디지털 성범죄 피해자 지원센터", "영상 유포 피해 신고 방법", "사이버범죄 신고 절차"],
        recommended_agencies=[D4U, POLICE],
        requires_human_review=True,
        safety_notice="분석은 법률적 판단이나 범죄 확정을 의미하지 않습니다.",
    )
