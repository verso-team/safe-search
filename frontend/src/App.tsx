import { FormEvent, useState } from "react";
import nasumiAi from "./assets/nasumi-ai.png";
import { analyzeClickbait } from "./lib/api";
import type { ClickbaitLabel, ClickbaitResult } from "./types/clickbait";

const clickbaitLabels: Record<ClickbaitLabel, string> = {
  normal: "일반",
  suspicious: "의심",
  clickbait: "클릭베이트",
};

export function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<ClickbaitResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!input.trim()) return;
    setIsLoading(true);
    setError("");
    try {
      setResult(await analyzeClickbait(input.trim()));
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
              <div className="eyebrow">TRUSTWORTHY AI · CLICKBAIT CHECK</div>
              <h1>나섬이와 함께<br /><em>낚시성 제목</em> 확인해요</h1>
              <p className="lead">
                뉴스 제목을 입력하면 클릭 유도 표현과 판단 근거를 투명하게 알려드릴게요.
              </p>
              <div className="service-points">
                <span>✓ 판단 근거 공개</span>
                <span>✓ 불확실성 표시</span>
                <span>✓ 필요 시 인간 검토</span>
              </div>
            </div>
            <div className="nasumi-panel">
              <img
                className="nasumi-character large"
                src={nasumiAi}
                alt="AI 안전 안내 마스코트 나섬이"
              />
              <p><strong>이 제목, 믿어도 될까요?</strong><br />나섬이가 근거와 함께 확인할게요.</p>
            </div>
          </section>

          <form className="situation-form" onSubmit={handleSubmit}>
            <div className="form-title">
              <span className="analysis-symbol" aria-hidden="true">⌕</span>
              <div>
                <label htmlFor="situation">뉴스 제목을 확인해요</label>
                <p className="field-hint">제목을 입력하고 클릭베이트 가능성을 분석해보세요.</p>
              </div>
            </div>
            <div className="search-input-wrap">
              <textarea
                id="situation"
                value={input}
                onChange={(event) => setInput(event.target.value)}
                placeholder="예: 충격! 아무도 몰랐던 비밀, 지금 확인하세요"
                maxLength={5000}
                rows={5}
              />
              <button type="submit" disabled={!input.trim() || isLoading}>
                {isLoading ? "분석 중…" : "제목 분석하기 →"}
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
              <article><span className="quick-icon shield">◆</span><strong>제목 분석</strong><p>과장과 클릭 유도 표현을 확인해요</p></article>
              <article><span className="quick-icon counsel">◎</span><strong>판단 근거</strong><p>AI가 본 표현과 가중치를 공개해요</p></article>
              <article id="official-help"><span className="quick-icon agency">▦</span><strong>인간 검토</strong><p>애매한 결과는 사람이 다시 확인해요</p></article>
            </div>
          </section>

          <section className="suggestions">
            <div className="section-heading">
              <div><span>SAFE KEYWORDS</span><h2>추천 검색어</h2></div>
            </div>
            <div className="suggestion-grid">
              {["충격! 지금 안 보면 후회합니다", "서울시 폭염 대응 계획 발표", "단 3일 만에 달라진 놀라운 비밀", "정부, 내년도 예산안 공개"].map((query) => (
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
              <div><span className="recent-icon">▤</span><strong>건강 정보 기사 제목</strong><time>15:30</time><b>일반</b></div>
              <div><span className="recent-icon lock">▣</span><strong>연예 뉴스 과장 표현</strong><time>11:20</time><b className="reviewing">의심</b></div>
              <div><span className="recent-icon search">⌕</span><strong>투자 정보 홍보 제목</strong><time>09:10</time><b className="reviewing">검토 중</b></div>
            </div>
          </section>

          <div className="emergency-banner">
            <span className="phone-icon">✓</span>
            <div><strong>결과보다 근거를 확인하세요</strong><span>AI 판단은 참고 자료이며 중요한 결정은 사람이 최종 검토합니다.</span></div>
            <a href="#analysis" aria-label="새 제목 분석하기">→</a>
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
  result: ClickbaitResult;
  onReset: () => void;
}) {
  const scorePercent = Math.round(result.score * 100);
  const confidencePercent = Math.round(result.confidence * 100);

  return (
    <section className="result-page">
      <button className="text-button" onClick={onReset}>← 다른 제목 분석하기</button>

      <div className="nasumi-guide compact">
        <img
          className="nasumi-character"
          src={nasumiAi}
          alt="AI 안전 안내 마스코트 나섬이"
        />
        <p><strong>분석이 완료됐어요.</strong><br />결론뿐 아니라 어떤 표현을 근거로 판단했는지 함께 확인해주세요.</p>
      </div>

      <section className="result-section">
        <h2>클릭베이트 분석 결과</h2>
        <div className="summary-card">
          <div>
            <span className="meta-label">AI 분류</span>
            <h2>{clickbaitLabels[result.label]}</h2>
          </div>
          <span className={`urgency-badge ${result.label}`}>
            위험도 {scorePercent}%
          </span>
          <p>{result.summary}</p>
          <div className="confidence">
            <div><span>분석 신뢰도</span><strong>{confidencePercent}%</strong></div>
            <progress value={result.confidence} max={1} />
            <small>
              모델: {result.modelProvider} / {result.modelName} · 정책: {result.policyVersion}
              <br />추적 ID: {result.traceId} · 입력 해시: {result.inputSha256.slice(0, 20)}…
              {result.fallbackUsed && <><br />로컬 모델 오류로 기준선 폴백을 사용했습니다.</>}
            </small>
          </div>
        </div>
      </section>

      <section className="result-section">
        <h2>판단 근거</h2>
        {result.evidence.length ? (
          <ol className="action-list">
            {result.evidence.map((item, index) => (
              <li key={`${item.indicator}-${item.excerpt}`}>
                <span>{index + 1}</span>
                <div>
                  <strong>{item.indicator}</strong>
                  <p>발견된 표현: “{item.excerpt}” · 가중치 {Math.round(item.weight * 100)}%</p>
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <div className="human-review normal-result">
            <strong>뚜렷한 클릭 유도 표현이 없어요.</strong>
            <p>본문의 사실성이나 출처 신뢰도까지 보장하는 결과는 아닙니다.</p>
          </div>
        )}
      </section>

      <section className="result-section">
        <h2>모델의 한계</h2>
        <div className="query-list">
          {result.limitations.map((limitation) => (
            <div className="limitation-item" key={limitation}>
              <span aria-hidden="true">!</span>{limitation}
            </div>
          ))}
        </div>
      </section>

      <div className={`human-review ${result.requiresHumanReview ? "" : "normal-result"}`}>
        <strong>{result.requiresHumanReview ? "사람의 추가 확인이 필요해요" : "자동 분석 범위에서 판단이 안정적이에요"}</strong>
        <p>
          {result.humanReviewReason ??
            "그래도 중요한 판단 전에는 기사 원문, 작성자, 게시 시각과 다른 출처를 함께 확인해주세요."}
        </p>
      </div>
    </section>
  );
}
