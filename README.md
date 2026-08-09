# socsci-paper-kit

사회과학 학술논문을 쓰는 **6인 에이전트 팀** 플러그인. 연구설계(RQ·가설·변수·조작적 정의·이론틀)부터 5축 검수, Word(`.docx`)+Markdown 산출까지. 방법론 4종(양적·질적·혼합·이론) 지원.

## 파이프라인

```
연구설계(designer: RQ·가설·이론틀·방법·목차) → 설계검토 게이트(reviewer 모드1)
  → 근거조사(investigator: SLR식) ∥ 데이터분석(analyst — 실증연구일 때만)
  → 집필(writer: APA7 논증형) → 5축 검수(reviewer 모드2)
  → 교정·변환(finalizer: docx+md)
```

- **5축 검수**: RQ·가설 충족 / 근거·출처 무결성 / 논리 정합성 / 방법론 타당성 / 한국어 교열. 실전에서 **유령인용 2건·고아출처 1건**을 적발했다.
- **심화 검수 포함**: 계량서지·정량 논문용 `scientometric-paper-review` — 측정 무결성·식별전략(staggered DiD·소표본)·귀무결과 해석·구성타당도까지 내려가는 전용 축.
- **조건부 분석가**: 데이터 없는 이론·문헌 연구면 analyst를 자동 스킵한다.

## 구성

| 에이전트 | 역할 | 스킬 |
|---|---|---|
| paper-designer | RQ·가설·이론틀·방법·목차 설계 | paper-design |
| paper-reviewer | 설계 게이트 + 5축 검수 (READ-ONLY) | paper-review, scientometric-paper-review |
| paper-investigator | 선행연구·이론출처·통계 조사 | paper-research (+geo-search 내장) |
| paper-analyst | 양적·질적·혼합 분석 (조건부) | paper-analysis |
| paper-writer | 학술 문체·APA7 집필 | paper-writing |
| paper-finalizer | 교정교열·docx 변환 | (companion: paper-proofread) |

오케스트레이터 스킬 `socsci-paper-orchestrator`가 조율한다.

## 설치·사용

```
/plugin marketplace add parkjui92/socsci-paper-kit
/plugin install socsci-paper-kit@socsci-paper-kit
```

한국어 학술 교정교열을 온전히 쓰려면 동반 스킬 설치를 권장:
[parkjui92/paper-proofread](https://github.com/parkjui92/paper-proofread) (미설치 시 검수관의 교열 축으로 대체).

```
"플랫폼 노동자의 사회보험 사각지대에 대한 실증연구 논문을 설계부터 시작해줘. 설문 데이터 첨부."
"가설을 조절효과 모형으로 재설계해줘"
```

## 알아두실 점

- 논문 한 편은 문헌조사와 검증 때문에 **시간이 꽤 걸립니다.** 급하실 때는 "빨리 해줘"라고 말씀하세요 — 문헌조사를 나눠 동시에 돌리고 집필을 장 단위 배치로 끊는 쾌속 방식으로 바꿉니다. 어느 단계가 예상보다 크게 늦어지면 완료된 중간 결과를 보여드리고 계속 갈지 여쭙니다. 다만 **검수하는 AI와 데이터 분석은 어떤 경우에도 가볍게 바꾸지 않습니다** — 유령 인용과 수치 오류는 논문에서 치명적이기 때문입니다.
- **점검이 오류를 줄여주긴 하지만 없애주지는 못합니다.** 검수하는 AI도 같은 계열이라 비슷한 착각을 할 수 있습니다. 인용·수치의 최종 확인은 사람이 해야 합니다.

## 문서·예제 (이 저장소 동봉)

- [examples/](examples/) — 전 과정 산출물: 설계 → 게이트 판정 → 근거 → 초안 → 검수 → 최종 파일
- [docs/verification-gates.md](docs/verification-gates.md) — 2단계 검증 게이트 설계 방법론
- [docs/runtime-notes.md](docs/runtime-notes.md) — 팀 API 폴백·kordoc 설치·geo-search 키·모델 선택

## 시리즈

다른 킷: [policy-research-kit](https://github.com/parkjui92/policy-research-kit) · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) · 단독 검증 스킬: [fact-verify](https://github.com/parkjui92/fact-verify) · [paper-proofread](https://github.com/parkjui92/paper-proofread) · [form-tailor](https://github.com/parkjui92/form-tailor) · [report-to-brief](https://github.com/parkjui92/report-to-brief)

## 라이선스

Apache-2.0. 독점 기관 양식·실제 과제 산출물은 포함하지 않는다(BYO-template 원칙).
