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
              <div className="eyebrow">AI와 함께, 더 안전한 선택</div>
              <h1>나섬이와 함께<br /><em>안전한 검색</em> 시작해요</h1>
              <p className="lead">
                궁금한 상황을 입력하면 필요한 정보와 도움을 쉽고 안전하게 안내해드릴게요.
              </p>
              <div className="service-points">
                <span>✓ 개인정보 보호</span>
                <span>✓ 공식기관 정보 우선</span>
                <span>✓ 24시간 AI 안내</span>
              </div>
            </div>
            <div className="nasumi-panel">
              <img
                className="nasumi-character large"
                src={nasumiAi}
                alt="AI 안전 안내 마스코트 나섬이"
              />
              <p><strong>무엇이 궁금한가요?</strong><br />나섬이가 차근차근 함께 확인할게요.</p>
            </div>
          </section>

          <form className="situation-form" onSubmit={handleSubmit}>
            <div className="form-title">
              <span className="analysis-symbol" aria-hidden="true">⌕</span>
              <div>
                <label htmlFor="situation">도움이 필요해요</label>
                <p className="field-hint">상황을 입력하고 AI 안전 분석을 받아보세요.</p>
              </div>
            </div>
            <div className="search-input-wrap">
              <textarea
                id="situation"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="예: 모르는 사람이 사진을 보내라고 협박해요. 어떻게 해야 하나요?"
                maxLength={5000}
                rows={5}
              />
              <button type="submit" disabled={!input.trim() || isLoading}>
                {isLoading ? "분석 중…" : "안전 분석하기 →"}
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
              <div><span>QUICK SERVICE</span><h2>빠르게 이용하기</h2></div>
              <small>필요한 도움으로 바로 이동하세요.</small>
            </div>
            <div className="quick-grid">
              <article><span className="quick-icon shield">◆</span><strong>안전 검색</strong><p>위험한 정보를 걸러내고 확인해요</p></article>
              <article><span className="quick-icon counsel">◎</span><strong>상담·신고 안내</strong><p>내 상황은 어디에 문의할까요?</p></article>
              <article id="official-help"><span className="quick-icon agency">▦</span><strong>공식기관 정보</strong><p>검증된 기관과 바로 연결해요</p></article>
            </div>
          </section>

          <section className="suggestions">
            <div className="section-heading">
              <div><span>SAFE KEYWORDS</span><h2>추천 검색어</h2></div>
            </div>
            <div className="suggestion-grid">
              {["불법촬영 피해 대응 방법", "디지털 성범죄 신고 절차", "사이버 스토킹 대처 방법", "온라인 사기 피해 지원"].map((query) => (
                <button key={query} type="button" onClick={() => setInput(query)}>
                  <span aria-hidden="true">⌕</span>{query}
                </button>
              ))}
            </div>
          </section>

          <section className="recent-analysis">
            <div className="section-heading">
              <div><span>MY SAFETY</span><h2>최근 분석</h2></div>
              <button type="button">전체 보기 ›</button>
            </div>
            <div className="recent-list">
              <div><span className="recent-icon">▤</span><strong>디지털 성범죄 관련 상담</strong><time>15:30</time><b>완료</b></div>
              <div><span className="recent-icon lock">▣</span><strong>불법 촬영 의심 상황</strong><time>11:20</time><b>완료</b></div>
              <div><span className="recent-icon search">⌕</span><strong>온라인 스토킹 피해</strong><time>09:10</time><b className="reviewing">검토 중</b></div>
            </div>
          </section>

          <div className="emergency-banner">
            <span className="phone-icon">☎</span>
            <div><strong>지금 바로 도움 요청</strong><span>긴급 상황 시 112로 연결됩니다.</span></div>
            <a href="tel:112" aria-label="112 전화하기">→</a>
          </div>

          <nav className="bottom-nav" aria-label="모바일 메뉴">
            <a className="active" href="/"><span>⌂</span>홈</a>
            <a href="#analysis"><span>◷</span>분석 내역</a>
            <a className="nasumi-home" href="#analysis"><img src={nasumiAi} alt="" /></a>
            <a href="#official-help"><span>♧</span>상담·신고</a>
            <a href="#top"><span>♙</span>마이페이지</a>
          </nav>
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
