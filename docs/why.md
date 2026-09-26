# 왜 만들었나 · 상세 사용법

**한국어** · [English](#english)

README에서 덜어낸 배경과 사용 시나리오를 여기 둔다.

---

## 왜 만들었나

LLM에게 논문 초안을 맡겨 본 사람은 대개 문장 품질에는 만족한다. 학술 문체를 흉내 내는 일은 이제 어렵지 않다. 문제는 다른 데 있다.

**인용이 무너진다.** 그것도 눈에 잘 띄지 않는 방식으로.

- **유령 인용** — 본문에 `(Smith, 2019)`가 있는데 참고문헌 목록에는 없다. 혹은 그런 문헌이 아예 존재하지 않는다.
- **고아 출처** — 참고문헌 목록에는 있는데 본문 어디에서도 인용되지 않는다. 원고를 고치는 과정에서 문장은 지워지고 목록만 남는다.
- **출처 없는 실증 주장** — "선행연구는 ~을 보고한다"라고 써 놓고 그 자리에 인용이 0건이다. 독자가 검증할 방법이 없는 문장이다.

이런 결함은 문장을 읽어서는 안 잡힌다. **대조해야 잡힌다.** 본문의 인용을 하나씩 목록과 맞춰 보고, 목록의 항목을 하나씩 본문에서 되찾아봐야 나온다. 마감 직전에 사람이 가장 하기 싫은 일이고, 그래서 실제로 안 하게 되는 일이다.

논문에서 이 대가는 보고서보다 비싸다. 이론적 배경의 실증 주장에 인용이 없는 것은 동료심사에서 desk-reject 1순위로 꼽히는 결함이다. 본문과 참고문헌의 불일치는 논증의 문제가 아니라 성실성의 문제로 읽히기 쉽고, 한 번 그렇게 읽히면 나머지가 아무리 단단해도 회복이 어렵다.

**설계도 무너진다.** 이쪽은 더 늦게 발견된다.

보고서는 목차가 어긋나도 문단을 옮기면 어느 정도 수습된다. 논문은 그렇지 않다. RQ 한 줄이 이론틀을 정하고, 이론틀이 가설을 정하고, 가설이 변수와 조작적 정의를 정하고, 그것이 어떤 데이터를 어떤 기법으로 분석할지를 정한다. **이 사슬의 앞쪽이 어긋나면 뒤에서 한 분석은 정확해도 의미가 없다.** 데이터를 다 모으고 논문을 다 쓴 다음에야 "이 가설로는 이 데이터가 답을 못 한다"를 알게 되는 것이 최악이고, 실제로 자주 일어난다.

그래서 필요했던 것은 더 좋은 문장을 뽑는 프롬프트가 아니라 **두 개의 관문**이었다.

1. 조사·분석·집필에 착수하기 **전에**, RQ·가설·변수·방법이 서로 맞물리는지 판정하는 관문
2. 초안을 다 쓴 **뒤에**, 인용을 참고문헌과 전수 대조하는 관문

이 킷은 실제 논문을 쓰면서 그 관문들을 하나씩 붙여 만든 개인 하네스를 정리해 공개한 것이다. 게이트2는 실전 완주에서 **유령 인용 2건과 본문에 없는 고아 출처 1건**을 잡아냈다([verification-gates.md](verification-gates.md)의 적발 기록).

한 가지 더 있다. 정량 논문에는 일반 검수로 잡히지 않는 급소가 따로 있다. "유의한 증거 없음"을 "효과 없음"으로 단정하는 것, 처치 시점이 엇갈리는 DiD에서 표준 TWFE 편향 문헌을 인용하지 않는 것, 군집 수가 적은데 분석적 군집 표준오차를 그대로 쓰는 것 — 계산이 전부 맞아도 논문은 이 지점에서 무너진다. 그래서 계량서지·정량 논문 전용 검수 축(`scientometric-paper-review`)을 따로 뒀다.

---

## 순정 Claude Code와 무엇이 다른가 — 전체 표

**먼저 밝힐 것.** 이 저장소에는 이 킷에 대한 순정 대비 A/B 실측이 없다. 아래 표는 측정치가 아니라 구조 서술이다.

| | 순정 세션 | 이 킷 |
|---|---|---|
| 착수 | 요청받은 대로 바로 쓰기 시작 | RQ·가설·변수·조작적 정의·방법을 먼저 확정하고 **GO/조건부/NO-GO 판정**을 받는다 |
| 인용 점검 | 초안에 인용이 달린 채로 끝 | 본문↔참고문헌 **1:1 전수 대조**(부록 인용 포함), 출처 실재·접근성 확인, 인용 수치와 원문 대조 |
| 검수자 | 쓴 세션이 자기 글을 본다 | **다른 에이전트**가, **READ-ONLY**로, 디스크에서 원고를 다시 읽고 본다 |
| 데이터 없는 연구 | 통계적 표현을 그대로 흉내 낼 수 있다 | 가설이 **분석명제로 대체**되고 분석가가 팀에서 빠진다 |
| 남는 것 | 원고 파일 하나 | 설계·게이트 판정·근거장부·검수 기록이 **파일로 잔존** |

핵심은 마지막 두 줄이다. 검수자와 집필자가 같으면 자기 글을 자기가 통과시킨다. 그리고 판정이 파일로 남지 않으면 "이 인용은 확인된 것인가"를 나중에 되물을 방법이 없다.

설계 철학이 같은 자매 킷에는 **순정 대비 실측 A/B 감사**가 있다(같은 요청·같은 기반 모델로 양쪽을 돌리고 제3의 감사 세션이 인용 URL을 전수 열람). 정책연구 도메인의 수치이므로 이 킷으로 그대로 옮겨 읽어서는 안 되지만, 게이트 구조가 무엇을 바꾸는지는 참고가 된다 — [policy-research-kit / vanilla-vs-kit.md](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md).

---

## 게이트 상세

```
연구설계(designer: RQ·가설·변수·조작적정의·이론틀·방법·목차)
  → 🚦 게이트1: 설계검토 (reviewer 모드1 — GO / 조건부 / NO-GO)
  → ★ 목차·가설 사용자 승인 ← 여기서 당신이 개입한다
  → 근거조사(investigator, SLR) ∥ 데이터분석(analyst — 실증연구일 때만)
  → 집필(writer, APA7 논증형)
  → 🚦 게이트2: 초안검수 (reviewer 모드2 — 5축)
  → 교정·변환(finalizer: 한국어 교정교열 → .docx + .md)
```

**게이트가 두 번인 이유.** 두 실패의 성격이 다르기 때문이다. 게이트1은 *방향*을 막는다 — 검증 못 할 가설, 답 못 할 RQ, 확보 못 할 데이터를 착수 전에 걷어낸다. 게이트2는 *과신*을 막는다 — 다 쓰고 나면 초안이 그럴듯해 보여서 자기 인용을 의심하기 어려워진다.

검수자는 **집필자와 다른 에이전트**이고 READ-ONLY다. 본문을 직접 고치지도, 집필을 다른 에이전트에 재위임하지도 않는다. 자기가 쓴 것을 자기가 통과시키는 구조를 원천 차단한다. 두 게이트 모두 **개정 최대 2회**이고, 그래도 안 풀리는 항목은 "잔여 리스크"로 기록하고 진행한다 — 완벽주의로 파이프라인을 세우지 않는다.

**5축 초안검수** — ①RQ·가설 충족 ②근거·출처 무결성 ③논리 정합성 ④방법론 타당성 ⑤한국어 교열.

축2가 이 킷의 중심이다: 본문 인용 ↔ 참고문헌 1:1(유령·고아 색출), 출처의 실재·접근성(URL·DOI·KCI 식별자), 인용된 수치와 원문 내용의 일치, 환각 출처 플래그.

**정량 논문은 축이 다르다.** 서지계량·패널·DiD·이벤트스터디·정책평가 계량·귀무결과 논문은 `scientometric-paper-review`의 5축으로 내려간다 — 측정 무결성(DB 커버리지·계수 방식·정규화 분모의 불안정)·식별전략(평행추세·staggered DiD 편향·소표본 군집 추론)·추론 언어(부재-증거 ≠ 증거-부재)·문헌토대와 인용 충실성·도메인 구성타당도.

---

## 상세 사용법

말을 걸면 시작된다. 아래는 실제로 입력할 법한 문장과, 그때 무슨 일이 일어나는지다.

### 시나리오 1 — 실증연구 (데이터 있음)

```
플랫폼 노동자의 사회보험 사각지대에 대한 실증연구 논문을 설계부터 시작해줘.
설문 데이터 첨부했어. 국내 학술지 투고용, APA7.
```

첨부 파일이 `_workspace/00_input/`에 저장되고 인덱싱된다 — "이 파일은 데이터니까 분석가로, 이건 선행연구니까 조사관으로". 그다음 설계자가 연구유형을 **실증-양적**으로 판별하고 RQ 1~3개, 가설(독립·종속·매개·조절 변수 + 각 변수의 조작적 정의 + "어떤 결과가 나오면 지지인지"), 이론틀, 표집·측정·분석기법, 목차를 짠다.

여기서 파이프라인이 **처음 멈춘다.** 검토관이 "이 설계대로 가면 심사를 통과할 논문이 나오는가"를 GO/조건부/NO-GO로 판정하고, 그다음 당신에게 목차와 가설을 보여준다.

승인하면 조사관(선행연구 SLR)과 분석가(데이터 무결성 점검 → 가설검정)가 **병렬로** 움직이고, 집필 → 5축 검수 → 교정 → `.docx`로 이어진다.

### 시나리오 2 — 이론·문헌 연구 (데이터 없음)

```
데이터는 없어. 문헌고찰로 이론 논문을 쓸 거야.
```

설계 단계에서 통계 가설이 **분석명제(Proposition)**로 대체되고, 목차의 연구방법·분석결과 장이 쟁점별 논증 구조로 바뀐다. 그리고 **분석가가 팀에서 빠진다.** 데이터가 없는데 분석가를 붙여 두면 없는 수치를 만들어 낼 자리가 생기기 때문이다.

동봉 예제가 정확히 이 경로다 — [examples/socsci-paper-demo/](../examples/socsci-paper-demo/).

### 시나리오 3 — 이미 쓴 초안을 검수·보강

```
이 논문 초안 검수해줘. 인용부터 봐줘.
```

기존 초안을 주면 백지 집필이 아니라 **개정 모드**로 들어간다. 설계자가 초안의 구조에서 RQ·가설을 역설계해 보완하고, 조사관이 초안 주장의 출처를 검증·보강하고, 집필자가 그 초안을 베이스로 고친다.

인용 점검은 이렇게 돈다 — 본문의 모든 `(저자, 연도)`를 참고문헌 목록과 대조해 **유령**을 찾고, 목록의 모든 항목을 본문에서 역으로 찾아 **고아**를 찾는다(부록의 인용까지 포함). 남은 출처는 URL·DOI·KCI 식별자로 실재를 확인하고, 인용된 수치가 원문 내용과 맞는지 본다.

### 시나리오 4 — 계량·서지계량 논문 심사

```
이 DiD 논문을 심사자 관점에서 봐줘. 귀무결과가 걸린다.
```

검수가 `scientometric-paper-review`로 전환된다. 점검되는 것들 — 처치 시점이 엇갈리는데 staggered DiD 편향 문헌을 인용하고 자기 설계를 그 논의 안에 위치시켰는가, never-treated 통제군이 있는가(없다면 계수가 "깨끗한 반사실"이 아니라 "상대 편차"임을 인정했는가), 군집 수가 적은데 와일드 군집 부트스트랩 없이 유의성을 주장하지 않았는가, 그리고 **"유의한 증거 없음"을 "효과 없음"으로 승격시키지 않았는가.**

### ★ 목차·가설 승인 게이트에서 개입하는 법

파이프라인이 멈추고 목차·RQ·가설·방법을 보여줄 때가 **가장 값싸게 방향을 바꿀 수 있는 지점**이다. 이렇게 말하면 된다.

```
가설을 조절효과 모형으로 재설계해줘
RQ가 셋은 많다 — 하나로 좁히고 나머지는 후속연구로 넘겨줘
이론틀을 바꿔줘. 이 현상엔 다른 틀이 더 맞다
표집을 편의표본 말고 층화로 다시 잡아줘
```

검토관의 게이트가 "실행 가능한가"를 본다면, 이 게이트는 "당신이 하려던 연구가 맞는가"를 본다. 여기서 가설 한 줄을 바꾸는 비용과 분석까지 끝낸 뒤 바꾸는 비용은 자릿수가 다르다.

### 결과가 미덥지 않을 때

```
2장 선행연구가 얇아. 국문 KCI 논문으로 더 찾아줘
이 출처 실재하는지 다시 확인해줘
논의 장만 다시 써줘
데이터 재분석해줘
docx만 다시 생성해줘
```

`_workspace/`가 남아 있으면 **해당 에이전트만 다시 부른다.** 처음부터 다시 돌지 않는다. 조사관은 모든 사실에 출처를 병기하도록 설계돼 있어, 본문의 어떤 문장이 어느 출처에서 왔는지를 근거장부(`03_literature.md`)에서 역추적할 수 있다.

---

## 산출물과 동봉 예제

| 파일 | 내용 |
|---|---|
| `01_research_design.md` | 연구설계 — 의도분석·RQ·가설(변수·조작적 정의)·이론틀·방법·목차·예상 리스크 |
| `02_design_review.md` | 게이트1 판정 — GO/조건부/NO-GO와 무엇을 왜 [필수]로 지적했는지 |
| `03_literature.md` | 근거장부 — 검색 기록(DB·검색어·선정 건수)·분석카드·출처 등급·갭분석 |
| `03b_data_analysis.md` | 데이터 분석 — 무결성 점검·절차·결과·가설 지지여부·한계 (실증연구만) |
| `04_paper_draft.md` | 본문 초안 + 참고문헌 |
| `05_draft_review.md` | 게이트2 5축 검수 — 위치·문제·권고 |
| `06_paper.docx` · `06_paper.md` · `06_proofread_log.md` | 최종 원고와 교정 내역 |

**동봉된 실제 예제.** [examples/socsci-paper-demo/](../examples/socsci-paper-demo/)는 이론·문헌 연구(데이터 없음) 완주본이다. 합성 주제·데모 규모지만 전 과정을 그대로 담았고, 관전 포인트는 완성본이 아니라 **게이트가 무엇을 잡았는지**다.

- **게이트1** — RQ에 쓴 "매개 경로"라는 표현이 무데이터 연구의 주장 범위를 넘는다고 지적했다(매개는 통상 데이터로 검증하는 개념인데, 문헌고찰은 검증이 아니라 종합만 할 수 있다). 그리고 양방향 명제 중 한쪽 근거만 확보되면 경계조건 명제가 공허해지므로, 촉진·억제 근거의 대칭 확보를 조사관에 대한 **차단 조건**으로 승격시켰다. 같은 문서에서 분석가 **SKIP을 확정**한다.
- **게이트2** — 본문 인용과 참고문헌을 전수 대조해 **유령 0건·고아 0건**을 확인했다. 그리고 저자 성명을 끝내 확정하지 못한 2022년 연구를 초안이 어떻게 다뤘는지가 이 예제의 백미다: `(저자, 연도)`를 지어내지 않고 본문에서 **서술적으로만 참조**한 뒤 〔보강 필요〕를 달고 **참고문헌 등재를 보류**했다. 유령 인용은 이렇게 만들지 않는 것이다.

읽는 순서와 관전 포인트는 [examples/README.md](../examples/README.md)에 정리돼 있다.

---

## 팀 구성

| 에이전트 | 역할 | 스킬 |
|---|---|---|
| `paper-designer` | 의도분석·연구유형 판별·RQ·가설(변수·조작적 정의)·이론틀·방법·목차 | `paper-design` |
| `paper-reviewer` | 설계 게이트(모드1) + 5축 초안검수(모드2) · **READ-ONLY** | `paper-review`, `scientometric-paper-review` |
| `paper-investigator` | 선행연구 SLR·이론 원전·통계·사례 조사, 전 사실 출처 병기 | `paper-research` (+geo-search 내장) |
| `paper-analyst` | 양적·질적·혼합 분석 · **조건부 투입** | `paper-analysis` |
| `paper-writer` | APA7 논증형 집필·참고문헌 정합 | `paper-writing` |
| `paper-finalizer` | 한국어 교정교열·`.docx`/`.md` 변환 | 동반 `paper-proofread` + `docx` |

오케스트레이터 `socsci-paper-orchestrator`가 전체를 조율하며 "사회과학 논문"·"학위논문"·"실증연구"·"가설 설계"·"논문 검수" 같은 요청에 자동 반응한다. 각 에이전트에는 오케스트레이터가 투입 여부를 판단할 수 있게 `cost`/`useWhen`/`avoidWhen` 메타데이터가 붙어 있다.

**연구유형 5분류.** 설계자는 착수 전에 실증-양적 / 실증-질적 / 혼합방법 / 이론·문헌 / 사례연구를 먼저 가른다. 이 분류가 가설의 형태(통계 가설이냐 분석명제냐), 분석가 투입 여부, 목차 변형을 전부 결정한다.

**출처 등급 5단계.** 조사관은 동료심사 논문·1차 통계(Tier 1)부터 블로그·생성형 요약(Tier 5)까지 등급을 매기고, 약탈적 저널과 미검증 출처를 플래그한다. 미확보 항목은 `[미확보]`로 남기고 지어내지 않는다.

> **geo-search 내장.** 해외 문헌·사례를 조사할 때 기본 웹검색은 미국 로케일에 고정된다. 내장 래퍼는 대상국 언어·지역으로 검색해(일본 자료는 일본어로) 현지 1차 자료에 닿게 한다. 학술 DB 검색은 그대로 병행한다. 키가 없으면 기본 검색으로 자동 폴백하므로 필수는 아니다.

---

## 요구사항·폴백·한계

- **`.docx` 변환**은 `docx` 스킬을 쓴다. 변환에 실패하면 마크다운 원고를 먼저 내주고 수동 변환 경로를 안내한다.
- **한국어 교정교열**은 동반 스킬 [paper-proofread](https://github.com/parkjui92/paper-proofread)가 있으면 온전해진다. 없으면 검수관 5축의 교열 축으로 대체된다.
- **팀 API가 없는 환경**에서는 순차 `Agent` 호출로 동일 파이프라인이 실행된다. Phase 순서와 산출물 파일 계약은 같다.
- **geo-search 키**(`SERPER_API_KEY` 또는 `SERPAPI_KEY`)는 선택이다. 없으면 기본 검색으로 폴백한다. 상세는 [runtime-notes.md](runtime-notes.md).
- **게이트는 오류를 줄이지 없애지 못한다.** 검수자도 집필자와 같은 계열 모델이라 같은 맹점을 공유할 수 있다. 최종 책임은 저자에게 있다.
- **구독·페이월 DB**(DBpia·Scopus·Web of Science 등)는 당신에게 접근권이 있어야 검증된다. 확인하지 못한 인용은 조용히 삭제되지 않고 `[보강 필요]`로 남는다 — 그리고 그것을 완성으로 간주하지 않는 것이 규율이다.
- **연구윤리는 자동화되지 않는다.** IRB 승인·사전동의·저자권·이해충돌은 사람의 몫이다. 설계자는 해당 여부를 짚어줄 뿐이다.
- 이 킷은 **국내 학술 관행**(한국어 교열, KCI·RISS·DBpia 검색원, 국내지 투고 시 국문 선행연구 균형)에 맞춰져 있다. 영문 저널 투고라면 교열 축과 검색원을 손봐야 한다.
- 동봉 예제는 **합성 주제·데모 규모**다(참고문헌 3편). 정식 논문 기준인 15편+에 못 미치며, 그 점이 예제 안에서도 [권고]로 지적돼 있다.
- 게이트 설계 방법론과 실전 적발 기록은 [verification-gates.md](verification-gates.md)에 있다(직접 만들 때 참고).

---
---

<a name="english"></a>

# Why I built this · Detailed usage

[한국어](#왜-만들었나--상세-사용법) · **English**

Background and usage scenarios trimmed out of the README.

---

## Why I built this

Most people who have asked an LLM to draft a paper are satisfied with the prose. Imitating academic register is no longer hard. The problem is elsewhere.

**Citations break.** And they break in ways that are hard to see.

- **Ghost citations** — `(Smith, 2019)` appears in the body, but not in the reference list. Or the work does not exist at all.
- **Orphan references** — an entry sits in the reference list that is cited nowhere in the body. You revised a paragraph away; the list entry stayed.
- **Unsourced empirical claims** — "prior research reports that…" with zero citations attached at that spot. There is no way for a reader to check it.

None of this is catchable by *reading*. It is catchable by **cross-checking**: matching every in-text citation against the list, then walking the list backwards and finding each entry in the body. It is the single most tedious job in manuscript preparation, which is exactly why it doesn't get done at 2 a.m. before a deadline.

In a paper the price is higher than in a report. An empirical claim in your literature review with no citation attached is one of the top desk-reject triggers in peer review. A mismatch between body and reference list reads not as a weak argument but as a lapse in care — and once a reviewer reads you that way, the rest of the manuscript doesn't recover easily.

**Research design breaks too.** That failure surfaces later, which makes it more expensive.

A report survives a wrong outline; you move paragraphs around. A paper does not. One line of research question fixes the theoretical framework, the framework fixes the hypotheses, the hypotheses fix the variables and their operational definitions, and those fix which data you collect and which technique you run on it. **If the front of that chain is misaligned, an analysis performed correctly at the back of it is still meaningless.** The worst case — collect all the data, write the whole paper, and only then discover that this hypothesis cannot be answered by this data — is common.

So what was needed was not a better prompt for better sentences. It was **two gates**:

1. One **before** research, analysis, and writing begin, that rules on whether the RQ, hypotheses, variables, and method actually fit together
2. One **after** the draft exists, that cross-checks every citation against the reference list

This kit is the personal harness I built by bolting those gates on, one at a time, while writing actual papers — cleaned up and published. In practice, gate 2 has caught **2 ghost citations and 1 orphan reference** on a completed paper run (see the log in [verification-gates.md](verification-gates.md)).

One more reason. Quantitative papers have failure modes that a general review will not catch: treating "no significant evidence" as "no effect," running a staggered-adoption DiD without engaging the literature on standard TWFE bias, reporting analytical cluster standard errors with a small number of clusters. The arithmetic can be entirely correct and the paper still collapses at exactly these points. So there is a dedicated review track for bibliometric and quantitative work — `scientometric-paper-review`.

---

## How it differs from vanilla Claude Code — full table

**Stated up front:** this repository contains no measured A/B comparison against vanilla for *this* kit. The table below is a description of structure, not a measurement.

| | Vanilla session | This kit |
|---|---|---|
| Starting out | Begins writing from the request as given | Fixes RQ, hypotheses, variables, operational definitions, and method first, and gets a **GO / conditional / NO-GO ruling** |
| Citation checking | Draft ships with citations attached, and that's it | **Exhaustive 1:1 cross-check** of body ↔ reference list (including citations in appendices), existence and accessibility of each source, cited figures matched against the source |
| Who reviews | The session that wrote it reads its own work | A **different agent**, **read-only**, re-reading the manuscript from disk |
| Research with no data | Can imitate statistical language anyway | Hypotheses are **replaced by analytical propositions** and the analyst is dropped from the team |
| What remains | One manuscript file | Design, gate rulings, evidence ledger, and review findings **persist as files** |

The last two rows are the point. If the reviewer and the writer are the same, someone is signing off on their own work. And if rulings don't persist as files, there is no way to later ask "was this citation actually verified?"

A sister kit built on the same design philosophy does have a **measured vanilla-vs-kit audit** — same request, same underlying model, run through both, with a neutral third audit session opening every cited URL. Those numbers belong to the policy-research domain and should not be transplanted onto this kit, but they do illustrate what the gate structure changes: [policy-research-kit / vanilla-vs-kit.md](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md).

---

## The gates in detail

```
Research design (designer: RQ, hypotheses, variables, operational
                 definitions, theory, method, outline)
  → 🚦 Gate 1: design review (reviewer mode 1 — GO / conditional / NO-GO)
  → ★ You approve the outline and hypotheses  ← your intervention point
  → Literature review (investigator, systematic) ∥ Data analysis
       (analyst — empirical studies only)
  → Drafting (writer, argument-driven, APA 7)
  → 🚦 Gate 2: draft review (reviewer mode 2 — five axes)
  → Finalizing (finalizer: Korean academic copy-editing → .docx + .md)
```

**Why two gates.** The two failures are different in kind. Gate 1 protects *direction* — it clears out untestable hypotheses, unanswerable RQs, and data you will never actually obtain, before anyone spends effort. Gate 2 protects against *overconfidence* — a finished draft reads convincingly, and it is hard to suspect your own citations.

The reviewer is **a different agent from the writer** and is read-only. It does not edit the manuscript and does not delegate writing to another agent. That structurally prevents anyone from passing their own work. Both gates cap revision at **two rounds**; anything still unresolved is logged as "residual risk" and the pipeline proceeds — perfectionism is not allowed to stall it.

**The five review axes** — ① RQ and hypothesis fulfillment ② evidence and source integrity ③ logical coherence ④ methodological validity ⑤ Korean-language copy-editing.

Axis 2 is the center of gravity: body ↔ reference list at 1:1 (hunting ghosts and orphans), existence and accessibility of each source (URL, DOI, KCI identifier), agreement between cited figures and the actual source, and flagging of hallucinated references.

**Quantitative papers get different axes.** Bibliometric, panel, DiD, event-study, quantitative policy-evaluation, and null-result papers drop into the five axes of `scientometric-paper-review` — measurement integrity (database coverage, counting method, instability in normalization denominators), identification strategy (parallel trends, staggered-DiD bias, small-cluster inference), inferential language (absence of evidence ≠ evidence of absence), literature foundation and citation fidelity, and domain construct validity.

> **A note for readers outside Korea.** The drafting and review skills are written for Korean-language output, and axis 5 is Korean academic copy-editing — Korean academic prose has its own conventions (spacing rules, translationese imported from English sources, hedging particles) that Korean journals enforce. Likewise, `KCI` (Korea Citation Index), `RISS`, and `DBpia` are Korean academic databases that CrossRef and Semantic Scholar do not index, so sources living there come back "unverifiable" through international tools alone — the investigator searches them directly. If you are writing for an English-language journal, the parts to adapt are axis 5 and the search-source list. **Everything else — the design gate, the citation-integrity protocol, the scientometric axes — is language-independent**, and citation integrity is where this kit earns its keep in any language.

---

## Detailed usage

You start by talking to it. Below is what you'd plausibly type, and what happens when you do.

### Scenario 1 — Empirical study (you have data)

```
Start a paper on social insurance blind spots among platform workers,
beginning with the research design. Survey data attached.
For a domestic journal, APA 7.
```

Attachments are saved to `_workspace/00_input/` and indexed — "this file is data, route it to the analyst; this one is prior literature, route it to the investigator." The designer then classifies the study as **empirical-quantitative** and builds 1–3 RQs, hypotheses (independent, dependent, mediating, moderating variables + an operational definition for each + "what result would count as support"), a theoretical framework, sampling/measurement/analysis technique, and an outline.

This is where the pipeline **stops for the first time.** The reviewer rules GO / conditional / NO-GO on one question — "will following this design produce a paper that survives peer review?" — and then shows you the outline and hypotheses.

Once you approve, the investigator (systematic literature review) and the analyst (data integrity check → hypothesis testing) run **in parallel**, then drafting → five-axis review → copy-editing → `.docx`.

### Scenario 2 — Theoretical / literature study (no data)

```
I don't have data. This will be a theoretical paper based on a
literature review.
```

At the design stage, statistical hypotheses are replaced by **analytical propositions**, and the method and results chapters of the outline are restructured as issue-by-issue argumentation. And **the analyst is dropped from the team** — leaving an analyst attached to a study with no data creates a place for numbers to be invented.

The bundled example follows exactly this path — [examples/socsci-paper-demo/](../examples/socsci-paper-demo/).

### Scenario 3 — Review and strengthen a draft you already wrote

```
Review this draft. Start with the citations.
```

Hand it an existing draft and it switches into **revision mode** rather than writing from scratch. The designer reverse-engineers the RQ and hypotheses out of the draft's structure and fills the gaps, the investigator verifies and shores up the sources behind the draft's claims, and the writer revises that draft rather than replacing it.

The citation check runs like this: every `(Author, Year)` in the body is matched against the reference list to find **ghosts**, then every list entry is searched back in the body to find **orphans** (citations in appendices included). Surviving sources are checked for existence via URL, DOI, or KCI identifier, and cited figures are compared against what the source actually says.

### Scenario 4 — Refereeing a quantitative or bibliometric paper

```
Review this DiD paper the way a referee would. The null result
worries me.
```

Review switches to `scientometric-paper-review`. Among the things it checks: with staggered treatment timing, does the paper cite the standard-TWFE bias literature and situate its own design within that discussion; is there a never-treated control group (and if not, does the paper concede that its coefficient is a *relative deviation* rather than a clean counterfactual); with few clusters, does it claim significance without a wild cluster bootstrap; and above all — **has "no significant evidence" been quietly promoted to "no effect"?**

### ★ How to intervene at the approval gate

When the pipeline stops and shows you the outline, RQs, hypotheses, and method, that is **the cheapest possible point to change direction**. Just say so:

```
Redesign the hypotheses as a moderation model
Three RQs is too many — keep one, push the rest to future work
Change the theoretical framework; another one fits this phenomenon better
Redo the sampling as stratified rather than convenience
```

The reviewer's gate asks "is this executable?" This gate asks "is this the study you meant to do?" The cost of changing one line of hypothesis here, versus changing it after the analysis is done, differs by orders of magnitude.

### When the output doesn't convince you

```
Chapter 2's literature is thin — find more Korean-language KCI articles
Re-verify that this source actually exists
Rewrite just the discussion chapter
Re-run the data analysis
Regenerate only the docx
```

If `_workspace/` is still there, **only the relevant agent is called again** — it does not re-run from the top. The investigator is designed to attach a source to every fact, so any sentence in the body can be traced back through the evidence ledger (`03_literature.md`).

---

## Output files and the bundled example

| File | Contents |
|---|---|
| `01_research_design.md` | Design — intent analysis, RQs, hypotheses (variables, operational definitions), theory, method, outline, anticipated risks |
| `02_design_review.md` | Gate 1 ruling — GO / conditional / NO-GO, and what was flagged [required] and why |
| `03_literature.md` | Evidence ledger — search log (databases, queries, hit counts), analysis cards, source tiers, gap analysis |
| `03b_data_analysis.md` | Analysis — integrity check, procedure, results, hypothesis support, limitations (empirical studies only) |
| `04_paper_draft.md` | Body draft + reference list |
| `05_draft_review.md` | Gate 2 five-axis review — location, problem, recommendation |
| `06_paper.docx` · `06_paper.md` · `06_proofread_log.md` | Final manuscript and the record of what was corrected |

**A real worked example is bundled.** [examples/socsci-paper-demo/](../examples/socsci-paper-demo/) is a complete run of a theoretical/literature study with no data. The topic is synthetic and the scale is demo-sized, but the full process is there, and the thing worth reading is not the finished manuscript — it's **what the gates caught**.

- **Gate 1** flagged that the phrase "mediating pathway" in the RQ overreached the claim scope available to a study with no data (mediation is normally established with data; an integrative review can synthesize proposed mechanisms, not test them). It also escalated a design risk into an instruction: because a boundary-condition proposition is empty unless *both* the enabling and the constraining proposition have support, symmetric evidence for both was made a **blocking condition** on the investigator. The same document is where the analyst **SKIP is confirmed**.
- **Gate 2** cross-checked every in-text citation against the reference list and confirmed **0 ghosts, 0 orphans**. The best part of the example, though, is how the draft handled a 2022 study whose author names could never be confirmed: rather than inventing an `(Author, Year)`, it **referred to the study descriptively only** in the body, tagged it "needs verification," and **withheld it from the reference list**. That is how a ghost citation doesn't get created.

Reading order and what to look for are laid out in [examples/README.md](../examples/README.md).

---

## The team

| Agent | Role | Skill |
|---|---|---|
| `paper-designer` | Intent analysis, study-type classification, RQs, hypotheses (variables, operational definitions), theory, method, outline | `paper-design` |
| `paper-reviewer` | Design gate (mode 1) + five-axis draft review (mode 2) · **READ-ONLY** | `paper-review`, `scientometric-paper-review` |
| `paper-investigator` | Systematic literature review, primary theory sources, statistics, cases — every fact sourced | `paper-research` (+ built-in geo-search) |
| `paper-analyst` | Quantitative, qualitative, and mixed-methods analysis · **conditional** | `paper-analysis` |
| `paper-writer` | Argument-driven drafting in APA 7, reference-list consistency | `paper-writing` |
| `paper-finalizer` | Korean academic copy-editing, `.docx` / `.md` conversion | companion `paper-proofread` + `docx` |

The orchestrator `socsci-paper-orchestrator` coordinates all of it and responds automatically to requests about papers, theses, empirical studies, hypothesis design, and manuscript review. Each agent carries `cost` / `useWhen` / `avoidWhen` metadata so the orchestrator can decide whether to deploy it.

**Five study types.** Before anything else, the designer classifies the work as empirical-quantitative, empirical-qualitative, mixed-methods, theoretical/literature, or case study. That classification determines the form the hypotheses take (statistical hypotheses vs. analytical propositions), whether the analyst is deployed at all, and how the outline is restructured.

**Five source tiers.** The investigator grades sources from peer-reviewed articles and primary statistics (Tier 1) down to blogs and AI-generated summaries (Tier 5), and flags predatory journals and unverified sources. Anything it could not obtain is marked "not obtained" rather than invented.

> **Built-in geo-search.** Default web search is pinned to a US locale. The bundled wrapper searches in the target country's language and region (Japanese material in Japanese), which is what it takes to reach local primary sources; academic database searches run alongside it as usual. Without an API key it falls back to standard search, so it's optional.

---

## Requirements, fallbacks, limitations

- **`.docx` conversion** uses the `docx` skill. If conversion fails, you get the Markdown manuscript first plus instructions for converting manually.
- **Korean copy-editing** is complete when the companion skill [paper-proofread](https://github.com/parkjui92/paper-proofread) is installed; without it, the reviewer's copy-editing axis covers it.
- **Without team-API support**, the same pipeline runs via sequential `Agent` calls. Phase order and the output-file contract are identical.
- **geo-search keys** (`SERPER_API_KEY` or `SERPAPI_KEY`) are optional; without them it falls back to standard search. Details: [runtime-notes.md](runtime-notes.md).
- **Gates reduce errors; they don't eliminate them.** The reviewer runs on a model from the same family as the writer and can share its blind spots. Final responsibility stays with the author.
- **Subscription and paywalled databases** (DBpia, Scopus, Web of Science) can only be verified if *you* have access. A citation that couldn't be checked is not quietly deleted — it stays marked "needs verification," and the discipline is to not treat that as finished.
- **Research ethics is not automated.** IRB approval, informed consent, authorship, and conflicts of interest are yours. The designer only flags when they apply.
- This kit is tuned to **Korean academic conventions** (Korean copy-editing, KCI/RISS/DBpia as search sources, a balance of Korean-language prior work for domestic journals). For an English-language journal, adapt axis 5 and the search-source list.
- The bundled example is **a synthetic topic at demo scale** (3 references) — short of the 15+ that a real paper needs, a point the example itself raises as a [recommended] finding.
- The two-stage gate design methodology and the log of what it has caught are in [verification-gates.md](verification-gates.md), if you want to build your own.
