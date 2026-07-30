import type {
  Agency,
  AnalysisResult,
  EmotionalState,
  RiskLevel,
  UserIntent,
} from "../types/analysis";
import type { ClickbaitResult } from "../types/clickbait";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

interface AnalyzeResponse {
  primary_intent: UserIntent;
  secondary_intents: UserIntent[];
  emotional_state: EmotionalState;
  urgency: RiskLevel;
  confidence: number;
  suspected_harm_type: string;
  emotional_support_message: string;
  situation_summary: string;
  immediate_actions: AnalysisResult["immediateActions"];
  safe_search_queries: string[];
  recommended_agencies: Array<Omit<Agency, "isOfficial"> & { is_official: boolean }>;
  requires_human_review: boolean;
  safety_notice?: string;
}

export async function analyzeSafety(text: string): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    throw new Error("분석을 완료하지 못했습니다. 잠시 후 다시 시도해주세요.");
  }

  const data = (await response.json()) as AnalyzeResponse;
  return {
    primaryIntent: data.primary_intent,
    secondaryIntents: data.secondary_intents,
    emotionalState: data.emotional_state,
    urgency: data.urgency,
    confidence: data.confidence,
    suspectedHarmType: data.suspected_harm_type,
    emotionalSupportMessage: data.emotional_support_message,
    situationSummary: data.situation_summary,
    immediateActions: data.immediate_actions.slice(0, 3),
    safeSearchQueries: data.safe_search_queries,
    recommendedAgencies: data.recommended_agencies
      .filter((agency) => agency.is_official)
      .map(({ is_official, ...agency }) => ({ ...agency, isOfficial: is_official })),
    requiresHumanReview: data.requires_human_review,
    safetyNotice: data.safety_notice,
  };
}

interface ClickbaitResponse {
  trace_id: string;
  input_sha256: string;
  policy_version: string;
  label: ClickbaitResult["label"];
  score: number;
  confidence: number;
  summary: string;
  evidence: ClickbaitResult["evidence"];
  model_provider: ClickbaitResult["modelProvider"];
  model_name: string;
  fallback_used: boolean;
  decision_thresholds: Record<string, number>;
  requires_human_review: boolean;
  human_review_reason?: string;
  limitations: string[];
}

export async function analyzeClickbait(title: string): Promise<ClickbaitResult> {
  const response = await fetch(`${API_BASE_URL}/api/v1/clickbait/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  if (!response.ok) {
    throw new Error("클릭베이트 분석을 완료하지 못했습니다. 잠시 후 다시 시도해주세요.");
  }

  const data = (await response.json()) as ClickbaitResponse;
  return {
    traceId: data.trace_id,
    inputSha256: data.input_sha256,
    policyVersion: data.policy_version,
    label: data.label,
    score: data.score,
    confidence: data.confidence,
    summary: data.summary,
    evidence: data.evidence,
    modelProvider: data.model_provider,
    modelName: data.model_name,
    fallbackUsed: data.fallback_used,
    decisionThresholds: data.decision_thresholds,
    requiresHumanReview: data.requires_human_review,
    humanReviewReason: data.human_review_reason,
    limitations: data.limitations,
  };
}

export async function submitHumanReview(
  result: ClickbaitResult,
  finalLabel: ClickbaitResult["label"],
  reason: string,
): Promise<{ reviewId: string; disagreesWithAi: boolean }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/clickbait/reviews`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      trace_id: result.traceId,
      input_sha256: result.inputSha256,
      ai_label: result.label,
      final_label: finalLabel,
      reason,
      reviewer_role: "user",
    }),
  });

  if (!response.ok) {
    throw new Error("검토 의견을 저장하지 못했습니다.");
  }
  const data = (await response.json()) as {
    review_id: string;
    disagrees_with_ai: boolean;
  };
  return {
    reviewId: data.review_id,
    disagreesWithAi: data.disagrees_with_ai,
  };
}
