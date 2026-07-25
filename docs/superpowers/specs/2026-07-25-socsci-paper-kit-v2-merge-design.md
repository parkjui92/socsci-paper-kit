# socsci-paper-kit v2.0.0 — 실증분석 근육 이식 설계 (Design Spec)

- **작성일:** 2026-07-25
- **대상:** `socsci-paper-kit`(GitHub 공개 플러그인) + `~/.claude` 운영 하네스
- **상태:** 승인됨 (구조 확정, 구현 계획 대기)

## 1. 배경과 목표

사회과학 논문 도메인에 세 자산이 존재한다.

| 자산 | 형태 | 강점 |
|------|------|------|
| ① `~/social-science-research-agent` | 로컬 실작업 폴더(비 git) | 실증분석 근육 — `data-engineer`(수집·전처리·코드북), `statistician`(OLS/DID/RDD/IV/PSM, Python 실행) |
| ② `~/.claude` 하네스 `socsci-paper-orchestrator` | 운영본 | 2단계 게이트 6인 팀 |
| ③ `socsci-paper-kit` | 공개 플러그인(②를 패키징) | 설계·검수 거버넌스, 인용 무결성, docx 산출 |

①과 ②/③은 상보적이다. ③의 `paper-analyst`는 READ-ONLY라 실제 코드를 돌리지 못한다. **목표: ①의 실증분석 근육을 ③의 게이트 구조에 이식**해, 데이터 수집→전처리→계량분석까지 실제 코드로 수행하는 6인 킷 v2를 만든다.

편집 대상은 **두 표면을 동시 동기화**한다.
- **배포 리포:** `~/Desktop/아이디어 점검/_staging/socsci-paper-kit`(git, → GitHub push)
- **운영 하네스:** `~/.claude/agents/paper-*.md`, `~/.claude/skills/paper-*`

로컬 사용은 **하네스 동기화가 곧 설치**다(플러그인 별도 설치 안 함 — 중복 등록 방지, 기존 킷 운영 패턴 유지). 동기화 후 다음 세션부터 승격된 analyst가 모든 세션에서 작동한다.

## 2. 설계 결정 (승인됨)

1. **통합 방식:** `paper-analyst`를 READ-ONLY → 실무형으로 승격. `data-engineer`+`statistician` 역량을 흡수. **6인 유지**(새 에이전트 추가 없음).
2. **흡수 자산:** 계량분석 스킬 내용 + `research-standards` 규칙 + Python 환경 명세 + 슬래시 명령어 — 전부.
3. **로컬 폴더 ①:** 자산 흡수 후 은퇴(archive).

## 3. 변경 명세

### 3.1 `paper-analyst.md` 승격 (핵심 변경 1) — 🟡★

두 편집 표면 모두에 반영.

- **description·본문:** "READ-ONLY 분석관" → "실무형 분석관". 실제 Write/Edit/Bash로 데이터·코드·결과표를 산출한다는 점 명시. `tools: All tools` 유지(권한 변경 불필요, 프롬프트가 실행을 지시).
- **역할 확장** — 기존 5역할(무결성 점검/양적/질적/혼합/결과정리)에 다음을 통합:
  - **데이터 엔지니어링:** 공공데이터 API 수집(KOSIS·data.go.kr·NTIS·KLIPS·KOWEPS / OECD.Stat·World Bank·V-Dem·QoG), 클리닝(타입변환·결측 MCAR/MAR/MNAR·이상치 IQR/Z·재코딩·파생·패널 구성), **코드북**, 품질진단.
  - **계량분석:** 기술통계→시각화→모형추정→진단→강건성 순서 엄수. 모형(OLS/로짓·프로빗/패널 FE·RE/DID·사건연구/RDD/IV·2SLS/PSM), 진단(VIF·BP·DW·Hausman·평행추세·1단계 F·McCrary), 강건성 최소 3종, random seed 고정(기본 42).
- **산출물 계약(폴더 관례 재조정):** 플러그인의 `_workspace/` 관례와 ①의 `data/`·`analysis/`·`paper/` 관례를 통합한다.
  - 실제 산출물: `_workspace/data/raw|cleaned/`, `_workspace/analysis/scripts|results/`, `_workspace/paper/tables|figures/` (재현 가능한 스크립트 + 결과표/그림).
  - 요약 보고: 기존 `_workspace/03b_data_analysis.md` 유지(①무결성 ②절차 ③결과표·그림 ④가설 지지 ⑤해석 ⑥한계).
  - `data/raw/` 원본 불변 원칙 유지.
- **불변 유지:** 조건부 스킵(데이터 없는 이론·문헌 연구), `[데이터 필요]` 마커, p-hacking·과대해석 금지, cost=EXPENSIVE, 팀 통신 프로토콜.

### 3.2 `paper-analysis/SKILL.md` 강화 (핵심 변경 2) — 🟡★

두 편집 표면 모두에 반영.

