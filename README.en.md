# socsci-paper-kit

[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)

[한국어](README.md) · **English**

A [Claude Code](https://claude.com/claude-code) plugin: a **six-agent team** that takes a social science paper from research design — research questions, hypotheses, variables, operational definitions, theoretical framework — to a submission-ready `.docx`.
What it protects is not prose. It's **citations and design** — whether every in-text citation actually exists in the reference list, and whether analyzing that data with that hypothesis makes sense in the first place.

<!-- demo GIF goes here -->

## Why gates

Citation defects are not catchable by *reading*. They are catchable by **cross-checking**: matching every in-text citation against the list, then walking the list backwards and finding each entry in the body. It is the single most tedious job in manuscript preparation, which is exactly why it doesn't get done at 2 a.m. before a deadline.

| | Vanilla session | This kit |
|---|---|---|
| Citation checking | Draft ships with citations attached, and that's it | **Exhaustive 1:1 cross-check** of body ↔ reference list (appendices included) · existence and figures verified |
| Who reviews | The session that wrote it reads its own work | A **different agent**, **read-only**, re-reading the manuscript from disk |
| What remains | One manuscript file | Design, gate rulings, evidence ledger, review findings **persist as files** |

If rulings don't persist as files, there is no way to later ask "was this citation actually verified?" That said, the table describes structure, not measurement — there is no measured A/B against vanilla for this kit.

→ [Why I built this + detailed usage](docs/why.md) · [A sister kit's measured A/B audit](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md)

## Pipeline

```
Design → 🚦Gate 1 (design review) → ★You approve outline + hypotheses
       → Literature ∥ Analysis → Drafting → 🚦Gate 2 (5 axes) → copy-edit → docx
```

Gate 1 protects *direction* (untestable hypotheses and unanswerable RQs are cleared out before anyone spends effort); gate 2 protects against *overconfidence*. The reviewer is **a different agent** from the writer and is read-only, so nobody signs off on their own work.

**The five axes** — ① RQ and hypothesis fulfillment ② evidence and source integrity ③ logical coherence ④ methodological validity ⑤ Korean-language copy-editing. Axis 2 is the center of gravity. Quantitative work (bibliometric, panel, DiD, null results) drops into the five axes of `scientometric-paper-review`: measurement integrity, identification strategy, inferential language, citation fidelity, construct validity.

Caught in practice: 2 ghost citations · 1 orphan reference not present in the body.

## Install

```
/plugin marketplace add parkjui92/socsci-paper-kit
/plugin install socsci-paper-kit@socsci-paper-kit
```

For full Korean academic copy-editing, installing the companion skill [paper-proofread](https://github.com/parkjui92/paper-proofread) is recommended (without it, that work falls back to the reviewer's copy-editing axis).

## Usage

```
Start a paper on platform workers' social insurance. Data attached.   ← you have data
No data. This will be a theoretical paper from a literature review.   ← analyst dropped
Review this draft. Start with the citations.                          ← revision mode
Redesign the hypotheses as a moderation model                         ← at the approval gate
```

It pauses twice (outline and hypothesis approval after gate 1, revision confirmation after gate 2), so you can step away in between.

## What you get

Not one manuscript but **an auditable record set** — design, gate 1 ruling, evidence ledger, data analysis, draft, gate 2 review, final `.docx`. Which means that six months later, when a reviewer asks where a citation came from, you can answer. Don't delete `_workspace/` — partial re-runs work off these files.

Worked example: [a complete theoretical/literature run](examples/socsci-paper-demo/) · [reading order and what to look for](examples/README.md)

## Requirements & limits

- `.docx` conversion uses the `docx` skill; if it fails you get the Markdown manuscript first plus manual conversion instructions
- **Gates reduce errors; they don't eliminate them.** The reviewer runs on a model from the same family as the writer and can share its blind spots
- **Subscription and paywalled databases** (DBpia, Scopus, Web of Science) can only be verified if *you* have access. A citation that couldn't be checked is not quietly deleted — it stays marked "needs verification"
- Tuned to Korean academic conventions (Korean copy-editing; KCI, RISS, DBpia as search sources). For an English-language journal, adapt axis 5 and the search-source list — **everything else, including the design gate and the citation-integrity protocol, is language-independent**
- [Fallbacks, dependencies, keys](docs/runtime-notes.md) · [Gate design methodology and the catch log](docs/verification-gates.md)

## Series

**Agent-team kits** — [policy-research-kit](https://github.com/parkjui92/policy-research-kit) (policy research reports) · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) (Korean government R&D proposals)

**Authoring kit** — [lecture-deck-kit](https://github.com/parkjui92/lecture-deck-kit) (HTML lecture decks with in-browser live editing)

**Standalone skills** — [fact-verify](https://github.com/parkjui92/fact-verify) (source verification) · [paper-proofread](https://github.com/parkjui92/paper-proofread) (Korean academic proofreading) · [form-tailor](https://github.com/parkjui92/form-tailor) (institutional document formats) · [report-to-brief](https://github.com/parkjui92/report-to-brief) (report compression)

## License

[MIT](LICENSE). No proprietary institutional templates and no real client deliverables are included (bring-your-own-template principle).
