# socsci-paper-kit

[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)

**한국어** · [English](README.en.md)

사회과학 학술논문을 연구설계(RQ·가설·변수·조작적 정의·이론틀)부터 투고 가능한 `.docx`까지 쓰는 **6인 에이전트 팀** [Claude Code](https://claude.com/claude-code) 플러그인.
지키는 것은 문장이 아니라 **인용과 설계**다 — 본문에 달린 인용이 실제로 참고문헌에 있는지, 그 가설로 그 데이터를 분석하는 것이 애초에 말이 되는지를 저자 대신 두 번 검문한다.

<!-- 데모 GIF 자리 -->

## 왜 게이트인가

인용 결함은 문장을 읽어서는 안 잡힌다. **대조해야 잡힌다** — 본문의 인용을 하나씩 목록과 맞춰 보고, 목록의 항목을 하나씩 본문에서 되찾아봐야 나온다. 마감 직전에 사람이 가장 하기 싫은 일이고, 그래서 실제로 안 하게 되는 일이다.

| | 순정 세션 | 이 킷 |
|---|---|---|
| 인용 점검 | 초안에 인용이 달린 채로 끝 | 본문↔참고문헌 **1:1 전수 대조**(부록 포함) · 출처 실재·수치 확인 |
| 검수자 | 쓴 세션이 자기 글을 본다 | **다른 에이전트**가 READ-ONLY로 디스크에서 다시 읽는다 |
| 남는 것 | 원고 파일 하나 | 설계·게이트 판정·근거장부·검수 기록이 **파일로 잔존** |

판정이 파일로 남지 않으면 "이 인용은 확인된 것인가"를 나중에 되물을 방법이 없다. 다만 이 표는 측정치가 아니라 구조 서술이다 — 이 킷에 대한 순정 대비 A/B 실측은 없다.

→ [왜 만들었나·상세 사용법](docs/why.md) · [자매 킷의 순정 대비 실측 A/B](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md)

## 파이프라인

```
설계 → 🚦게이트1(설계검토) → ★목차·가설 승인 → 조사 ∥ 분석 → 집필 → 🚦게이트2(5축 검수) → 교정 → docx
```

게이트1은 *방향*을 막고(검증 못 할 가설·답 못 할 RQ를 착수 전에 걷어낸다), 게이트2는 *과신*을 막는다. 검수자는 집필자와 **다른 에이전트**이고 READ-ONLY라, 자기 글을 자기가 통과시킬 수 없다.

**5축 검수** — ①RQ·가설 충족 ②근거·출처 무결성 ③논리 정합성 ④방법론 타당성 ⑤한국어 교열. 축2가 중심이다. 정량 논문(서지계량·패널·DiD·귀무결과)은 `scientometric-paper-review`의 5축(측정 무결성·식별전략·추론 언어·인용 충실성·구성타당도)으로 내려간다.

실제 적발: 유령 인용 2건 · 본문에 없는 고아 출처 1건.

## 설치

```
/plugin marketplace add parkjui92/socsci-paper-kit
/plugin install socsci-paper-kit@socsci-paper-kit
```

한국어 교정교열을 온전히 쓰려면 동반 스킬 [paper-proofread](https://github.com/parkjui92/paper-proofread) 설치를 권장한다(미설치 시 검수관 5축의 교열 축으로 대체된다).

## 쓰는 법

```
플랫폼 노동자 사회보험 논문, 설계부터. 설문 데이터 첨부했어    ← 데이터 있음
데이터는 없어. 문헌고찰로 이론 논문을 쓸 거야                  ← 분석가 자동 제외
이 논문 초안 검수해줘. 인용부터 봐줘                           ← 개정 모드
가설을 조절효과 모형으로 재설계해줘                            ← 승인 게이트에서
```

두 번 멈춰 선다(게이트1 후 목차·가설 승인, 게이트2 후 수정 확인). 그사이 자리를 비워도 된다.

## 무엇이 남는가

원고 하나가 아니라 **감사 가능한 기록 한 벌** — 설계·게이트1 판정·근거장부·데이터분석·초안·게이트2 검수·최종 `.docx`.
6개월 뒤 심사자가 "이 인용 어디서 나왔냐"고 물었을 때 답할 수 있다는 뜻이다. `_workspace/`는 지우지 않는다 — 부분 재실행이 이 파일들을 기준으로 돈다.

동봉 예제: [이론·문헌 연구 완주본](examples/socsci-paper-demo/) · [읽는 순서와 관전 포인트](examples/README.md)

## 요구사항·한계

- `.docx` 변환은 `docx` 스킬을 쓴다. 실패하면 마크다운 원고를 먼저 내주고 수동 변환 경로를 안내한다
- **게이트는 오류를 줄이지 없애지 못한다.** 검수자도 집필자와 같은 계열 모델이라 같은 맹점을 공유할 수 있다
- **구독·페이월 DB**(DBpia·Scopus·Web of Science)는 당신에게 접근권이 있어야 검증된다. 확인하지 못한 인용은 조용히 삭제되지 않고 `[보강 필요]`로 남는다
- 국내 학술 관행(한국어 교열, KCI·RISS·DBpia 검색원)에 맞춰져 있다. 영문 저널 투고라면 교열 축과 검색원을 손봐야 한다
- [폴백·의존성·키 설정](docs/runtime-notes.md) · [게이트 설계 방법론과 적발 기록](docs/verification-gates.md)

## 시리즈

**에이전트 팀 킷** — [policy-research-kit](https://github.com/parkjui92/policy-research-kit) (정책연구보고서) · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) (정부 R&D 제안서)

**제작·편집 킷** — [lecture-deck-kit](https://github.com/parkjui92/lecture-deck-kit) (강의자료 HTML 덱 · 브라우저 라이브 편집)

**단독 스킬** — [fact-verify](https://github.com/parkjui92/fact-verify) (출처 검증) · [paper-proofread](https://github.com/parkjui92/paper-proofread) (한국어 학술 교정교열) · [form-tailor](https://github.com/parkjui92/form-tailor) (기관 양식 맞춤) · [report-to-brief](https://github.com/parkjui92/report-to-brief) (보고서 압축)

## 라이선스

[MIT](LICENSE). 독점 기관 양식과 실제 수탁 과제 산출물은 포함하지 않는다(BYO-template 원칙).
