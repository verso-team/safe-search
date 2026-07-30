import type {
  Agency,
  AnalysisResult,
  EmotionalState,
  RiskLevel,
  UserIntent,
} from "../types/analysis";

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