- 현재 64줄(양적/질적/혼합 개념 가이드)에 ①의 `data-collection`(수집·코드북·품질진단, 32줄) + `statistical-analysis`(계량모형·인과추론·진단·강건성·시각화, 71줄)의 **실행 워크플로우**를 병합.
- 추가: 실제 Python 실행 절차(수집→클리닝→기술통계→모형→진단→강건성→표/그림), 데이터소스 카탈로그, 인과추론 식별전략별 기법·패키지 표.
- `references/` 신설 — 계량 레시피(인과추론 식별전략, 진단검정 임계값, 강건성 6종, 코드북 템플릿, 결과표 형식). SKILL.md 본문은 요약·라우팅, 상세는 references로.

### 3.3 흡수 자산 편입 — 🟢 (배포 리포 전용)

- `requirements.txt` — ①에서 이식(pandas·numpy·scipy·statsmodels·linearmodels·scikit-learn·matplotlib·seaborn·stargazer·openpyxl·requests, 선택 rdrobust·konlpy). 배포판 루트에 동봉.
- `rules/research-standards.md` — ①에서 이식. 연구윤리·재현성·데이터윤리·품질 공용 규칙. analyst·writer·reviewer가 참조.
- `commands/` 신설 — ①의 5개 명령어를 **6인 게이트 파이프라인으로 재배선**:
  - `research.md` = 전체: 설계→설계게이트→(조사 ∥ 분석)→집필→5축 검수→마무리(docx)
  - `lit-review.md` → paper-investigator | `data-prep.md` → paper-analyst(데이터 단계) | `analyze.md` → paper-analyst(분석 단계) | `draft-paper.md` → paper-writer
  - ※ 구 4인(문헌리뷰어·데이터엔지니어·통계분석가·논문작성자) 매핑은 폐기하고 신 6인 에이전트로 지시.
- `docs/runtime-notes.md` — 🟡 Python 환경 의존성·재현성 규약(seed·패키지 버전 기록·원본 불변) 추가.
- `docs/analysis-environment.md` — 🟢(선택) 데이터/분석 폴더 관례와 실행 가이드.

### 3.4 버전·문서 — 🟡

- `.claude-plugin/plugin.json` version `0.9.0` → `2.0.0`, description에 "실증분석(데이터 수집→코드 실행→결과표)" 반영.
- `README.md` — 실증분석 지원 섹션 + Python 요구사항 안내.
- `CHANGELOG.md` — v2.0.0 항목(실증분석 근육 이식, commands·rules·requirements 추가).
- `~/.claude/CLAUDE.md` — 사회과학 논문 하네스 변경 이력 +1행(2026-07-25 병합).
- `socsci-paper-orchestrator/SKILL.md` — 🟡 분석 단계의 실코드 산출 계약을 오케스트레이션에 반영(두 표면).

### 3.5 로컬 폴더 ① 은퇴 — 🔴

`~/social-science-research-agent`는 자산 흡수 완료 후 아카이브(예: `~/Desktop/아이디어 점검/_archive/`로 이동 또는 폴더 내 `ARCHIVED.md` 표식). 이중관리 금지.

## 4. 명시적 비목표 (YAGNI)

- designer·investigator·writer·reviewer·finalizer 로직 변경 ❌
- 새 에이전트 추가 ❌ (6인 유지)
- 플러그인 marketplace 설치 ❌ (하네스 동기화로 대체)
- 로컬 폴더 ① 유지·이중관리 ❌

## 5. 산출물 요약

| 구분 | 개수 | 내역 |
|------|------|------|
| 🟢 신규 | 8~9 | commands 5 + requirements.txt + rules/research-standards.md + paper-analysis/references (+선택 docs/analysis-environment.md) |
| 🟡 변경 | 7~8 | paper-analyst · paper-analysis · orchestrator · plugin.json · README · CHANGELOG · runtime-notes (+CLAUDE.md) |
| ⚪ 불변 | 나머지 | 5인 에이전트 · 5개 스킬 · 게이트 · 예제 |
| 🔴 은퇴 | 1 | 로컬 폴더 ① |

핵심은 **2개 파일(`paper-analyst.md`, `paper-analysis/SKILL.md`)의 실질 개조**로 실증분석 근육이 들어가고, 나머지는 자산 이관·재배선·버전 문서라는 점이다.

## 6. 검증 (완료 정의)

1. 두 편집 표면(배포 리포 + 하네스)에서 `paper-analyst`·`paper-analysis`가 동일하게 승격됨.
2. 배포 리포에 commands 5·rules·requirements·references 존재, plugin.json v2.0.0.
3. 배포 리포 git commit + GitHub push 완료.
4. 하네스 동기화 완료 — 새 세션에서 논문 요청 시 승격된 analyst가 실코드 경로로 작동(개념 확인).
5. 로컬 폴더 ① 아카이브 표식.
6. `~/.claude/CLAUDE.md` 변경 이력 갱신.
