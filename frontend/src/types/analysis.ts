export type RiskLevel = "low" | "medium" | "high" | "critical";
export type UserIntent =
  | "information"
  | "emotional_support"
  | "reporting"
  | "evidence"
  | "emergency"
  | "legal_question"
  | "institution"
  | "secondary_damage"
  | "unknown";
export type EmotionalState =
  | "stable"
  | "anxious"
  | "confused"
  | "fearful"
  | "panic"
  | "high_distress";

export interface ActionItem {
  title: string;
  detail: string;
  priority: 1 | 2 | 3;
}

export interface Agency {
  id: string;
  name: string;
  role: string;
  phone?: string;
  website: string;
  isOfficial: boolean;
}

export interface AnalysisResult {
  primaryIntent: UserIntent;
  secondaryIntents: UserIntent[];
  emotionalState: EmotionalState;
  urgency: RiskLevel;
  confidence: number;
  suspectedHarmType: string;
  emotionalSupportMessage: string;
  situationSummary: string;
  immediateActions: ActionItem[];
  safeSearchQueries: string[];
  recommendedAgencies: Agency[];
  requiresHumanReview: boolean;
  safetyNotice?: string;
}
