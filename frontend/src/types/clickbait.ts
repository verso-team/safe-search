export type ClickbaitLabel = "normal" | "suspicious" | "clickbait";

export interface ClickbaitEvidence {
  indicator: string;
  excerpt: string;
  weight: number;
}

export interface ClickbaitResult {
  traceId: string;
  inputSha256: string;
  policyVersion: string;
  label: ClickbaitLabel;
  score: number;
  confidence: number;
  summary: string;
  evidence: ClickbaitEvidence[];
  modelProvider: "heuristic" | "ollama" | "skax";
  modelName: string;
  fallbackUsed: boolean;
  decisionThresholds: Record<string, number>;
  requiresHumanReview: boolean;
  humanReviewReason?: string;
  limitations: string[];
}
