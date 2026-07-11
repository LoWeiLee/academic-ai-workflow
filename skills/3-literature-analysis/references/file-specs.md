# literature-analysis｜檔案規格參考（file-specs）

> 載入時機：產出知識檔／應用檔、或 Mode C 拆分時。SKILL.md 守決策層（Step 0、批次協議、三模式、寫作原則、段落涵蓋規則、完成清單回寫）；本檔提供切分線、雙檔結構與 frontmatter 規格、索引格式、自我檢核模板與 Obsidian 相容性。範本對齊優先於本檔規則窮舉。

---

## 切分線規格（哪些內容歸哪一檔）

| 現行內容 | 歸屬 |
|---|---|
| 銜接摘要前 5 欄（文獻標識／核心主張／理論框架／研究缺口建構方式／方法設計） | 知識檔「核心摘要」 |
| 銜接摘要「警示」之**文獻內在脈絡限制** | 知識檔「通用警示」欄 |
| 銜接摘要「警示」之**特定 paper 引用注意** | 應用檔「本研究警示」欄 |
| 銜接摘要「對當前研究的直接用途」 | 應用檔「應用摘要」 |
| Section 0 導讀 | 知識檔 |
| Section 1 逐節精華 | 知識檔（複用價值主體） |
| Section 2 對當前研究的具體啟發 | 應用檔 |
| Section 3 批判性評估（評價／貢獻／弱點，含文獻內在引用限制） | 知識檔 |
| Section 3 之**特定章節引用操作建議** | 應用檔 Section 2 |

> 判別法：問「換一篇論文，這段話還成立嗎？」——成立 → 知識檔；只對當前 paper 成立（含章節編號） → 應用檔。

---

## 知識檔規格（literature-knowledge）

### 結構順序

1. YAML frontmatter
2. `# [主題]_[作者年份]_[關鍵詞]_知識`
3. 原文 PDF 連結：標題下一行置 `> 📎 原文 PDF：[[主題_作者年份_關鍵詞.pdf]]`（Obsidian basename wikilink，folder-independent，供在 vault 內一鍵點開 PDF）。**PDF 晉升進 vault 時一律改名為與知識檔同前綴的 `[主題]_[作者年份]_[關鍵詞].pdf`**，連結即用此正規檔名，與資料夾位置無關。
4. 範本對齊確認（對齊知識檔範本）
5. **核心摘要**（六欄：文獻標識／核心主張／理論框架／研究缺口建構方式／方法設計／通用警示）
6. Section 0 導讀
7. Section 1 逐節精華
8. Section 3 批判性評估（含內在引用限制）
9. 自我檢核回報（知識檔 8 項，見下）

### 核心摘要格式硬規則

- **禁止使用 Markdown 表格**。以「**欄位名：** 內容」的 key-value 格式，欄位名以粗體 + 全形冒號區隔。
- **六欄名稱不得新增、刪除、合併、改名**：文獻標識／核心主張／理論框架／研究缺口建構方式／方法設計／通用警示。
- 「通用警示」欄收錄文獻內在限制（理論假設、概念性質、作者自承缺口、譯名爭議等跨論文皆成立的注意事項）。**不含**任何特定論文的章節編號或引用動作。

### Section 0（導讀）

> **全文最重要的節。** 讓從未讀過這篇文章的人看完後，清楚知道作者為什麼寫、做了什麼、想說什麼。
> **格式**：2–4 段連貫敘述，**禁止條列**。邏輯串連：發現什麼問題 → 既有文獻什麼缺口 → 用什麼方法 → 得到什麼發現與結論 → 對領域的意義。

### Section 1（逐節精華）

> **本技能的核心複用產出。** 預設按原文實際章節標題生成，不套「緒論/文獻/方法/結果/結論」模板。非標準結構（理論框架／純概念／文獻回顧型論文）在本節開頭說明文章類型與分段依據後依識別結構生成。
> 遵守 SKILL「段落涵蓋規則四條」與「格式禁用清單」。每節格式：`### [章節編號與原文標題]（pp. X–X）` + 定位句 + 逐段關鍵意思（含頁碼）。

