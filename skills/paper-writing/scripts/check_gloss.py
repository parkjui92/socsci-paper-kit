#!/usr/bin/env python3
"""check_gloss.py — 국문 원고의 영문 병기·약어 규칙을 결정론적으로 점검한다.

국내 학술지 관례 "한국어 우선, 최초 1회 영문 병기, 약어는 정의 후 사용"을
모델 판단 없이 검사한다. 원고를 고치지 않고 보고만 한다. 표준 라이브러리만 쓴다.

    python3 check_gloss.py 원고.md
    python3 check_gloss.py 원고.md --allow OECD,GDP --json
    python3 check_gloss.py --selftest

보고 유형
- 중복 병기: 같은 영문 병기가 두 번 이상 나온다(두 번째부터 보고).
- 정의 전 사용: 약어가 병기로 정의되기 전에 본문에 단독으로 나온다.
- 미정의 약어: 약어가 본문에 나오지만 병기로 정의된 적이 없다.

읽지 않는 곳: 코드 블록, `<!-- -->` 주석, 표 줄(`|`로 시작), 참고문헌 절 이후,
인용 괄호(연도·et al.·p.가 든 괄호). 표 안의 약어 단독 사용은 관례상 허용한다.

종료 코드: 0 = 지적 없음, 1 = 지적 있음, 2 = 오류.
"""
import argparse
import json
import re
import sys

DEFAULT_ALLOW = {"AI", "R&D", "OECD", "GDP", "EU", "UN", "ICT", "IT", "SNS", "COVID"}
REF_HEADING = re.compile(r"^#{1,6}\s*.*(참고문헌|References|Bibliography)", re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
PAREN = re.compile(r"\(([^()]*)\)")
ACRONYM = re.compile(r"(?<![A-Za-z0-9&])([A-Z][A-Z0-9&]*[A-Z0-9](?:s)?)(?![A-Za-z0-9&])")
CITATION_HINT = re.compile(r"(\b(1[89]|20)\d{2}[a-z]?\b|et al\.|\bp{1,2}\.\s*\d|n\.d\.)")
HANGUL_BEFORE = re.compile(r"[가-힣][가-힣A-Za-z0-9·･\-\s]{0,2}$")
LABEL = re.compile(r"[A-Z]{1,4}\d+[a-z]?")   # RQ1·H2·P1·APA7 같은 번호 이름표는 약어가 아니다


def body_lines(text):
    """(줄번호, 줄) — 읽을 줄만 돌려준다."""
    text = COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if REF_HEADING.match(line):
            return
        if line.lstrip().startswith("|"):
            continue
        yield i, line


def is_gloss(inner, before):
    """괄호 안이 영문 병기인가: 라틴 문자가 있고, 인용이 아니며, 앞이 한글이다."""
    if not re.search(r"[A-Za-z]", inner) or CITATION_HINT.search(inner):
        return False
    if re.search(r"[가-힣]", inner):
        return False
    words = re.findall(r"[A-Za-z][A-Za-z0-9&]*", inner)
    if words and all(LABEL.fullmatch(w) for w in words):
        return False
    return bool(HANGUL_BEFORE.search(before))


def check(text, allow=frozenset()):
    allow = DEFAULT_ALLOW | set(allow)
    seen_gloss = {}        # 정규화 병기 → 첫 줄
    defined = {}           # 약어 → 정의 줄
    first_bare = {}        # 약어 → 첫 단독 사용 줄
    findings = []
    for ln, line in body_lines(text):
        gloss_spans = []
        for m in PAREN.finditer(line):
            inner = m.group(1).strip()
            if not is_gloss(inner, line[:m.start()]):
                continue
            gloss_spans.append((m.start(), m.end()))
            key = re.sub(r"\s+", " ", inner.lower())
            if key in seen_gloss:
                findings.append({"type": "중복 병기", "line": ln, "term": inner,
                                 "note": f"{seen_gloss[key]}행에서 이미 병기함"})
            else:
                seen_gloss[key] = ln
            for a in ACRONYM.findall(inner):
                defined.setdefault(a, ln)
        for m in ACRONYM.finditer(line):
            if any(s <= m.start() < e for s, e in gloss_spans):
                continue
            if any(s <= m.start() < e for s, e in
                   ((p.start(), p.end()) for p in PAREN.finditer(line)
                    if CITATION_HINT.search(p.group(1)))):
                continue
            if LABEL.fullmatch(m.group(1)):
                continue
            first_bare.setdefault(m.group(1), ln)
    for a, ln in sorted(first_bare.items(), key=lambda x: x[1]):
        if a in allow or a.rstrip("s") in allow:
            continue
        base = a if a in defined else a.rstrip("s")
        if base not in defined:
            findings.append({"type": "미정의 약어", "line": ln, "term": a,
                             "note": "한국어 명칭(영문, 약어) 형태로 먼저 정의"})
        elif ln < defined[base]:
            findings.append({"type": "정의 전 사용", "line": ln, "term": a,
                             "note": f"{defined[base]}행에서야 정의됨"})
    findings.sort(key=lambda f: f["line"])
    return findings


def selftest():
    cases = [
        ("정상 병기", "정책이전(policy transfer)을 본다. 정책이전은 흔하다.\n", 0),
        ("중복 병기", "정책이전(policy transfer)이다.\n\n정책이전(policy transfer)이다.\n", 1),
        ("인용 괄호 무시", "선행연구(Smith, 2020)와 연구(Kim et al., 2019)가 있다.\n", 0),
        ("정의 후 약어", "고위험·고보상(high-risk high-reward, HRHR) 연구다. HRHR은 드물다.\n", 0),
        ("정의 전 약어", "HRHR이 있다.\n\n고위험·고보상(high-risk high-reward, HRHR) 연구다.\n", 1),
        ("미정의 약어", "DARPA가 설립되었다.\n", 1),
        ("허용 약어", "OECD 자료다.\n", 0),
        ("표 줄 허용", "| 기관 | HRHR |\n|---|---|\n", 0),
        ("참고문헌 이후 무시", "본문.\n\n## 참고문헌\n\nDARPA (2020). Report.\n", 0),
        ("주석 무시", "본문 <!--loc:\"DARPA says\"--> 이다.\n", 0),
        ("번호 이름표 무시", "RQ1에 대해 촉진(P1)과 억제(P2)가 있다. 명제 1(P1, 촉진).\n", 0),
    ]
    ok = True
    for name, text, want in cases:
        got = len(check(text))
        passed = got == want
        print(("PASS " if passed else "FAIL ") + f"{name} (지적 {got}건, 기대 {want}건)")
        ok &= passed
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--allow", default="", help="쉼표로 구분한 허용 약어")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.file:
        ap.print_usage(sys.stderr)
        return 2
    try:
        with open(a.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"오류: {e}", file=sys.stderr)
        return 2
    allow = {s.strip() for s in a.allow.split(",") if s.strip()}
    findings = check(text, allow)
    if a.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    elif not findings:
        print("지적 없음 — 영문 병기·약어 규칙 충족")
    else:
        print(f"# 영문 병기·약어 점검 — {len(findings)}건\n")
        for f in findings:
            print(f"- {f['line']}행 [{f['type']}] {f['term']} — {f['note']}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
