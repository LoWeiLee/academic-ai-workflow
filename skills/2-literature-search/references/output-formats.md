# output-formats.md — literature-search 階段六輸出檔案格式

> 階段六（輸出）時載入。承載五個輸出物的完整格式：search_log.md、zotero_import_dois.txt、pending_zotero_transfer.md、_metadata.json、_index.json。
> 檔案寫入：一律 Write tool 完整寫檔（不用 bash heredoc/echo）；JSON 大檔分段寫；寫後驗證檔尾完整。

---

## `search_log.md`

```markdown
# 文獻搜尋日誌｜{topic}

- 時間：YYYY-MM-DD HH:MM（ISO 8601）
- 聚焦節次：{paper-structure 節號與標題}
- 參數：年代 ≥ XXXX；候選池上限 XXX；語言 XXX
- Skill 版本：[現行版，見 SKILL.md 檔尾版本區]
- rubric prompt 版本：[rubric-prompt.md 檔頭版本]
- API 版本：OpenAlex (stable) / S2 graph/v1
- 使用者：[使用者姓名/代稱]

---

## Part A｜原始查詢紀錄

### A.1 種子輪 API 呼叫清單
| # | 時間戳 | 端點 | 完整 URL | 回傳筆數 | HTTP 狀態 |

### A.2 關鍵字輪 API 呼叫清單
| # | 時間戳 | 關鍵字組（boolean 字串）| 完整 URL | total | 回傳筆數 | HTTP 狀態 |

### A.3 降級事件
| 時間戳 | 原端點 | 降級至 | 原因 |

---

## Part B｜決策歷程

### B.1 種子提名（Claude 原始輸出）
| # | Claude 提名作者年代 | 提名標題 | 提名 DOI | 提名理由 |

### B.2 DOI 驗證結果
| # | 原提名 DOI | 驗證結果 | 替換 DOI（若有）| 替換方式 |

### B.3 使用者確認後的最終種子清單
| # | 最終 DOI | 來源 | 使用者動作 |

### B.4 關鍵字組設計與試搜決策歷程

#### B.4.1 雙層概念抽取
- Focal: ...
- Domain: ...
- 結構：focal × domain（或其他層數）

#### B.4.2 Claude 建議關鍵字組（Step 1b）
| 組 | 查詢字串 | 子群分類 | Claude 選用理由 |

#### B.4.3 使用者於 Step 1c 的選擇
- 選擇：(a)/(b)/(c)/(d)
- 若 (b)/(c)：使用者調整內容
- 最終確認的查詢字串：...

#### B.4.4 試搜決策（每組 Step 3）
| 組 | 查詢字串 | total | 使用者選擇 (a/b/c/d) | 備註 |

### B.5 Pending 桶使用者裁決摘要
| DOI | Claude 建議 | 使用者決定 | 偏離 Claude 建議？ |

---

## Part C｜統計摘要

### C.1 候選池構成
- 種子衍生池：X 篇 / 關鍵字衍生池：X 篇 / 合併去重後候選池：X 篇
- 軟上限檢查點（>400 時）：是否觸發＝是/否；處置＝收緊標準重跑｜確認全量評分。候選池不在評分前截斷，無靜默溢出

### C.2 Rubric 分桶統計
- 納入（自動）：X / 排除（自動）：X / Pending：X（特殊保留 X / 分數競爭 X）/ Pending 溢出：X / 使用者裁決：納入 X、暫存 X、排除 X

### C.3 rubricBasis 分佈
- title+abstract+tldr：X / title+abstract：X / title_only：X

### C.4 使用者決定 vs Claude 建議一致率
- Pending 裁決一致率：X%

### C.5 關鍵字組設計協作度
- Claude 建議組數：X / 使用者最終採用組數：X / 使用者調整類型：(a/b/c/d)

---

## Part D｜本次搜尋回顧（使用者自填）
- rubric 閾值是否合理？候選池是否夠？關鍵字組設計是否實用？同義詞分類是否到位？
- Pending 上限 50 是否太緊/太鬆？Rubric anchor examples 是否實用？其他觀察：

---

## Part E｜下一步操作
1. 機構 VPN 連線（校外存取付費全文時才需要；校內網路或開放取用文獻可略過）
2. Zotero Add by Identifier
3. 匯出 PDF 至 `01_文獻/{topic}/`（搜尋暫存區，不另設 pdfs 子層）
4. 將 PDF 比照知識檔晉升流程移入自己慣用的文獻管理 vault（例如 Obsidian 中自訂的文獻資料夾），並於 pending_zotero_transfer.md 勾選「PDF 已晉升至 vault」
5. 啟動 literature-analysis（從 vault 讀取 PDF）
```