### Section 3（批判性評估）

> 先一段整體評價，再以連貫段落說明核心貢獻、明顯弱點、**文獻內在的引用限制**（這篇文獻不適合支撐哪類主張，例如純概念論文不提供測量指標、不能用來宣稱經測量的差異）。**禁止 `####` 小節切分。**
> 注意：舊版「引用注意事項」中關於「特定章節適合/不適合引用」的操作建議，移至應用檔 Section 2，**不寫在知識檔**。

### 知識檔 frontmatter

```yaml
---
citation_key: chen2020topic
title: "An Example Framework for Understanding <Topic A>"
authors:
  - Chen, A.
  - Lee, B.
  - Wang, C.
year: 2020
venue: Example Journal of Policy Studies
doi: "10.0000/example.2020.0001"
type_of_work: article
type: literature-knowledge
topic: ＜主題A＞
analyzed_date: 2026-06-XX
analyzed_by_skill_version: literature-analysis-v1.0.0
pdf_path: "＜主題A＞_Chen2020_TopicFramework.pdf"
zotero_select: "zotero://select/library/items/@chen2020topic"
tags:
  - 文獻/＜主題A＞
aliases:
  - "Chen, Lee & Wang (2020)"
  - "@chen2020topic"
---
```

> frontmatter 設計：相對舊版單檔架構**刪除** `paper_id`、`skill_stage`、`paper/[paper_id]` tag（應用狀態改由 Obsidian backlink 自然呈現）。`type` 為 `literature-knowledge`。

### 知識檔命名

`[主題]_[作者年份]_[關鍵詞]_知識.md`
範例：`＜主題A＞_Chen2020_TopicFramework_知識.md`

---

## 應用檔規格（literature-application）

### 結構順序

1. YAML frontmatter
2. `# [主題]_[作者年份]_[關鍵詞]_應用_[paper-id]`
3. 脈絡對齊確認（已讀 paper-structure.md）
4. 對應知識檔連結：`> 🔗 對應知識檔：[[主題_作者年份_關鍵詞_知識]]`（Obsidian basename wikilink）。**這行驅動 Obsidian backlink，讓知識檔能反向顯示「哪些 paper 用過此文獻」；只靠 frontmatter 的 knowledge_note 字串不會生 backlink。**
5. **應用摘要**（兩欄：對當前研究的直接用途／本研究警示）
6. Section 2 對當前研究的具體啟發（含特定章節引用操作建議）
7. 自我檢核回報（應用檔 4 項，見下）

### 應用摘要格式硬規則

- 「對當前研究的直接用途」欄必須以**編號列表呈現 3–5 條**，每條必須包含 `paper-structure.md` 中的具體章節編號（例如「第2.3節」、「第4.4節」），格式為：
  > （1）第X.X節[章節名]：[3–5 句應用說明，含引用論點、論證位置、所需轉譯]；（2）……
- 「本研究警示」欄收錄綁定當前 paper 的引用注意（部分引用須交代、譯名須在某節選定、某節須正視某侷限等含章節編號的提醒）。

### Section 2（對當前研究的具體啟發）

> 根據 `research-identity.md` 與 `paper-structure.md` 動態生成。三段：(1) 這篇文獻在當前論文中的定位；(2) 具體應用建議（**以章節編號為小節標題**，逐點說明可用在哪裡／如何轉譯／需要注意什麼）；(3) 需要搭配的文獻。**禁止泛用描述**，每個啟發都對應到具體章節。

### 應用檔 frontmatter

```yaml
---
citation_key: chen2020topic
type: literature-application
paper_id: ＜你的論文＞
knowledge_note: "＜主題A＞_Chen2020_TopicFramework_知識.md"
applied_date: 2026-06-XX
analyzed_by_skill_version: literature-analysis-v1.0.0
tags:
  - paper/＜你的論文＞
  - 文獻/＜主題A＞
---
```

> 同一篇文獻可有多份應用檔（每 paper 一份）。`knowledge_note` 連結使 Obsidian graph 自動呈現「哪些 paper 用過此文獻」。

