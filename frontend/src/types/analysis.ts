export type RiskLevel = "low" | "medium" | "high" | "critical";

export interface AnalysisResult {
  crimeType: string;
  urgency: RiskLevel;
  confidence: number;
  safeQueries: string[];
  recommendedAgencies: string[];
  requiresHumanReview: boolean;
}
