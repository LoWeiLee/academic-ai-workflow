#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
split_legacy.py  --  literature-analysis Mode C 批次拆分工具（一次性遷移；版本戳記=SKILL_VERSION）

將舊版的單一分析檔（[主題]_[作者年份]_[關鍵詞]_分析.md）機械切分為：
  1. 知識檔  [主題]_[作者年份]_[關鍵詞]_知識.md           (literature-knowledge, paper-agnostic)
  2. 應用檔  [主題]_[作者年份]_[關鍵詞]_應用_[paper-id].md (literature-application, 綁定 paper_id)

切分依 SKILL.md Mode C 規則，按 "## " 節標題機械切分。不做語意級細拆
（警示欄與 Section 3 第 4 段的精細拆分留待 Mode B 複用時人工補判）。

用法：
    python split_legacy.py <輸入檔或資料夾> -o <輸出資料夾> [--paper-id paper-1] [--vault-prefix 文獻知識]

設計約束：
    - AI / 腳本不直接寫入 Obsidian vault；本腳本只產出至 05_輸出 供使用者審定後手動晉升。
    - 機械切分後標記 needs_review，由使用者抽查校正。
"""

import argparse
import json
import os
import re
import sys
from datetime import date
SKILL_VERSION = "v1.0.0"  # 與 SKILL.md 版本同步升（禁散落硬編版號）

CORE_FIELDS = ["文獻標識", "核心主張", "理論框架", "研究缺口建構方式", "方法設計"]
APP_FIELDS = ["對當前研究的直接用途", "警示"]
ALL_ABSTRACT_FIELDS = CORE_FIELDS + APP_FIELDS

GENERAL_WARN_PLACEHOLDER = "[待補：舊版未分拆，由 Mode B 複用時補判]"


def split_frontmatter(text):
    if text.startswith("---"):
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if m:
            return m.group(1), text[m.end():]
    return None, text


def parse_yaml_simple(fm):
    d = {}
    if not fm:
        return d
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"')
    return d


def parse_filename(path):
    base = os.path.basename(path)
    base = re.sub(r"\.md$", "", base)
    base = re.sub(r"_分析(_v\d+)?$", "", base)
    parts = base.split("_")
    topic = parts[0] if len(parts) >= 1 else "未分類"
    authoryear = parts[1] if len(parts) >= 2 else ""
    keyword = parts[2] if len(parts) >= 3 else ""
    return topic, authoryear, keyword, base


def derive_citation_key(authoryear, keyword):
    m = re.match(r"^([A-Za-z]+)(\d{4})", authoryear)
    if m:
        kw = re.sub(r"[^A-Za-z].*$", "", keyword).lower()
        return m.group(1).lower() + m.group(2) + kw
    return authoryear.lower() + "needsreview"


def split_sections(body):
    lines = body.splitlines(keepends=True)
    sections = []
    cur_head = None
    cur_buf = []
    for ln in lines:
        m = re.match(r"^##\s+(.*)$", ln)
        if m and not ln.startswith("###"):
            if cur_head is not None or cur_buf:
                sections.append((cur_head, "".join(cur_buf)))
            cur_head = m.group(1).strip()
            cur_buf = []
        else:
            cur_buf.append(ln)
    if cur_head is not None or cur_buf:
        sections.append((cur_head, "".join(cur_buf)))
    return sections


def classify(heading):
    if heading is None:
        return "preamble"
    h = heading
    if "銜接摘要" in h:
        return "abstract"
    if "自我檢核" in h:
        return "selfcheck"
    m = re.match(r"^([0-9])", h)
    if m:
        return {"0": "sec0", "1": "sec1", "2": "sec2", "3": "sec3"}.get(m.group(1), "other")
    if "這篇文章在說什麼" in h or "導讀" in h:
        return "sec0"
    if "逐節精華" in h:
        return "sec1"
    if "對當前研究" in h or "具體啟發" in h:
        return "sec2"
    if "批判性評估" in h:
        return "sec3"
    return "other"


def parse_abstract_fields(abstract_body):
    fields = {}
    pat = re.compile(r"\*\*\s*(" + "|".join(map(re.escape, ALL_ABSTRACT_FIELDS)) + r")\s*[：:]\*\*")
    matches = list(pat.finditer(abstract_body))
    for i, mt in enumerate(matches):
        start = mt.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(abstract_body)
        fields[mt.group(1)] = abstract_body[start:end].strip()
    return fields


def match_pdf(topic, authoryear, pdf_dir):
    """在 pdf_dir/topic/ 找出對應 PDF。回傳 (pdf_name, vault_rel) 或 (None, None)。
    依 第一作者姓氏 + 年份 (+ chN 章節) 配對。"""
    if not pdf_dir:
        return None, None
    import glob
    sm = re.match(r"^([A-Z][a-z]+)", authoryear)
    ym = re.search(r"(\d{4})", authoryear)
    cm = re.search(r"(ch\d+)", authoryear)
    if not (sm and ym):
        return None, None
    surname, year = sm.group(1).lower(), ym.group(1)
    ch = cm.group(1) if cm else None
    folder = os.path.join(pdf_dir, topic)
    if not os.path.isdir(folder):
        return None, None
    for fp in sorted(glob.glob(os.path.join(folder, "*.pdf"))):
        name = os.path.basename(fp)
        norm = name.lower().replace(" ", "")
        if surname in norm and year in norm:
            if ch and ch not in norm:
                continue
            if not ch and re.search(r"ch\d+", norm):
                continue
            return name, topic + "/" + name
    return None, None


def build_knowledge_md(meta, fields, sec0, sec1, sec3, selfcheck, needs_review, pdf_name=None):
    ck = meta["citation_key"]
    topic, ay, kw = meta["topic"], meta["authoryear"], meta["keyword"]
    fm = ["---", "citation_key: " + ck]
    if meta.get("title"):
        fm.append('title: "' + meta["title"] + '"')
    fm.append("type: literature-knowledge")
    fm.append("topic: " + topic)
    fm.append("analyzed_date: " + meta.get("analyzed_date", str(date.today())))
    fm.append("analyzed_by_skill_version: literature-analysis-" + SKILL_VERSION)
    fm.append('pdf_path: "' + topic + "_" + ay + "_" + kw + '.pdf"')
    fm.append('zotero_select: "zotero://select/library/items/@' + ck + '"')
    fm.append("tags:")
    fm.append("  - 文獻/" + topic)
    fm.append("aliases:")
    fm.append('  - "@' + ck + '"')
    if needs_review:
        fm.append("needs_review: true")
    fm.append("---")

    out = ["\n".join(fm), ""]
    out.append("# " + topic + "_" + ay + "_" + kw + "_知識")
    out.append("")
    out.append("> 📎 原文 PDF：[[" + topic + "_" + ay + "_" + kw + ".pdf]]")
    out.append("")
    out.append("**範本對齊確認**：本檔由舊版分析檔經 Mode C 機械拆分產生，"
               "格式深度基準為 `references/example-literature-knowledge.md`（隨 skill 同捆範本）。")
    out.append("")
    out.append("## 核心摘要")
    out.append("")
    for f in CORE_FIELDS:
        out.append("**" + f + "：** " + fields.get(f, "[原檔缺此欄，需校正]"))
        out.append("")
    out.append("**通用警示：** " + GENERAL_WARN_PLACEHOLDER)
    out.append("")
    if sec0:
        out += ["## 0. 這篇文章在說什麼：給第一次讀者的導讀", "", sec0.strip(), ""]
    if sec1:
        out += ["## 1. 逐節精華", "", sec1.strip(), ""]
    if sec3:
        out += ["## 3. 批判性評估", "", sec3.strip(), ""]
    if selfcheck:
        out += ["## 原始產出檢核紀錄（舊版）", "", selfcheck.strip(), ""]
    return "\n".join(out).rstrip() + "\n"


def build_application_md(meta, fields, sec2, paper_id, knowledge_rel, needs_review):
    ck = meta["citation_key"]
    topic, ay, kw = meta["topic"], meta["authoryear"], meta["keyword"]
    fm = ["---", "citation_key: " + ck, "type: literature-application",
          "paper_id: " + paper_id, 'knowledge_note: "' + topic + "_" + ay + "_" + kw + '_知識.md"',
          "applied_date: " + meta.get("analyzed_date", str(date.today())),
          "analyzed_by_skill_version: literature-analysis-" + SKILL_VERSION, "tags:",
          "  - paper/" + paper_id, "  - 文獻/" + topic]
    if needs_review:
        fm.append("needs_review: true")
    fm.append("---")

    out = ["\n".join(fm), ""]
    out.append("# " + topic + "_" + ay + "_" + kw + "_應用_" + paper_id)
    out.append("")
    out.append("**脈絡對齊確認**：本檔由舊版分析檔經 Mode C 機械拆分產生，"
               "Section 2 啟發對應 `paper-structure.md` 章節編號。")
    out.append("")
    out.append("> 🔗 對應知識檔：[[" + topic + "_" + ay + "_" + kw + "_知識]]")
    out.append("")
    out.append("## 應用摘要")
    out.append("")
    out.append("**對當前研究的直接用途：**")
    out.append("")
    out.append(fields.get("對當前研究的直接用途", "[原檔缺此欄，需校正]").strip())
    out.append("")
    out.append("**本研究警示：** " + fields.get("警示", "[原檔缺此欄，需校正]").strip())
    out.append("")
    if sec2:
        out += ["## 2. 對當前研究的具體啟發", "", sec2.strip(), ""]
    return "\n".join(out).rstrip() + "\n"


def process_file(path, out_dir, paper_id, vault_prefix, index, pdf_dir=None):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm_raw, body = split_frontmatter(text)
    fm = parse_yaml_simple(fm_raw)
    needs_review = fm_raw is None
    topic, ay, kw, base = parse_filename(path)
    ck = fm.get("citation_key")
    if not ck:
        ck = derive_citation_key(ay, kw)
        needs_review = True
    pdf_name, pdf_rel = match_pdf(topic, ay, pdf_dir)
    if pdf_dir and not pdf_name:
        needs_review = True
    bucket = {"abstract": "", "sec0": "", "sec1": "", "sec2": "", "sec3": "", "selfcheck": ""}
    for head, content in split_sections(body):
        kind = classify(head)
        if kind in bucket:
            bucket[kind] += content
    fields = parse_abstract_fields(bucket["abstract"]) if bucket["abstract"] else {}
    if not fields or any(f not in fields for f in CORE_FIELDS):
        needs_review = True
    meta = {"citation_key": ck, "topic": topic, "authoryear": ay, "keyword": kw,
            "title": fm.get("title", ""), "pdf_path": pdf_rel or fm.get("pdf_path", ""),
            "analyzed_date": fm.get("analyzed_date", str(date.today()))}
    know_name = topic + "_" + ay + "_" + kw + "_知識.md"
    app_name = topic + "_" + ay + "_" + kw + "_應用_" + paper_id + ".md"
    knowledge_rel = (vault_prefix + "/" if vault_prefix else "") + topic + "/" + know_name
    know_md = build_knowledge_md(meta, fields, bucket["sec0"], bucket["sec1"],
                                 bucket["sec3"], bucket["selfcheck"], needs_review, pdf_name)
    app_md = build_application_md(meta, fields, bucket["sec2"], paper_id,
                                  knowledge_rel, needs_review)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, know_name), "w", encoding="utf-8") as f:
        f.write(know_md)
    with open(os.path.join(out_dir, app_name), "w", encoding="utf-8") as f:
        f.write(app_md)
    index[ck] = {"topic": topic, "file": knowledge_rel,
                 "analyzed_date": meta["analyzed_date"], "skill_version": SKILL_VERSION,
                 "applications": [paper_id], "needs_review": needs_review}
    return know_name, app_name, needs_review


def main():
    ap = argparse.ArgumentParser(description="literature-analysis Mode C 批次拆分（一次性遷移）")
    ap.add_argument("input", help="輸入：單一 _分析.md 檔，或包含多個分析檔的資料夾")
    ap.add_argument("-o", "--out", required=True, help="輸出資料夾（建議 05_輸出/知識庫批次拆分/）")
    ap.add_argument("--paper-id", default="paper-1", help="應用檔綁定的 paper_id（預設 paper-1）")
    ap.add_argument("--vault-prefix", default="", help="knowledge_note 連結的 vault 內前綴")
    ap.add_argument("--pdf-dir", default=None, help="PDF 根目錄（含各主題子夾），用於自動配對內文 PDF 連結")
    args = ap.parse_args()

    if os.path.isdir(args.input):
        files = sorted(os.path.join(args.input, f) for f in os.listdir(args.input)
                       if f.endswith(".md") and "_分析" in f and "綜整" not in f)
    else:
        files = [args.input]
    if not files:
        print("找不到符合的 _分析.md 檔。", file=sys.stderr)
        sys.exit(1)

    index = {}
    review_list = []
    print("共 " + str(len(files)) + " 檔待拆分。\n")
    for p in files:
        try:
            kn, an, nr = process_file(p, args.out, args.paper_id, args.vault_prefix, index, args.pdf_dir)
            flag = "  (needs_review)" if nr else ""
            print("  OK " + os.path.basename(p))
            print("      -> " + kn)
            print("      -> " + an + flag)
            if nr:
                review_list.append(os.path.basename(p))
        except Exception as e:
            print("  FAIL " + os.path.basename(p) + ": " + str(e), file=sys.stderr)
            review_list.append(os.path.basename(p) + "（拆分失敗）")

    idx_path = os.path.join(args.out, "_index.json")
    with open(idx_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print("\n_index.json 初版已生成：" + idx_path + "（" + str(len(index)) + " 條目）")
    if review_list:
        print("\n需使用者審定校正（" + str(len(review_list)) + " 篇）：")
        for r in review_list:
            print("  - " + r)


if __name__ == "__main__":
    main()
