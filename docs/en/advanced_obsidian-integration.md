# Advanced: Knowledge Base and Obsidian Integration

> English translation of [進階_知識庫與Obsidian整合.md](../進階_知識庫與Obsidian整合.md). Where wording differs, the Chinese original governs.

This document explains how to accumulate the literature outputs of the seven stages into a cross-project literature knowledge base you can reuse over the long term. It is an optional enhancement layer, not a requirement of the core workflow: with just the control files, folder governance, and the seven skills, you can already complete the literature work for a paper. But if you want "a piece of literature analyzed for this paper never has to be re-read for the next one", and want to see at a glance "which papers have cited the same piece of literature", this layer amplifies the value of the earlier stages.

The following walks through the order in which literature actually moves through the workflow, from collection to building the knowledge base.

## 1. Collection: Zotero and the literature pool

The literature-search stage uses APIs to generate a candidate literature pool, verifies each DOI one by one, and finally outputs a DOI list, `zotero_import_dois.txt`. On your own machine you open Zotero and use "Add by Identifier" to paste in this batch of DOIs for bulk import; Zotero does its best to fetch the PDFs, and those it cannot fetch you fill in manually following the list's prompts. The PDFs are obtained by you locally — the workflow does not fetch them on your behalf, which is at once a technical limitation and a copyright boundary. Place the obtained PDFs into the current paper project's `01_文獻/` for the next stage to read.

Zotero's role in the overall design is not just fetching PDFs: it provides a stable `citation_key` for each piece of literature, and this key later becomes the bridge between the knowledge base and Zotero.

## 2. Analysis: two files per paper

The per-paper analysis stage (literature-analysis) produces two files for each PDF. The knowledge file records what the literature itself says — independent of any paper of yours, reusable across papers; the application file records what it does for your current paper, bound to a paper number. This two-file separation is the precondition for a knowledge base that accumulates over the long term: the knowledge is set down once, and for a new paper you only add one new application file.

Both file types carry YAML frontmatter at the top, letting the same `.md` serve three ends at once: on the workflow side, the synthesis stage parses it to build literature lists (regardless of execution environment — the skills on claude.ai read the frontmatter just the same); on the Obsidian side, it supports graph view and backlinks; on the Zotero side, the `citation_key` links back to the original entry.

## 3. Synthesis: across papers

The cross-paper synthesis stage (literature-synthesis) integrates multiple analyses into a theoretical knowledge map with explicit attribution to the literature, likewise outputting a synthesis knowledge file and a synthesis application file. By this point, both per-paper and cross-paper knowledge have taken shape; only then does anything enter the knowledge base.

## 4. Promotion into the vault

The outputs of every stage land first in the current project's `05_輸出/`. After you have read them and confirmed their quality, you move the finalized versions into the literature vault by hand. The AI does not write into the vault directly; promotion is your sign-off, and the last gate protecting the master copies in the knowledge base. The merged docx version (knowledge followed by application) stays in the paper project folder for reading and commenting in Word — it does not enter the vault.

## 5. Building and running the knowledge base

The vault follows a "single folder, three roles in one" design: the same folder is simultaneously your manually curated literature library, your Obsidian vault, and your Zotero attachment library — there is no second copy to maintain. The path is yours to choose, for example `3_文獻/` under a cloud-synced folder.

For layout, knowledge files live under a category tree, for example `理論基礎/[主題]/`; when a PDF is promoted into the vault, it is renamed to share the knowledge file's prefix, `[主題]_[作者年份]_[關鍵詞].pdf`, and sits in the same folder beside the knowledge file. Application files live in `應用/[論文編號]/`. At the vault root sits an index, `_index.json`, recording each literature item's topic, file locations, and which papers have cited it.

Links are the key to this layer, and they are deliberately made folder-independent: cross-file links always use Obsidian's basename wikilinks, never folder paths, so reorganizing folders later will not break them. Two links matter most. The line right below a knowledge file's title carries `> 📎 原文 PDF：[[主題_作者年份_關鍵詞.pdf]]`, letting you open the PDF with one click inside the vault; the application file's body carries `> 🔗 對應知識檔：[[..._知識]]`, and it is this line that drives Obsidian's backlinks. The `pdf_path` and `knowledge_note` fields in the frontmatter are metadata only — they do not automatically generate clickable links.

## Why it is worth it

The two-file separation, plus that `[[..._知識]]` wikilink, buys you a knowledge base that automatically answers a question that is normally hard to track: which papers have cited the same piece of literature. Open any knowledge file, and Obsidian's backlink panel lists every application file that has used it — that is, every paper that has used this literature. The more literature you accumulate and the more papers you write, the more valuable this cross-project citation network becomes. This is exactly the payoff of the two-file design that is invisible at the single-paper level and only cashes out at the knowledge-base level.

A reminder once more: this layer is optional. It requires you to adopt two specific tools, Obsidian and Zotero; without them, the core workflow runs just the same — you merely forgo the enhancement of automatic cross-project accumulation and backlinks. Whether it is worth it depends on whether you have a long-term need to reuse literature across multiple papers.
