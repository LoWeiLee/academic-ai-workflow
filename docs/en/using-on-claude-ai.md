# Using the Skills on claude.ai: Seven Standalone Tools

> English translation of [在-claude-ai-上使用.md](../在-claude-ai-上使用.md). Where wording differs, the Chinese original governs.

The full form of this workflow is **a pipeline**: seven stages share one persistent workspace folder, and each stage's output lands automatically where the next one can read it. This requires running in Claude Cowork or Claude Code — that is, a paid plan (Pro and above) together with the [Claude desktop app](https://claude.com/download).

But if you just want to try things out at a small scale first, **all seven skills can be installed on the claude.ai web interface, and Skills are available from the free plan up.** The difference: on claude.ai you get not a pipeline but **seven standalone tools** — open one conversation today to discuss your paper's structure, open another tomorrow to analyze one piece of literature, and you hand files between stages manually. And if you already have another AI model you are used to, the design concepts carry over as well.

This document is written for exactly that kind of use. It is not "a stripped-down manual for the full workflow" but **an operating manual for standalone, single-skill use**.

Whichever skill you use, though, I consider skill 1 essential: the paper-structure.md it produces is the core of your research. Of course, if you are used to writing it yourself, you can skip skill 1. What I want to convey is that in a research workflow, a **clear overall research structure and plan** is the core and starting point of good research.

## 1. Installation (one-time)

1. **Settings → Capabilities**, enable **Code execution and file creation**. Skills only appear when a code execution environment is available.
2. **Customize → Skills** → click "+" → "Create skill" → "Upload a skill".
3. Upload the `.skill` files inside `skills/packaged/`. Each is itself a zip — **upload it directly, no unpacking needed**; `references/` (templates, reasoning frameworks) and `scripts/` are uploaded intact with the package.

**The minimal starting set is the same as in the full environment — you do not need to install all seven.** The ones a researcher will most likely use are research-design-diagnosis (research design) plus literature-analysis (per-paper analysis); these two form the complete loop of "think the structure through first, then read the literature in depth". For standalone use you can add **review-diagnosis** (review diagnosis), the skill among the seven that depends least on file governance — upload a manuscript and it works. For these three, the experience on claude.ai is nearly identical to the full environment.

Interface options may change across versions; refer to the official documentation for details.

## 2. One-time preparation: put the control files into a Project

On claude.ai, **Projects are available even on the Free plan**, and Project files enter the skill's code execution environment — **this is what makes standalone use viable**.

Create a Project (for example, "My research") and put these files into Project files:

| File | Why it goes in | Who reads it |
|---|---|---|
| `about-me.md` | Your goals, timeline, self-declared writing habits | skills 1, 2, 4, 5 |
| `research-identity.md` | Your theoretical landscape and methodological stance (determines how deeply the AI engages with you) | skills 1, 3, 5, 7 |
| `writing-standards.md` | Prohibited-items list, citation format, academic Chinese register | skills 1, 4, 5, 6, 7 |
| `paper-structure.md` | **The hub of the entire pipeline** (produced by skill 1, then placed here) | skills 2, 3, 4, 5, 7 |

Once they are in the Project, every conversation opened inside that Project can read them — **you do not have to re-upload them each time**. With this step done, "standalone single-skill use" goes from tedious to smooth.

You can run without a Project too; you will just have to drag the control files into the attachments of every conversation.

## 3. Skills auto-detect the environment (since v1.1.0)

The skill instructions are anchored on **paths** such as `00_專案控制/paper-structure.md`. On claude.ai those paths do not exist.

**Since v1.1.0, all seven skills run an environment check at startup**: when the workspace folder is not found, they automatically switch to workspace-less mode — looking for control files in conversation attachments and Project files instead, delivering outputs as downloadable files, and telling you in the startup announcement that "this session runs in workspace-less mode". You do not need to do anything.

**If a skill still reports that it cannot find files** (for example, you installed the older v1.0.1, or detection fails), add this at the start of the conversation:

> This session is claude.ai standalone single-skill mode; **there is no workspace folder**. All control files from `00_專案控制/` have been placed in the Project files (or attached to this message) — read them from there, and do not abort because the folder path cannot be found. Deliver all outputs as **downloadable files**; do not attempt to write to `05_輸出/`.

## 4. Standalone-use card for the seven skills

| # | Skill | Standalone availability | What you feed it | What it hands back |
|---|---|---|---|---|
| 1 | research-design-diagnosis | **Fully usable** | Project files (control files) + your research idea | `paper-structure.md` (download it and put it back into Project files) |
| 2 | literature-search | **Automated search unavailable** (see Section 6) | `paper-structure.md` | Manual-export mode only: you search yourself and paste DOIs back; the skill continues with bucketing and the import list |
| 3 | literature-analysis | **Fully usable** | One PDF (conversation attachment) | Knowledge file + application file + merged .docx |
| 4 | literature-synthesis | **Usable (file-count cap)** | Multiple same-topic **knowledge files + application files** (outputs of skill 3) | Synthesis knowledge file + synthesis application file |
| 5 | chapter-drafting | **Usable (cross-conversation hurts the most)** | `paper-structure.md` + the topic's synthesis files + `writing-standards.md` | Chapter draft .md |
| 6 | review-diagnosis | **Fully usable** | Your manuscript (PDF/docx) | Review report .md/.docx |
| 7 | thematic-analysis | **Usable (cross-conversation somewhat painful)** | De-identified transcripts | Codebook, theme map, thematic narrative skeleton |