### 應用檔命名

`[主題]_[作者年份]_[關鍵詞]_應用_[paper-id].md`
範例：`＜主題A＞_Chen2020_TopicFramework_應用_＜你的論文＞.md`

---

## 知識庫索引（_index.json）

位置：`3_文獻/_index.json`（vault 根目錄＝使用者本機文獻庫資料夾，例如 `~/Documents/研究/3_文獻`，實際路徑由使用者自訂；知識檔存於分類樹 `理論基礎/[主題]/`，索引正本僅此一份）

```json
{
  "chen2020topic": {
    "topic": "＜主題A＞",
    "file": "理論基礎/＜主題A＞/＜主題A＞_Chen2020_TopicFramework_知識.md",
    "analyzed_date": "2026-06-XX",
    "skill_version": "v1.0.0",
    "applications": ["＜你的論文＞"]
  }
}
```

**維護規則**：
- Mode A 產出知識檔時，於 `05_輸出/` 附帶 `_index_更新.json` 片段，使用者移檔入 vault 時合併至正本索引。
- Mode B 產出應用檔時，更新片段中追加該 citation_key 的 `applications` 條目。

---

## 自我檢核回報（兩檔合計 12 項）

> 各檔在結尾署名之前附上對應檢核，逐項標示「✓ 已執行」或「✗ 未執行，原因：……」。檢核回報為產出的一部分，缺漏視為未完成。

**知識檔（8 項）**：

```markdown
## 自我檢核回報（知識檔）
- [ ] 範本對齊確認已置於開頭：
- [ ] frontmatter 完整且 citation_key 與索引／metadata 一致：
- [ ] 核心摘要六欄完整（文獻標識／核心主張／理論框架／研究缺口建構方式／方法設計／通用警示）：
- [ ] Section 0 為 2–4 段連貫敘述、無條列：
- [ ] 逐節精華每節有定位句、節層級無遺漏：
- [ ] 三類內容（核心定義／確立論點／因果機制）均附英文引句含頁碼：
- [ ] 無表格呈現概念內容、無 #### 深層切分：
- [ ] 所有引句／頁碼／數據均出自本次載入素材；〔記憶未驗證〕項未寫入正文、已彙列於完成通知：
```

**應用檔（4 項）**：

```markdown
## 自我檢核回報（應用檔）
- [ ] 應用摘要「直接用途」為 3–5 條編號列表且每條含章節編號：
- [ ] Section 2 每項啟發對應具體章節，引句與頁碼與知識檔記載一致：
- [ ] 內文含 `> 🔗 對應知識檔：[[..._知識]]` wikilink（驅動 Obsidian backlink）：
- [ ] 輸出路徑為 05_輸出，frontmatter 的 knowledge_note 連結正確：
```

> 相對舊版已刪除項：`skill_stage` 欄位與「下游 Skills 逐步更新」承諾；舊版檢核中與範本對齊重複、模型無法真實驗證的項目（含段數核對配額）。

---

## Obsidian 相容性

每份 `.md` 最前端的 YAML frontmatter 使檔案同時滿足三端：
- **Cowork 端**：literature-synthesis 解析 metadata 自動建立文獻清單
- **Obsidian 端**：貼入 vault 後 graph view、tag、Dataview、backlink 皆可運作
- **Zotero 端**：citation_key 作為橋梁，從 Obsidian 連回 Zotero 條目

欄位生成規則重點：`authors` 必為 YAML array；`doi` 允許空字串但不可省欄位；`tags` 採階層式（`/` 分隔）；`aliases` 至少含 APA 內引格式與 `@citation_key`。應用狀態不再寫入 frontmatter（由 backlink 呈現），`knowledge_note` 為應用檔連回知識檔的唯一連結欄位。注意：frontmatter 的 `pdf_path` 僅為 metadata，Obsidian 不會自動變成可點連結；要在筆記內一鍵開 PDF，靠的是標題下那行 `[[檔名.pdf]]` 內文 wikilink（PDF 與知識檔同在 `3_文獻` vault 內即可解析）。
