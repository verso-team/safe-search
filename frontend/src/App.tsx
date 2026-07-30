import { FormEvent, ReactNode, useState } from "react";
import { analyzeSafety } from "./lib/api";
import type { AnalysisResult, RiskLevel } from "./types/analysis";

const urgencyLabels: Record<RiskLevel, string> = {
  low: "낮음",
  medium: "주의",
  high: "높음",
  critical: "긴급",
};

export function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!input.trim()) return;
    setIsLoading(true);
    setError("");
    try {
      setResult(await analyzeSafety(input.trim()));
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "분석 중 오류가 발생했습니다.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="site-header">
        <a className="brand" href="/" aria-label="SAFE SEARCH 홈">
          <span className="brand-mark">S</span>
          SAFE:SEARCH
        </a>
        <span className="header-caption">AI Safety Guide</span>
      </header>

      {!result ? (
        <section className="input-page">
          <div className="eyebrow">디지털 범죄 피해 지원</div>
          <h1>지금 필요한 안전한 다음 행동을 함께 찾습니다.</h1>
          <p className="lead">
            범죄 여부를 단정하지 않고, 위험 신호와 정서 상태를 확인해 검증된 지원
            경로를 안내합니다.
          </p>

          <div className="nasumi-guide">
            <div className="nasumi-avatar" aria-label="나섬이">나</div>
            <p>당황하지 않아도 괜찮아요.<br />필요한 것부터 하나씩 확인해볼게요.</p>
          </div>

          <form className="situation-form" onSubmit={handleSubmit}>
            <label htmlFor="situation">어떤 상황인지 알려주세요</label>
            <p className="field-hint">이름, 연락처, 계좌번호 같은 개인정보는 적지 않아도 됩니다.</p>
            <textarea
              id="situation"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="예: 영상이 퍼지고 있는데 어디로 신고해야 할지 모르겠어요."
              maxLength={5000}
              rows={7}
            />
            <div className="form-footer">
              <span>{input.length.toLocaleString()} / 5,000</span>
              <button type="submit" disabled={!input.trim() || isLoading}>
                {isLoading ? "안전 신호를 확인하고 있어요…" : "안전하게 분석하기"}
              </button>
            </div>
            {error && <p className="error-message" role="alert">{error}</p>}
          </form>

          <p className="emergency-note">즉각적인 생명·신체 위험이 있다면 112에 먼저 연락하세요.</p>
        </section>
      ) : (
        <ResultView result={result} onReset={() => setResult(null)} />
      )}
    </main>
  );
}

function ResultView({
  result,
  onReset,
}: {
  result: AnalysisResult;
  onReset: () => void;
}) {
  return (
    <section className="result-page">
      <button className="text-button" onClick={onReset}>← 상황 다시 입력하기</button>
      {result.safetyNotice && (
        <div className={`safety-notice ${result.urgency}`} role="alert">
          <strong>{result.urgency === "critical" ? "긴급 안내" : "안전 안내"}</strong>
          <span>{result.safetyNotice}</span>
        </div>
      )}

      <div className="nasumi-guide compact">
        <div className="nasumi-avatar" aria-label="나섬이">나</div>
        <p>{result.emotionalSupportMessage}</p>
      </div>

      <ResultSection title="지금 확인된 상황">
        <div className="summary-card">
          <div>
            <span className="meta-label">예상 피해 유형</span>
            <h2>{result.suspectedHarmType}</h2>
          </div>
          <span className={`urgency-badge ${result.urgency}`}>
            {urgencyLabels[result.urgency]}
          </span>
          <p>{result.situationSummary}</p>
          <div className="confidence">
            <div><span>분석 신뢰도</span><strong>{Math.round(result.confidence * 100)}%</strong></div>
            <progress value={result.confidence} max={1} />
            <small>신뢰도가 낮거나 긴급한 상황은 전문가 검토로 연결합니다.</small>
          </div>
        </div>
      </ResultSection>

      <ResultSection title="지금 먼저 해주세요">
        <ol className="action-list">
          {result.immediateActions.map((action) => (
            <li key={`${action.priority}-${action.title}`}>
              <span>{action.priority}</span>
              <div><strong>{action.title}</strong><p>{action.detail}</p></div>
            </li>
          ))}
        </ol>
      </ResultSection>

      <ResultSection title="안전하게 검색하기">
        <div className="query-list">
          {result.safeSearchQueries.map((query) => (
            <a
              key={query}
              href={`https://www.google.com/search?q=${encodeURIComponent(query)}`}
              target="_blank"
              rel="noreferrer"
            >
              <span aria-hidden="true">⌕</span>{query}
            </a>
          ))}
        </div>
      </ResultSection>

      <ResultSection title="도움을 받을 수 있는 곳">
        <div className="agency-list">
          {result.recommendedAgencies.map((agency) => (
            <a key={agency.id} href={agency.website} target="_blank" rel="noreferrer">
              <div><strong>{agency.name}</strong><p>{agency.role}</p></div>
              <span>{agency.phone ?? "웹사이트"} ↗</span>
            </a>
          ))}
        </div>
      </ResultSection>

      <div className="human-review">
        <strong>{result.requiresHumanReview ? "추가 확인이 필요해요" : "자동 분석이 완료됐어요"}</strong>
        <p>
          {result.requiresHumanReview
            ? "전문가 검토가 필요한 사례로 표시했습니다. 공식기관 상담을 함께 이용해주세요."
            : "상황이 바뀌거나 불안이 커지면 다시 분석해주세요."}
        </p>
      </div>
    </section>
  );
}

function ResultSection({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return <section className="result-section"><h2>{title}</h2>{children}</section>;
}
