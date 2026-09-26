#!/usr/bin/env python3
"""revision_diff.py — 심사 전 원고와 수정본을 단락 단위로 대조한다.

재심사·답변서 점검에서 "원고가 실제로 바뀌었는가"를 모델의 기억이 아니라
파일 대조로 확인하기 위한 도구다. 표준 라이브러리만 쓴다.

    python3 revision_diff.py 원본.md 수정본.md            # 사람이 읽는 보고
    python3 revision_diff.py 원본.md 수정본.md --json     # 기계용
    python3 revision_diff.py --selftest

- 단락 = 빈 줄로 나뉜 블록. 각 블록에 소속 장·절(마크다운 제목 경로)을 붙인다.
- `<!-- ... -->` 숨김 주석(인용 위치 표기 등)은 비교에서 뺀다.
- 제목이 바뀌었거나 바뀐 단락 비율이 0.6을 넘으면 '구조 변경'으로 표시한다.

종료 코드: 0 = 대조 완료, 3 = 대조 완료 + 구조 변경 경고, 2 = 오류.
"""
import argparse
import difflib
import json
import re
import sys

COMMENT = re.compile(r"<!--.*?-->", re.S)
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
STRUCTURAL_RATIO = 0.6


def split_blocks(text):
    """빈 줄 기준 블록 목록. 각 블록: {text, heading_path, is_heading, line}."""
    text = COMMENT.sub("", text)
    blocks, path, buf, start = [], [], [], None
    lines = text.splitlines()

    def flush():
        nonlocal buf, start
        body = "\n".join(buf).strip()
        if body:
            blocks.append({"text": body, "path": " > ".join(p for _, p in path),
                           "is_heading": False, "line": start})
        buf, start = [], None

    for i, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if m:
            flush()
            level, title = len(m.group(1)), m.group(2)
            path = [(lv, t) for lv, t in path if lv < level] + [(level, title)]
            blocks.append({"text": line.strip(), "path": " > ".join(p for _, p in path),
                           "is_heading": True, "line": i})
        elif line.strip() == "":
            flush()
        else:
            if start is None:
                start = i
            buf.append(line)
    flush()
    return blocks


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def excerpt(s, n=90, start=0):
    s = norm(s)
    head = "…" if start > 0 else ""
    s = s[start:]
    return head + (s if len(s) <= n else s[:n] + "…")


def diverge_at(a, b, lead=20):
    """두 단락이 처음 달라지는 지점에서 lead자 앞 — 발췌를 바뀐 곳부터 보여 주기 위해."""
    a, b = norm(a), norm(b)
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return max(i - lead, 0)


def compare(old_text, new_text):
    old, new = split_blocks(old_text), split_blocks(new_text)
    sm = difflib.SequenceMatcher(None, [norm(b["text"]) for b in old],
                                 [norm(b["text"]) for b in new], autojunk=False)
    changes, heading_changes = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        olds, news = old[i1:i2], new[j1:j2]
        kind = {"replace": "수정", "delete": "삭제", "insert": "추가"}[tag]
        where = (news or olds)[0]["path"] or "(제목 이전)"
        sim = None
        at = diverge_at(olds[0]["text"], news[0]["text"]) if len(olds) == len(news) == 1 else 0
        if olds and news:
            sim = round(difflib.SequenceMatcher(
                None, " ".join(norm(b["text"]) for b in olds),
                " ".join(norm(b["text"]) for b in news), autojunk=False).ratio(), 2)
        changes.append({
            "kind": kind, "where": where,
            "old_lines": [b["line"] for b in olds], "new_lines": [b["line"] for b in news],
            "old_blocks": len(olds), "new_blocks": len(news), "similarity": sim,
            "before": [excerpt(b["text"], start=at) for b in olds],
            "after": [excerpt(b["text"], start=at) for b in news],
        })
        for b in olds:
            if b["is_heading"]:
                heading_changes.append("- " + b["text"])
        for b in news:
            if b["is_heading"]:
                heading_changes.append("+ " + b["text"])
    touched = sum(max(c["old_blocks"], c["new_blocks"]) for c in changes)
    ratio = round(touched / max(len(old), 1), 3)
    return {
        "old_blocks": len(old), "new_blocks": len(new),
        "changed_groups": len(changes), "touched_ratio": ratio,
        "heading_changes": heading_changes,
        "structural": bool(heading_changes) or ratio > STRUCTURAL_RATIO,
        "changes": changes,
    }


def render(r):
    out = ["# 원고 변경 대조", "",
           f"- 단락 수: 원본 {r['old_blocks']} → 수정본 {r['new_blocks']}",
           f"- 변경 묶음: {r['changed_groups']}건 · 바뀐 단락 비율 {r['touched_ratio']}"]
    if r["structural"]:
        out.append("- **구조 변경 경고**: 제목이 바뀌었거나 바뀐 단락 비율이 "
                   f"{STRUCTURAL_RATIO}를 넘는다. 사용자 확인 없이 진행하지 않는다.")
    if r["heading_changes"]:
        out += ["", "## 제목 변경", *r["heading_changes"]]
    out += ["", "## 변경 목록", ""]
    if not r["changes"]:
        out.append("(변경 없음 — 원고가 바이트 수준에서 같거나 주석만 바뀌었다)")
    for n, c in enumerate(r["changes"], 1):
        sim = f" · 유사도 {c['similarity']}" if c["similarity"] is not None else ""
        out.append(f"### D{n}. {c['kind']} — {c['where']}{sim}")
        out.append(f"- 원본 줄 {c['old_lines'] or '-'} → 수정본 줄 {c['new_lines'] or '-'}")
        for b in c["before"]:
            out.append(f"  - 전: {b}")
        for a in c["after"]:
            out.append(f"  - 후: {a}")
        out.append("")
    return "\n".join(out)


def selftest():
    old = ("# 1. 서론\n\n문단 가.\n\n문단 나. <!--loc:p.3-->\n\n"
           "# 2. 이론\n\n문단 다.\n\n문단 라.\n")
    same_but_comment = old.replace("<!--loc:p.3-->", "<!--loc:p.4-->")
    edited = old.replace("문단 다.", "문단 다를 고쳤다.")
    added = old + "\n문단 마.\n"
    retitled = old.replace("# 2. 이론", "# 2. 이론적 배경")
    checks = [
        ("주석만 변경은 무변경", compare(old, same_but_comment)["changed_groups"] == 0),
        ("단락 수정 1건 감지", compare(old, edited)["changed_groups"] == 1),
        ("수정 위치가 2장", compare(old, edited)["changes"][0]["where"].startswith("2. 이론")),
        ("추가 감지", compare(old, added)["changes"][0]["kind"] == "추가"),
        ("제목 변경은 구조 변경", compare(old, retitled)["structural"]),
        ("국소 수정은 구조 변경 아님", not compare(old, edited)["structural"]),
        ("동일 원고 무변경", compare(old, old)["changed_groups"] == 0),
    ]
    ok = True
    for name, passed in checks:
        print(("PASS " if passed else "FAIL ") + name)
        ok &= passed
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("original", nargs="?")
    ap.add_argument("revised", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.original and a.revised):
        ap.print_usage(sys.stderr)
        return 2
    try:
        with open(a.original, encoding="utf-8") as f:
            old = f.read()
        with open(a.revised, encoding="utf-8") as f:
            new = f.read()
    except OSError as e:
        print(f"오류: {e}", file=sys.stderr)
        return 2
    r = compare(old, new)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
    return 3 if r["structural"] else 0


if __name__ == "__main__":
    sys.exit(main())