**The four "fully usable" ones (1, 3, 6, plus 4 at modest scale) are claude.ai's sweet spot.** They are naturally single-shot tasks: one piece of literature at a time, one manuscript at a time, one round of structure discussion at a time. What a workspace folder provides is something they never needed much of anyway.

One common confusion worth clearing up along the way: **"help me synthesize this paper" (a single one) is actually skill 3 (per-paper analysis), not skill 4.** Skill 4 takes "the outputs of multiple completed per-paper analyses" and builds the cross-paper theoretical landscape and research gaps; feeding a single paper into skill 4 makes no sense.

## 5. Handoffs between stages: you are the pipeline

In Cowork, skill 3's output lands in `05_輸出/`; you review and approve it, move it into the literature library, and skill 4 reads it on its own. On claude.ai, you walk this path manually:

1. **Skill 3 conversation**: upload the PDF → receive the knowledge file + application file → **download**.
2. **You review and approve**: read them, confirm the quality. This step is the same in both environments — it is a sign-off that cannot be outsourced.
3. **Skill 4 conversation**: upload the approved knowledge/application files (or put them into Project files) → receive the synthesis files → download.
4. **Skill 5 conversation**: feed in the synthesis files + `paper-structure.md` → receive the chapter draft.

What is tedious is moving files; what is not tedious is the decisions — and **the real value of this workflow (AI produces, you sign off) is fully preserved**. In fact, the read-only protection on claude.ai is even harder than in Cowork: the AI cannot touch any file on your computer at all, so an accidental write is physically impossible. The price you pay is serving as your own porter.

I still recommend organizing the downloaded files on your machine following the 00–05 skeleton in `starter-kit/`, so that if you later upgrade to Cowork, the whole workspace connects seamlessly.

## 6. Three real limitations

### (1) literature-search's automated search is unavailable

The claude.ai sandbox's approved domains form a **fixed allowlist**: PyPI, npm, GitHub, Ubuntu, crates.io, and the Anthropic API. It does **not include** `api.openalex.org` or `api.semanticscholar.org`, and Free/Pro/Max users cannot add domains themselves. The three search scripts will inevitably be blocked with 403.

The skill has built-in handling for this: it **declares "blocked by the environment" and switches to manual-export mode**, rather than disguising the 403 as "zero results" — and it will never fabricate a candidate pool from model memory. In manual mode you search yourself via the OpenAlex web interface or Zotero, paste the DOIs back into the list, and continue with bucketing and import.

Exception: **organization owners on Team/Enterprise plans can customize the domain allowlist**; once these two APIs are added, automated search works.

### (2) State does not carry across conversations

Skills 1, 5, 6, and 7 rely on `05_輸出/progress-log.md` to resume from checkpoints; chapter-drafting moreover uses files as the source of truth for "frozen paragraphs", preventing the AI from going back and altering paragraphs you have already finalized. claude.ai has no persistent files, so these mechanisms fail.

**Workaround**: in every follow-up conversation, re-upload the previous round's output and state up front:

> This is round N. The previous round's output is attached; paragraphs X and Y are frozen. Continue from paragraph Z, and do not modify the frozen paragraphs.

Hardest hit are **chapter-drafting (skill 5)** and **thematic-analysis (skill 7)** on long datasets — the two skills designed to span multiple sessions in the first place. Practical advice: **finish one section / one phase per conversation**; do not split work too finely across conversations.

### (3) File-count caps

claude.ai conversation attachments have count and size limits (generally 20 files per conversation and 30MB per file; Project files capacity varies by plan). This bites **skill 4 (cross-paper synthesis)** the hardest: 15 papers = 30 files, which exceeds a single conversation's attachment quota.

Pick one of two countermeasures: **merge the same-topic knowledge files into a single .md** before uploading; or use skill 4's built-in **batched-synthesis guardrail** (each batch of ≤10 papers produces an intermediate summary first, merged at the end). The skill reports the paper count and the batching plan at startup.

## 7. When to upgrade to Cowork / Claude Code

In short, **this workflow does work on claude.ai** — it is just clunkier and asks more actions of you.

But if your usage is "**occasionally getting the AI to discuss research structure, analyze one piece of literature, or review one manuscript**", claude.ai is entirely sufficient — no need to upgrade. Those three things are precisely the parts of this workflow that depend least on file governance and deliver the most value.

Only when any of the following applies does the pipeline's value start to outweigh the cost of moving files:

- You want to run **literature-search**'s automated pool building (the only hard reason)
- Your knowledge files have accumulated to the point of needing **cross-project reuse**, and file management starts eating your time
- You want to use **chapter-drafting** to actually write complete chapters (cross-session protection of frozen paragraphs is this skill's core mechanism)
- You have decided to **commit to Claude** and use this workflow long term

---

*Back to the [Quick Start Guide](./quick-start-guide.md) | [Workflow Architecture Whitepaper](./architecture-whitepaper.md)*
