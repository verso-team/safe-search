"""이전 import 경로 호환용 모듈.

실제 분석 구현은 ``rule_based_analysis``에 있다.
"""

from app.services.rule_based_analysis import analyze_safely

__all__ = ["analyze_safely"]
