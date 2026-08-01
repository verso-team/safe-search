from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Pattern

logger = logging.getLogger("app.pii")


class PIICategory(str, Enum):
    resident_registration_number = "resident_registration_number"
    email = "email"
    phone = "phone"
    payment_card = "payment_card"
    bank_account = "bank_account"
    authentication_code = "authentication_code"

    @property
    def display_name(self) -> str:
        return {
            PIICategory.resident_registration_number: "주민등록번호",
            PIICategory.email: "이메일",
            PIICategory.phone: "전화번호",
            PIICategory.payment_card: "카드번호",
            PIICategory.bank_account: "계좌번호",
            PIICategory.authentication_code: "인증번호",
        }[self]

    @property
    def placeholder(self) -> str:
        return {
            PIICategory.resident_registration_number: "[주민등록번호]",
            PIICategory.email: "[이메일]",
            PIICategory.phone: "[전화번호]",
            PIICategory.payment_card: "[카드번호]",
            PIICategory.bank_account: "[계좌번호]",
            PIICategory.authentication_code: "[인증번호]",
        }[self]


@dataclass(frozen=True)
class PIIRedactionResult:
    """원문을 보관하지 않는 마스킹 결과."""

    redacted_text: str
    counts: dict[PIICategory, int]

    @property
    def total_count(self) -> int:
        return sum(self.counts.values())

    @property
    def has_sensitive_data(self) -> bool:
        return self.total_count > 0

    @property
    def category_names(self) -> tuple[str, ...]:
        return tuple(
            category.display_name
            for category in PIICategory
            if self.counts.get(category, 0) > 0
        )


@dataclass(frozen=True)
class _RedactionRule:
    category: PIICategory
    pattern: Pattern[str]
    replacement: str | Callable[[re.Match[str]], str]


def _context_replacement(
    category: PIICategory,
) -> Callable[[re.Match[str]], str]:
    def replace(match: re.Match[str]) -> str:
        return f"{match.group('label')}{category.placeholder}"

    return replace


# 탐지 순서가 중요하다.
# 주민등록번호·카드번호처럼 길이가 긴 형식을 전화번호보다 먼저 치환한다.
_RULES: tuple[_RedactionRule, ...] = (
    _RedactionRule(
        PIICategory.resident_registration_number,
        re.compile(r"(?<!\d)\d{6}\s*[- ]?\s*[1-8]\d{6}(?!\d)"),
        PIICategory.resident_registration_number.placeholder,
    ),
    _RedactionRule(
        PIICategory.email,
        re.compile(
            r"(?<![\w.+-])[\w.+-]+@(?:[\w-]+\.)+[A-Za-z]{2,63}(?![\w.-])",
            re.IGNORECASE,
        ),
        PIICategory.email.placeholder,
    ),
    _RedactionRule(
        PIICategory.payment_card,
        re.compile(r"(?<!\d)(?:\d{4}[- ]?){3}\d{4}(?!\d)"),
        PIICategory.payment_card.placeholder,
    ),
    _RedactionRule(
        PIICategory.phone,
        re.compile(
            r"(?<!\d)(?:"
            r"01[016789][-\s]?\d{3,4}[-\s]?\d{4}"
            r"|02[-\s]?\d{3,4}[-\s]?\d{4}"
            r"|0(?:3[1-3]|4[1-4]|5[1-5]|6[1-4]|70)"
            r"[-\s]?\d{3,4}[-\s]?\d{4}"
            r")(?!\d)"
        ),
        PIICategory.phone.placeholder,
    ),
    # 계좌번호는 일반 숫자·날짜 오탐을 줄이기 위해
    # '계좌번호', '통장번호' 같은 문맥이 있을 때만 치환한다.
    _RedactionRule(
        PIICategory.bank_account,
        re.compile(
            r"(?P<label>(?:계좌(?:번호)?|통장(?:번호)?|입금\s*계좌|송금\s*계좌)"
            r"\s*(?:은|는|:|：)?\s*)"
            r"(?P<value>(?:\d{8,20}|\d{2,6}(?:[-\s]\d{2,6}){1,4}))",
            re.IGNORECASE,
        ),
        _context_replacement(PIICategory.bank_account),
    ),
    # 짧은 숫자를 무조건 가리지 않고 인증 관련 표현 뒤의 4~8자리만 치환한다.
    _RedactionRule(
        PIICategory.authentication_code,
        re.compile(
            r"(?P<label>(?:인증번호|인증코드|OTP|보안코드|일회용\s*비밀번호)"
            r"\s*(?:은|는|:|：)?\s*)"
            r"(?P<value>\d{4,8})(?!\d)",
            re.IGNORECASE,
        ),
        _context_replacement(PIICategory.authentication_code),
    ),
)


def redact_sensitive_text(text: str) -> PIIRedactionResult:
    """민감정보를 정해진 placeholder로 치환한다.

    반환 객체는 원문이나 원래 민감정보 값을 보관하지 않는다.
    """

    redacted = text
    counts: dict[PIICategory, int] = {}

    for rule in _RULES:
        redacted, count = rule.pattern.subn(rule.replacement, redacted)
        if count:
            counts[rule.category] = counts.get(rule.category, 0) + count

    return PIIRedactionResult(
        redacted_text=redacted,
        counts=counts,
    )


def build_redaction_notice(
    result: PIIRedactionResult,
) -> str | None:
    if not result.has_sensitive_data:
        return None

    categories = ", ".join(result.category_names)
    return (
        f"입력에서 민감정보 {result.total_count}건({categories})을 "
        "분석 전에 마스킹했습니다. "
        "원문은 분석 결과와 애플리케이션 로그에 기록하지 않습니다."
    )


def log_redaction_summary(
    result: PIIRedactionResult,
) -> None:
    """원문이나 실제 값을 제외한 통계만 기록한다."""

    if not result.has_sensitive_data:
        return

    logger.info(
        "PII redaction applied total=%d categories=%s",
        result.total_count,
        ",".join(category.value for category in result.counts),
    )
