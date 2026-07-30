import { FormEvent, ReactNode, useState } from "react";
import nasumiAi from "./assets/nasumi-ai.png";
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
      <div className="official-bar">
        <div><span className="flag-mark">태극</span> 이 서비스는 디지털 범죄 피해 지원을 위한 공익 프로젝트입니다.</div>
      </div>
      <header className="site-header">
        <a className="brand" href="/" aria-label="SAFE SEARCH 홈">
          <span className="brand-mark">S</span>
          <span><strong>SAFE:SEARCH</strong><small>피해자 안전정보 안내</small></span>
        </a>
        <nav aria-label="주요 메뉴">
          <a href="#analysis">안전 분석</a>
          <a href="#quick-services">피해 대응</a>
          <a href="#official-help">공식기관</a>
        </nav>
        <button className="header-help" type="button">이용안내</button>
      </header>

      {!result ? (
        <section className="input-page">
          <section className="public-hero" id="analysis">
            <div className="hero-copy">
              <div className="eyebrow">디지털 범죄 피해 지원</div>
              <h1>혼자 판단하지 않아도 됩니다.</h1>
              <p className="lead">
                현재 상황을 알려주시면 위험 신호를 확인하고, 지금 필요한 대응과
                검증된 공식기관을 순서대로 안내합니다.
              </p>
              <div className="service-points">
                <span>✓ 개인정보 최소 수집</span>
                <span>✓ 공식기관 정보 우선</span>
                <span>✓ 필요 시 전문가 검토</span>
              </div>
            </div>
            <div className="nasumi-panel">
              <img
                className="nasumi-character large"
                src={nasumiAi}
                alt="AI 안전 안내 마스코트 나섬이"
              />
              <p><strong>나섬이가 안내할게요.</strong><br />필요한 정보부터 차근차근 확인해요.</p>
            </div>
          </section>

          <form className="situation-form" onSubmit={handleSubmit}>
            <div className="form-title">
              <span className="step-number">1</span>
              <div>
                <label htmlFor="situation">피해 상황 안전 분석</label>
                <p className="field-hint">상황을 설명하면 필요한 지원을 한 번에 찾아드립니다.</p>
              </div>
            </div>
            <div className="search-input-wrap">
              <textarea
                id="situation"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="예: 영상이 퍼지고 있는데 어디로 신고해야 할지 모르겠어요."
                maxLength={5000}
                rows={5}
              />
              <button type="submit" disabled={!input.trim() || isLoading}>
                {isLoading ? "분석 중…" : "분석하기"}
              </button>
            </div>
            <div className="form-meta">
              <p>이름, 연락처, 계좌번호 등 개인정보는 입력하지 마세요.</p>
              <span>{input.length.toLocaleString()} / 5,000</span>
            </div>
            {error && <p className="error-message" role="alert">{error}</p>}
          </form>

          <section className="quick-services" id="quick-services">
            <div className="section-heading">
              <div><span>자주 찾는 피해 대응</span><h2>지금 바로 확인하세요</h2></div>
              <small>상황에 맞는 안전한 대응 원칙입니다.</small>
            </div>
            <div className="quick-grid">
              <article><span className="quick-icon">112</span><strong>긴급 신고</strong><p>신체 위험이 있다면 안전한 장소로 이동 후 신고</p></article>
              <article><span className="quick-icon">01</span><strong>증거 보존</strong><p>대화, 계정, URL, 송금 내역을 삭제하지 않고 보존</p></article>
              <article><span className="quick-icon">02</span><strong>추가 피해 차단</strong><p>추가 송금이나 사진·개인정보 요구에 응하지 않기</p></article>
              <article id="official-help"><span className="quick-icon">03</span><strong>공식기관 상담</strong><p>경찰청·KISA·피해자지원센터로 안전하게 연결</p></article>
            </div>
          </section>

          <div className="emergency-banner">
            <strong>긴급한 도움이 필요하신가요?</strong>
            <span>즉각적인 생명·신체 위험이 있다면 분석보다 112 신고가 우선입니다.</span>
            <a href="tel:112">112 전화하기</a>
          </div>
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
        <img
          className="nasumi-character"
          src={nasumiAi}
          alt="AI 안전 안내 마스코트 나섬이"
        />
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
