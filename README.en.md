# socsci-paper-kit

[![Version](https://img.shields.io/badge/version-0.11.0-blue.svg)](CHANGELOG.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Claude Code](https://img.shields.io/badge/Claude_Code-Plugin-purple.svg)

[한국어](README.md) · **English**

A [Claude Code](https://claude.com/claude-code) plugin that writes a social science paper for you, start to finish.

Give it a topic and it works out the research question and hypotheses, finds the prior literature, writes the body, and produces a submission-ready Word file (`.docx`) plus Markdown. Six AIs split the work, and one of them **only reviews** — so the AI that wrote the text can never sign off on its own work. That's the whole idea.

## What makes it different

What this plugin guards is not the prose. It's the **citations** — and citation problems aren't the kind you catch by reading. You catch them by **cross-checking**: matching each in-text citation against the reference list, then walking the list backwards and finding every entry in the body. Two things fall out:

- **Citations to papers that don't exist** — a plausible author and year are attached, so reading right past them is easy
- **References in the list that appear nowhere in the body** — leftovers from a paragraph that got cut

It's the most tedious job in finishing a manuscript, which is exactly why it doesn't get done the night before a deadline. This plugin just does it, mechanically.

| | Plain Claude Code | This plugin |
|---|---|---|
| Does it cross-check citations? | Ships with citations attached, and that's it | Matches body against reference list **one by one** (appendices included) |
| Who reviews it? | The AI that wrote it reads its own work | **A different AI** re-reads the files and checks |
| Does the work leave a trail? | One manuscript file | Design, review findings, source list, and revision log stay as files |

One thing I'll be straight about: **that table describes how it's built, not something I measured.** I haven't yet run this kit side by side against plain Claude Code. A sister kit built the same way does have that measurement, so take a look there.

→ [Why I built this, and fuller usage notes](docs/why.md) · [A sister kit's side-by-side test](https://github.com/parkjui92/policy-research-kit/blob/main/docs/vanilla-vs-kit.md)

## How it runs

```
Design → 🚦Check 1 → ★You confirm the outline and hypotheses
       → Literature review + data analysis (at the same time) → Writing → 🚦Check 2 → Copy-edit → Word file
```

It **stops twice.** The first stop looks at direction before any writing happens: hypotheses nothing could confirm, research questions nothing could answer, concepts that are named but never pinned down to something you can actually count or measure. Leave those in and finish the paper, and there's no cheap way back.

The second stop reviews the finished draft, because polished writing is hard to doubt on your own. It's done by **a different AI that didn't write anything**, and that AI **can read but not edit** — with no power to change the text, it has no way to quietly smooth a problem over.

The review asks five things: ① did it actually answer the research question and hypotheses ② are the citations and sources real ③ does the argument hold together ④ is the method sound ⑤ does the Korean read well. Number ② is the center of gravity. Papers built on numbers (statistical work, citation-data studies) get a stricter version that asks what exactly was measured and how, whether there's real ground for a causal claim, and whether the write-up overstates what the results show.

Caught in practice: 2 citations to papers that don't exist, 1 reference listed but never used in the body.

It also checks whether **the cited paper actually says what the sentence claims**. The writing AI tags each citation with an invisible note pointing to the page or passage in the source; the reviewing AI opens that spot and compares. The notes are stripped from the final Word file.

## After peer review

When reviewer comments come back from a journal, the plugin handles that stage too. Three things usually go wrong in a revise-and-resubmit:

- **Gaps** — one comment contains two or three requests and only one gets answered
- **Paper promises** — the response letter says "revised" but the manuscript didn't change
- **Spillover** — fixing one spot rewrites untouched sections and creates new problems

So the comments are split into individual requests, and **you decide** for each one whether to revise, partially revise, or rebut. The AI edits only the spots you approved, and a script diffs the before/after manuscripts to catch edits outside that list. The response letter is written only from changes that actually appear in the diff. Finally, a fresh reviewer that took no part in the revision simulates re-review **without seeing the response letter first**, judging the manuscript changes on their own.

## Install

```
/plugin marketplace add parkjui92/socsci-paper-kit
/plugin install socsci-paper-kit@socsci-paper-kit
```

For proper Korean copy-editing, install [paper-proofread](https://github.com/parkjui92/paper-proofread) alongside it. Without it, the fifth review question above covers that work instead.

## Using it

Just ask in plain language.

```
Write a paper on platform workers' social insurance. Survey data attached.  ← you have data
No data — a theoretical paper from a literature review.                     ← analyst drops out
Review this draft. Start with the citations.                                ← fixing an existing one
Redesign the hypotheses as a moderation model                               ← at the confirm step
Reviewer comments are in. Sort them, revise, and draft the response letter. ← after peer review
Check my response letter for anything I missed.                             ← response letter only
```

The fourth one matters: when it shows you the outline and hypotheses, asking for changes rebuilds them right there. **It's the cheapest moment to change direction.** And you can step away while it's paused.

## What you end up with

Not just a finished paper — **the whole process stays on disk as files.**

The research design, what the first check flagged and why, a list of which fact came from which source, the data analysis, the draft, what the second check found and what was actually changed, and the final Word file.

Which means that months later, when a reviewer asks where a citation came from, you can answer. Don't delete the `_workspace/` folder — re-running just one part works off these files.

## Good to know

- A full paper **takes a while**, mostly literature search and verification. If you're in a hurry, say "do it fast" — it splits the literature search into parallel runs and writes chapters in batches. If a stage runs well past its expected time, it shows you the finished intermediate results and asks whether to continue. **The reviewing AI and the data analysis are never downgraded**, whatever the speed setting — ghost citations and wrong numbers are fatal in a paper.
- If the Word conversion fails, you get the Markdown manuscript first, plus instructions for converting it yourself.
- **The checks reduce errors but don't eliminate them.** The reviewing AI comes from the same model family and can share the same blind spots. A person still needs to look.
- **Paywalled academic databases** (DBpia, Scopus, Web of Science) can only be checked if *you* have access. A citation that couldn't be confirmed isn't quietly deleted — it stays marked "needs verification."
- It's shaped around Korean academic practice: the copy-editing works on Korean prose, and the searching covers KCI, RISS, and DBpia because that's where the domestic literature lives. For an English-language journal you'd swap those two out, and **everything else works the same regardless of language.**
- [If setup gives you trouble](docs/runtime-notes.md) · [Building this kind of review structure yourself](docs/verification-gates.md)

## Related work

**Plugins that write reports and proposals** — [policy-research-kit](https://github.com/parkjui92/policy-research-kit) (policy research reports) · [rnd-proposal-kit](https://github.com/parkjui92/rnd-proposal-kit) (Korean government R&D proposals)

**Plugins that build and edit** — [lecture-deck-kit](https://github.com/parkjui92/lecture-deck-kit) (HTML lecture slides you edit right in the browser)

**Single-purpose tools** — [fact-verify](https://github.com/parkjui92/fact-verify) (check whether sources are real) · [paper-proofread](https://github.com/parkjui92/paper-proofread) (Korean academic proofreading) · [form-tailor](https://github.com/parkjui92/form-tailor) (match an organization's document format) · [report-to-brief](https://github.com/parkjui92/report-to-brief) (shorten long reports)

## Credits

The peer-review response stage, citation-location checks, and re-review discipline were inspired by the design of [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) (Imbad0202, CC BY-NC 4.0) and rewritten from scratch for Korean journal practice. No text or code was copied.

## License

[MIT](LICENSE). Contains no organization-specific templates and no real client deliverables.
