# socsci-paper-kit

[![Version](https://img.shields.io/badge/version-0.9.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)

[한국어](README.md) · **English**

> A [Claude Code](https://claude.com/claude-code) plugin: a **six-agent team** that takes a social science paper from research design — research questions, hypotheses, variables, operational definitions, theoretical framework — all the way to a submission-ready `.docx`.
> What this kit protects is not prose. It's **citations and design** — it checks, twice and on your behalf, whether every in-text citation actually exists in the reference list, and whether analyzing that data with that hypothesis makes sense in the first place.

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

This kit is the personal harness I built by bolting those gates on, one at a time, while writing actual papers — cleaned up and published. In practice, gate 2 has caught **2 ghost citations and 1 orphan reference** on a completed paper run (see the log in [docs/verification-gates.md](docs/verification-gates.md)).

One more reason. Quantitative papers have failure modes that a general review will not catch: treating "no significant evidence" as "no effect," running a staggered-adoption DiD without engaging the literature on standard TWFE bias, reporting analytical cluster standard errors with a small number of clusters. The arithmetic can be entirely correct and the paper still collapses at exactly these points. So there is a dedicated review track for bibliometric and quantitative work — `scientometric-paper-review`.

---

## How it differs from vanilla Claude Code

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

## Pipeline

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

---

## Install

```
/plugin marketplace add parkjui92/socsci-paper-kit
/plugin install socsci-paper-kit@socsci-paper-kit
```

Restart Claude Code and the orchestrator will pick up relevant requests automatically.

For full Korean academic copy-editing, installing the companion skill is recommended — [parkjui92/paper-proofread](https://github.com/parkjui92/paper-proofread). Without it, that work falls back to the reviewer's copy-editing axis.

> **A note for readers outside Korea.** The drafting and review skills are written for Korean-language output, and axis 5 is Korean academic copy-editing — Korean academic prose has its own conventions (spacing rules, translationese imported from English sources, hedging particles) that Korean journals enforce. Likewise, `KCI` (Korea Citation Index), `RISS`, and `DBpia` are Korean academic databases that CrossRef and Semantic Scholar do not index, so sources living there come back "unverifiable" through international tools alone — the investigator searches them directly. If you are writing for an English-language journal, the parts to adapt are axis 5 and the search-source list. **Everything else — the design gate, the citation-integrity protocol, the scientometric axes — is language-independent**, and citation integrity is where this kit earns its keep in any language.

---

## How to use it

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

The bundled example follows exactly this path — [examples/socsci-paper-demo/](examples/socsci-paper-demo/).

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

## What you get

Not one manuscript — **an auditable record set**.

| File | Contents |
|---|---|
| `01_research_design.md` | Design — intent analysis, RQs, hypotheses (variables, operational definitions), theory, method, outline, anticipated risks |
| `02_design_review.md` | Gate 1 ruling — GO / conditional / NO-GO, and what was flagged [required] and why |
| `03_literature.md` | Evidence ledger — search log (databases, queries, hit counts), analysis cards, source tiers, gap analysis |
| `03b_data_analysis.md` | Analysis — integrity check, procedure, results, hypothesis support, limitations (empirical studies only) |
| `04_paper_draft.md` | Body draft + reference list |
| `05_draft_review.md` | Gate 2 five-axis review — location, problem, recommendation |
| `06_paper.docx` · `06_paper.md` · `06_proofread_log.md` | Final manuscript and the record of what was corrected |

Which means that six months later, when a reviewer asks where a citation came from, you can answer. Don't delete `_workspace/` — partial re-runs work off these files.

**A real worked example is bundled.** [examples/socsci-paper-demo/](examples/socsci-paper-demo/) is a complete run of a theoretical/literature study with no data. The topic is synthetic and the scale is demo-sized, but the full process is there, and the thing worth reading is not the finished manuscript — it's **what the gates caught**.

- **Gate 1** flagged that the phrase "mediating pathway" in the RQ overreached the claim scope available to a study with no data (mediation is normally established with data; an integrative review can synthesize proposed mechanisms, not test them). It also escalated a design risk into an instruction: because a boundary-condition proposition is empty unless *both* the enabling and the constraining proposition have support, symmetric evidence for both was made a **blocking condition** on the investigator. The same document is where the analyst **SKIP is confirmed**.
- **Gate 2** cross-checked every in-text citation against the reference list and confirmed **0 ghosts, 0 orphans**. The best part of the example, though, is how the draft handled a 2022 study whose author names could never be confirmed: rather than inventing an `(Author, Year)`, it **referred to the study descriptively only** in the body, tagged it "needs verification," and **withheld it from the reference list**. That is how a ghost citation doesn't get created.

Reading order and what to look for are laid out in [examples/README.md](examples/README.md).

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

## Requirements and fallbacks

- **`.docx` conversion** uses the `docx` skill. If conversion fails, you get the Markdown manuscript first plus instructions for converting manually.
- **Korean copy-editing** is complete when the companion skill [paper-proofread](https://github.com/parkjui92/paper-proofread) is installed; without it, the reviewer's copy-editing axis covers it.
- **Without team-API support**, the same pipeline runs via sequential `Agent` calls. Phase order and the output-file contract are identical.
- **geo-search keys** (`SERPER_API_KEY` or `SERPAPI_KEY`) are optional; without them it falls back to standard search.
- Details: [docs/runtime-notes.md](docs/runtime-notes.md).

## Limitations

- **Gates reduce errors; they don't eliminate them.** The reviewer runs on a model from the same family as the writer and can share its blind spots. Final responsibility stays with the author.
- **There is no measured A/B against vanilla for this kit.** The comparison table above describes structure, not measurement.
- **Subscription and paywalled databases** (DBpia, Scopus, Web of Science) can only be verified if *you* have access. A citation that couldn't be checked is not quietly deleted — it stays marked "needs verification," and the discipline is to not treat that as finished.
- **Research ethics is not automated.** IRB approval, informed consent, authorship, and conflicts of interest are yours. The designer only flags when they apply.
- This kit is tuned to **Korean academic conventions** (Korean copy-editing, KCI/RISS/DBpia as search sources, a balance of Korean-language prior work for domestic journals). For an English-language journal, adapt axis 5 and the search-source list.
- The bundled example is **a synthetic topic at demo scale** (3 references) — short of the 15+ that a real paper needs, a point the example itself raises as a [recommended] finding.

## Further reading

- [docs/verification-gates.md](docs/verification-gates.md) — the two-stage gate design methodology and the log of what it has caught, if you want to build your own
- [docs/runtime-notes.md](docs/runtime-notes.md) — team-API fallback, model selection, geo-search key setup
- [examples/](examples/) — full process artifacts and the order to read them in
- [policy-research-kit / vanilla-vs-kit.md](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md) — the sister kit's measured vanilla-vs-kit audit (policy-research domain)

## Series

Sister kits and standalone skills built on the same design philosophy:

**Agent-team kits** — [policy-research-kit](https://github.com/parkjui92/policy-research-kit) (policy research reports) · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) (Korean government R&D proposals)

**Authoring kit** — [lecture-deck-kit](https://github.com/parkjui92/lecture-deck-kit) (HTML lecture decks with in-browser live editing)

**Standalone skills** — [fact-verify](https://github.com/parkjui92/fact-verify) (source verification) · [paper-proofread](https://github.com/parkjui92/paper-proofread) (Korean academic proofreading) · [form-tailor](https://github.com/parkjui92/form-tailor) (institutional document formats) · [report-to-brief](https://github.com/parkjui92/report-to-brief) (report compression)

## License

[MIT](LICENSE). No proprietary institutional templates and no real client deliverables are included (bring-your-own-template principle).
