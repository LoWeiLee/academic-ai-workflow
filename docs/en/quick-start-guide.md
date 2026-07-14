# Quick Start Guide: From Clone to Your First Literature Analysis

> English translation of [快速上手指南](../快速上手指南.md). Where wording differs, the Chinese original governs.

This guide takes you from installation to a working minimal chain of "research design → per-paper analysis" within half a day, using a real, small topic. For the architecture and design rationale, read the [architecture whitepaper](./architecture-whitepaper.md) first. You need not read it word for word, but do read at least Sections 2 and 3 to understand the three-layer architecture and the governance logic of "05_輸出 is the only writable area" — so that when you operate, you know what you are doing.

## Before You Start

**Environment.** There are two ways to use this workflow; pick one first:

**A. Pipeline mode (the main path of this guide)**: the seven stages share one **persistent workspace folder**, so the output of one stage lands automatically where the next stage can read it. This requires the Claude desktop app's **Cowork** mode, or **Claude Code**; all steps below assume this setup. Cowork comes with any paid plan (Pro and up) and is used inside the [Claude desktop app](https://claude.com/download); see the [official guide](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork) for how to get and open it.

**B. Standalone-tool mode (claude.ai web)**: all seven skills can be installed on claude.ai, and **Skills are available from the Free plan up** (just enable Code execution under Settings → Capabilities). What you get is not a pipeline but seven independent tools: open one conversation today to discuss your paper's structure, open another tomorrow to analyze a piece of literature, and hand files between stages manually yourself. **This path requires no payment and no desktop app**, and for three of the skills — research-design-diagnosis (research design), literature-analysis (per-paper analysis), and review-diagnosis (review diagnosis) — the experience is nearly indistinguishable from the full environment.

Simply put, this was designed around the academic research workflow to begin with: mode A merely uses AI tools to string the individual work points into a chain, while mode B adds AI assistance to each of those work points as they already exist.

| | claude.ai (standalone tools) | Cowork / Claude Code (pipeline) |
|---|---|---|
| Install all seven skills (incl. references/scripts) | Yes | Yes |
| Read control files, PDFs, transcripts | Yes (Project files / conversation attachments) | Yes (workspace folder) |
| Produce .md / .docx / .xlsx | Yes (download) | Yes (written to `05_輸出/`) |
| Handoff between stages | **Manual file moves** | Automatic (`05_輸出/`) |
| Cross-conversation continuation (`progress-log.md`, frozen chapter sections) | No | Yes |
| literature-search automated search | No (sandbox allowlist excludes OpenAlex / S2) | Yes |

**If you take path B, read [Using on claude.ai](./using-on-claude-ai.md) instead** — that document is the complete operating manual for standalone use (including Project files preparation and standalone usage cards for all seven skills). In the rest of this guide, Step 3.5, Step 4 (2)(3)(5), Step 5, and the first FAQ entry all assume you have a workspace folder.

