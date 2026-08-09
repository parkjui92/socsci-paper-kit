# Changelog

## v0.10.0 (2026-08-10) — 성능 폴백 장치

무거운 세션 모델(opus/sonnet)로 전 단계가 돌아 논문 한 편에 오래 걸리는 문제 대응. 4겹 구조:

- ① 단계별 모델 티어 기본값: 문헌·근거조사 `sonnet`, 설계·분석·집필·검수·마무리는 세션 상속 유지
- ② 쾌속 프로파일("빨리"·투고 마감 임박 시): 문헌조사 분할 병렬, 집필 장 배치 분할(체크포인트), 수정 루프 2→1회, 출처 검증은 핵심 이론출처·직접인용·주요 수치 전수 + 주변 표본(미개봉 출처 명시)
- ③ 지연 폴백 래더: `_workspace/_run_log.md`에 단계별 시각 기록, 안내 예산 초과 시 분할·병렬화 → 다운시프트 → 루프 축소 → 사용자 범위 협상 순 적용
- ④ 실패 시 업시프트: 하위 모델 단계가 자체 검증에 실패하면 한 단계 위 모델로 1회 재스폰. 재실패 시 없는 문헌을 지어내지 않고 [미확보]로 남긴다
- 검증 게이트(paper-reviewer)와 **데이터분석(paper-analyst)은 어떤 프로파일·래더 단계에서도 경량화하지 않는다** — 유령 인용과 수치 오류는 논문에서 치명적이다.
- `paper-finalizer`는 자매 킷의 변환 단계와 달리 `haiku`로 내리지 않는다 — 한국어 학술 교정교열을 겸하기 때문. 교정 없는 docx 재변환 단독 호출에만 하향을 허용한다.

자매 킷 [policy-research-kit](https://github.com/parkjui92/policy-research-kit) v1.1.0 · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) v0.10.0과 동일 설계다.

## v0.9.0 (2026-07-20) — 공개 후보(Release Candidate)

- 통합 저장소(policy-research-kits)에서 **단독 저장소로 분리** — 이 저장소 하나로 마켓플레이스 등록·설치 가능.
- 전 과정 예제(examples/)·검증 게이트 방법론(docs/) 동봉.
- 공개판 조정: `model: inherit` 기본, 팀 API 부재 시 순차 Agent 폴백, BYO-template, geo-search 내장.

다른 킷: https://github.com/parkjui92/policy-research-kit · https://github.com/parkjui92/rnd-proposal-kit