---

## `zotero_import_dois.txt`

```
# literature-search [現行版] 輸出
# Topic: {topic}
# 產出時間: YYYY-MM-DD HH:MM:SS

# === 納入桶（include）=== 23 篇
10.1080/14719037.2016.1148191
...

# === 暫存桶（shelf）=== 12 篇
10.1080/01900692.2018.1498105
...
```

排除桶不寫入 DOI 清單，僅列入 search_log.md 備查。

---

## `pending_zotero_transfer.md`

```markdown
# Zotero 處理追蹤｜{topic}

| DOI | 標題 | 年 | 分桶 | Zotero 已匯入 | PDF 取得 | PDF 已晉升至 vault |
|---|---|---|---|---|---|---|

## 異常處理（使用者自填）
```

> 下游 literature-analysis 以本檔「PDF 已晉升至 vault」欄判定哪些納入桶文獻 PDF 已進入使用者的文獻管理 vault、可進入分析。

---

## `_metadata.json`

**範圍**：僅寫入最終為 `include`、`shelf`、或曾經進入 `pending` 的條目。自動排除（auto-exclude）與溢出條目不寫入。

**頂層容器**：JSON 陣列（array），每個元素為一筆條目物件；下游（literature-analysis）以 `finalBucket == "include"` 過濾。

**每筆結構**：

```json
{
  "paperId": "s2-abc123",
  "openAlexId": "W4XXXXXXX",
  "doi": "10.1111/puar.13456",
  "title": "...",
  "authors": ["..."],
  "year": 2023,
  "venue": "Public Administration Review",
  "citationCount": 87,
  "tldr": "...",
  "abstract": "...",

  "rubricScores": {"relevance": 3, "theory": 3, "method": 2, "quality": 3},
  "rubricBasis": "title+abstract",
  "rubricReasoning": {"relevance": "...", "theory": "...", "method": "...", "quality": "..."},

  "finalBucket": "include",
  "claudeSuggestion": "include",
  "claudeConfidence": "high",

  "source": "seed:example2008:fwd | keyword:example-topic-group2",
  "pendingSubLayer": null,

  "provenance": {
    "apiSource": "openalex",
    "apiVersion": "stable",
    "queryTimestamp": "2026-04-24T09:15:23Z",
    "searchQuery": "https://api.openalex.org/works?filter=title_and_abstract.search:%22your+topic%22...",
    "rankInfo": "17"
  }
}
```

**欄位值**：
- `apiSource`：openalex / semantic_scholar / manual
- `rubricBasis`：title_only / title+abstract / title+abstract+tldr
- `finalBucket`：include / shelf / exclude（排除需曾經進 pending 才寫入）
- `pendingSubLayer`：special_hold / score_competition / null
- `rankInfo`：目前腳本輸出單一排位數字（例 `"17"`＝該來源清單第 17 位）；「原始→重排」雙位格式為未實作的規格遺留，勿據此期待
- `source` 的 keyword 標記為 `keyword:{group_id}`，對應 search_log Part B.4.2 的組編號

---

## `_index.json`

```json
{
  "10.1111/puar.13456": [
    {"paper": "Paper A", "topic": "主題X", "timestamp": "2026-05-01", "bucket": "include"}
  ]
}
```