**Other**: Zotero (free reference-management software, used to obtain PDFs); a cloud-synced folder (OneDrive, Dropbox, etc. — recommended but not required; version history is this workflow's last line of insurance).

## Step 1: Get the Package and Create Your Workspace

```
git clone https://github.com/LoWeiLee/academic-ai-workflow.git
```

If you are not familiar with git, simply click "Code → Download ZIP" on the GitHub page and unzip — the effect is the same.

Next, copy the entire `starter-kit/` folder to the location you intend to use long-term (for example, inside a cloud-synced folder) and rename it to your workspace name. Inside the workspace is the complete folder skeleton:

| Folder | Purpose | Read/write rules |
|---|---|---|
| `00_專案控制/` | The four control files (who you are, how to collaborate) | Read-only during task execution (sole exception: literature-analysis writes back the "completed literature analysis list" in `paper-structure.md` per its protocol) |
| `01_文獻/` | Literature library (PDFs and finalized analyses) | Read-only; promotion is performed by you manually |
| `02_資料與證據/` | Primary data (interview transcripts, datasets) | Read-only |
| `03_寫作/` | Finalized chapters | Read-only; you move finalized drafts in manually |
| `04_審稿與回應/` | Review comments and responses | Read-only |
| `05_輸出/` | The only writable area for all AI output | AI-writable |

Each of the folders 01–05 contains a README with the detailed rules (the rules for 00_專案控制/ are written directly in the four control files). The workspace root also holds a `CLAUDE.md`, which restates the governance rules in the table above as a version the AI reads at the start of a session: once the workspace is mounted, it loads automatically — so even if you trigger no skill at all and simply ask the AI in plain conversation to work on files, the read-only zones and the promotion process still hold. Just remember one main line: the AI can write only to `05_輸出/`; every file anywhere else was placed there by your own hand.

## Step 2: Control Files — Four in Place, Two Must Be Filled In

This is the most important step of the whole installation, and the one you can least afford to phone in: the quality of the control files directly determines the quality of AI collaboration. All four templates are in `00_專案控制/`, each field accompanied by filling-in guidance and fictional example sentences (the examples show you the format; replace all of their content with your own).

First, keep two things straight:

**All four must stay in `00_專案控制/`.** Skills read them directly, and a missing file will break a stage — for example, if chapter-drafting cannot read `writing-standards.md`, it will stop and ask you to supply it. So do not delete them and do not move them away.

**But for the first run you only need to put pen to paper on two of them:**

1. **`about-me.md` (required)**: your goals, schedule pressure, hours per week you can devote to research, and your priority rules when multitasking. In the "self-declared writing habits" section, be honest with yourself — the more concretely you describe your known bad writing habits (literature reviews that will not stop growing? over-abstraction? trouble writing openings?), the more accurately the AI can intercept them.
2. **`research-identity.md` (required)**: your research positioning and theoretical map, graded into five levels by depth of command. This determines the depth at which the AI speaks to you — it is the reason it will not lecture you on basics as if you were an undergraduate.
3. `writing-standards.md` (keep the default): the template already carries a complete list of prohibitions, citation formats, and provisions on academic-Chinese tone; skim it once, no changes needed. Leave the "personal style library" empty for now and build it up over time.
4. `portfolio-status.md` (may stay empty): a dynamic dashboard of your publication portfolio. With only one paper in flight there is no portfolio to speak of; fill it in once you are genuinely running multiple lines in parallel.

For the first pass, capture the big things and let the small ones go; come back and revise after two or three weeks of use, and it will be far more accurate.

## Step 3: Install the Skills

`skills/packaged/` contains the seven packaged `.skill` files (that is, skill folders packaged in zip format); `skills/1-*` through `7-*` are the corresponding source files.

**Claude desktop app (Cowork) users**: open the Claude desktop app → Settings → Capabilities → Skills → Upload skill → select the `.skill` file. **Claude Code users**: unzip the `.skill` file and place the resulting folder in a skills directory (the personal level `~/.claude/skills/` for cross-project use, or the project's own `.claude/skills/` for a single project). **claude.ai web users**: Settings → Capabilities → enable Code execution → Customize → Skills → upload the `.skill` file (`references/` and `scripts/` are uploaded as part of the package; no need to unpack). Interface options may shift across versions; for details, follow the official documentation for the version you are using.

After installation, no commands are needed; simply trigger the skills in conversation with natural language (for example, "help me analyze this paper").

You do not have to install all seven at once. **The minimal start needs only two: research-design-diagnosis (research design) and literature-analysis (per-paper analysis).** These two form a complete closed loop: first think your research structure through, then have the AI deeply analyze the literature in your hands. Once you are familiar with the rhythm, add the remaining five as needed (for literature-search, which builds literature pools automatically, see Step 5).

## Step 3.5: Hand the Workspace to Claude

**This step cannot be skipped**: by default, Claude sees none of the files on your computer. You must explicitly hand it the workspace folder you created in Step 1 before it can read `00_專案控制/` — or write into `05_輸出/`.

In the Claude desktop app, after entering Cowork mode, use the folder entry point in the conversation interface to select your workspace folder (the folder you copied and renamed in Step 1 — **select the whole workspace, not one of its subfolders**). Button names may vary across versions; what you are looking for is a "select / add folder" kind of entry point. Follow the official documentation for the version you are using. Claude Code users: simply launch it inside the workspace folder.

**Confirm the workspace is connected every time you open a new conversation.** This is the most common sticking point for newcomers: however well your control files are written, if the workspace is not connected the AI simply cannot read them, and the whole chain cannot start.

## Step 4: Run Your First "Research Design → Per-Paper Analysis"

Pick a topic you genuinely care about but that is very small in scope — say, a concept needed by one section of your next paper. Do not use a made-up topic; a fake topic cannot test the feel of the human-AI division of labor.

**(1) Start research design and think the structure through.** Tell Claude, "I want to start writing a paper on ⟨some topic⟩ — help me build the structure." research-design-diagnosis will walk you through it stepwise (chapter → section → subsection). Along the way there is a commitment gate: at three decision points — working direction, core research question, and contribution claim — **you must state your own answer first before the AI gives its version**. This order must not be reversed: if you look at the AI's answer first and then "choose," your framing has already been anchored.

**(2) Promote the structure file.** The output of stage 1 lands in `05_輸出/`, with a filename like `paper-structure_⟨paper name⟩_章層級_⟨date⟩.md`. **After reading it and confirming it is correct, rename it to `paper-structure.md` and move it into `00_專案控制/`.** This step is required: `paper-structure.md` is the hub of the entire pipeline, and stages 2 through 5 all look for it at the anchor path `00_專案控制/paper-structure.md`; if it has not been moved there, downstream stages will fail to find it and break. (It is normal for `00_專案控制/paper-structure.md` not to exist initially — it is produced by stage 1 in the first place.)

**(3) Get the PDFs with Zotero.** Find a few pieces of literature you genuinely need to read for this section, import them with Zotero to obtain the PDFs, and put them into `01_文獻/`. PDF acquisition is done by you on your own machine; the workflow does not fetch them on your behalf — this is both a technical limitation and a copyright boundary. (If you want the AI to help you build a candidate literature pool, see Step 5.)

**(4) Start per-paper analysis.** Tell Claude, "help me analyze this paper." When the analysis completes you will receive two files: the **knowledge file** (what this piece of literature itself says, independent of your paper, permanently reusable) and the **application file** (what use it is to this particular paper of yours). This two-file separation is the signature design of this workflow: when a future paper draws on the same literature, the knowledge file is reused directly and only a new application file needs to be added. (To see what the finished product looks like: `skills/3-literature-analysis/references/` in the repo includes complete examples of a [knowledge file](../../skills/3-literature-analysis/references/example-literature-knowledge.md) and an [application file](../../skills/3-literature-analysis/references/example-literature-application.md), both demonstrations on fictional literature.)

**(5) Review and promote.** The output lands in `05_輸出/`. After reading it and confirming the quality, you move the finalized version into `01_文獻/` with your own hands. That act of "moving the file" is your sign-off: the AI produces, you stamp.

Once you have run these five steps, you have experienced all of the core logic of this workflow: the structural anchor, human-AI checkpoints, the citation-authenticity defense line, the two-file architecture, and output promotion. Everything that comes later (literature search, cross-paper synthesis, chapter drafting, review diagnosis) is an extension of the same rhythm.

## Step 5 (Optional): Add literature-search to Build Literature Pools Automatically

Once you are familiar with the rhythm, literature-search is the next skill with the highest return on investment: it spares you the first-pass screening of literature retrieval. Note that it requires an environment that can run scripts and reach the external network, and its token consumption is relatively high.

After installing it, tell Claude, "find me literature on ⟨topic⟩ and build a literature pool." It will use `00_專案控制/paper-structure.md` as its basis for interpretation (which is why the promotion in Step 4 cannot be skipped), and the process passes through several checkpoints adjudicated by you: confirming the seed literature, confirming the search keywords, and ruling on the bucketing results (include / hold / exclude). You will notice that every reference the AI recommends has passed DOI verification, and every step is recorded in the search log. This is not red tape; it is the core guarantee of this workflow: **the candidate pool will contain no literature the model fabricated from memory**.

When the search completes, it produces a DOI list (`zotero_import_dois.txt`). Open Zotero, use "Add by Identifier," and paste in the DOIs for batch import; Zotero will do its best to fetch the PDFs, and for any it cannot fetch, fill them in manually following the list's notes. Then return to Step 4 (4) for per-paper analysis.

**Advanced option (skippable)**: OpenAlex has a "polite pool" mechanism — requests carrying a contact email receive more stable service quality. `MAILTO` in the scripts defaults to a placeholder, and **the scripts run fine without changing it**; if you want to set it, edit the `MAILTO` value in the three scripts under `scripts/` of the skill copy you actually installed (editing the source files in the repo will not affect the packaged version already installed). When a script detects the placeholder, it prints a one-line notice but does not interrupt execution.

## FAQ

**The AI says it cannot find `00_專案控制/` or cannot see my files?** Nine times out of ten the workspace is not connected (see Step 3.5). Reconfirm every time you open a new conversation.

**A skill says it cannot find `paper-structure.md`?** It is normal for this file not to exist initially — it is produced by stage 1 (research-design-diagnosis). Once produced, it lands in `05_輸出/`; make sure you have renamed it and moved it into `00_專案控制/` (see Step 4 (2)). If you just want to try literature-search first without running stage 1, you can also handwrite a simplified version: at minimum, write out two fields — the research question and the theoretical framework.

**The search reports "environment blocked" or zero results?** Check whether your execution environment allows outbound network access (the OpenAlex and Semantic Scholar APIs). The workflow explicitly distinguishes "the environment is broken" from "there really is no literature," and never pads results from memory; if the environment is restricted, switch to manual import mode as prompted.

**Can I skip the control files and just use the skills?** Technically some skills will run in degraded mode, but you will lose the most valuable part of this workflow: the AI's calibration to *you*. Strongly discouraged.

**Can the output go straight into my paper?** Analysis and synthesis outputs are your research material; chapter-drafting outputs are drafts confirmed by you paragraph by paragraph — but the final responsibility for every citation rests with the author. The workflow greatly reduces the risk of fabrication; it does not transfer that responsibility.

**I only have claude.ai, no Cowork / Claude Code — can I use this?** Yes. All seven can be installed (the Free plan suffices); they just become "seven independent tools" rather than a pipeline: handoffs between stages are manual file moves by you, literature-search's automated search is unavailable, and chapter-drafting's cross-conversation freeze protection is lost. research-design-diagnosis, literature-analysis, and review-diagnosis are almost unaffected. For full instructions, see [Using on claude.ai](./using-on-claude-ai.md).

**Do the seven skills have to be used in order?** The linear order is "design → search → analysis → synthesis → drafting"; review diagnosis cuts across all stages and can be used at any of them, and qualitative thematic analysis is a parallel branch for handling primary data. Entering mid-chain also works (for example, you already have a literature pool and start straight from analysis); each skill checks its prerequisite inputs and tells you whatever is missing.

**Will the PDFs, unpublished manuscripts, and interview transcripts I upload be used to train the AI?** Under Anthropic's current consumer terms (updated August 2025), the Free/Pro/Max individual plans **do by default** use conversation content for model training; you can turn off "Help improve Claude" at any time under Settings → Privacy on claude.ai — once off, new conversations are not used for training and data is retained for 30 days; if left on, retention lasts up to five years. Team/Enterprise commercial plans follow the commercial terms and are not used for training by default. Researchers handling unpublished manuscripts and interview data are advised to turn the option off; transcripts must additionally be de-identified first (thematic-analysis enforces a hard gate on this). As for copyrighted literature PDFs, uploading them for your own analysis and distributing them to others are two different things — do not share full texts with others. Policies may be updated; the [official announcement](https://www.anthropic.com/news/updates-to-our-consumer-terms) and the privacy settings page in your own account govern.

**How many runs will the free plan's quota cover?** Officially no fixed message count is published; quotas fluctuate with model and load. As a rough feel: on the Free plan, a single literature-analysis run on one long PDF may approach the daily cap — suitable for a first taste of two or three skills; for regular research needs, Pro is recommended. Of the seven, literature-search and literature-synthesis consume the most tokens; when quota is tight, economize on these two first (smaller batches, split runs).
