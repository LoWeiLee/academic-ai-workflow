---
name: literature-search
description: "文獻搜尋自動化技能。當使用者啟動某論文某節的文獻蒐集任務、需要從 OpenAlex 與 Semantic Scholar API 自動產生候選文獻池、並分桶決定哪些納入文獻庫時，必須使用此技能。觸發情境以「找/建文獻池」類動詞為主：「幫我找＜主題A＞的文獻」「開始搜＜你的論文＞＜主題B＞這節」「這個主題我要建文獻池」「種子論文跑一下」「幫第 2.3 節補建文獻池」。此技能以 paper-structure.md 為判讀錨，產出結構化 DOI 清單（納入／暫存分區）；PDF 取得由使用者在本機 Zotero 以 Add by Identifier 完成。界定：本技能只「找/建文獻池」；不負責單篇深度分析（literature-analysis 職責）、不負責跨文件綜整（literature-synthesis 職責）、不負責章節正文撰寫（chapter-drafting 職責；「補/寫第 X 節正文」非本技能）、不負責 PDF 自動下載（Cowork 沙盒限制）。"
---

# 文獻搜尋自動化技能 v1.0.1

> **結構**：SKILL.md 保留工作流決策層（「何時做什麼決策」），技術細節下放至腳本與參考檔。
> - 技術實作 → `scripts/`：`doi_verify.py`（DOI 驗證）、`citation_expand.py`（雙向引用擴展、abstract 還原、rate limit、降級）、`keyword_search.py`（boolean 構造、URL encoding、試搜/正式搜、timeout 降級鏈）
> - 細節規格 → `references/`：`rubric-prompt.md`（rubric 四維度 + anchor + prompt，階段三載入）、`widget-spec.md`（pending widget，階段四載入）、`output-formats.md`（五個輸出物格式，階段六載入）
> - 寫入策略 → 一律 Write tool 完整寫檔（禁 bash heredoc／echo）；JSON 大檔分段；中間結果寫 /tmp
> **不變項**：六階段工作流邏輯、分桶閾值、Human-in-the-loop 決策點、search_log 的 Part A–E 結構、與 literature-analysis 的介面合約。

## 核心原則

1. **API-grounded**：所有候選文獻來自真實 API 回傳，不得用訓練記憶生成
2. **Human-in-the-loop**：種子確認、關鍵字驗證、Pending 裁決由使用者決策
3. **Auditable**：所有 API 呼叫、rubric 打分、分桶依據完整記錄於 search_log
4. **Claude 限於資訊呈現與執行**：決策權盡量歸屬使用者

---

## 階段零｜執行前準備

### 必讀脈絡檔案

啟動時強制讀取：
- `00_專案控制/paper-structure.md`：研究問題、理論框架、方法論類型、目標期刊、經典文獻白名單 DOI、本次聚焦節次
- `00_專案控制/about-me.md`、`research-identity.md`：使用者脈絡（若你的環境已透過 `CLAUDE.md` 自動載入可略）

缺失檢查：若 `paper-structure.md` 不存在或無核心研究問題段落，**中斷**並依序提示：
1. **先檢查 `05_輸出/` 是否已有 `paper-structure_*` 版本**——若有，代表 research-design-diagnosis 已跑過但尚未正本化，請使用者確認內容後**改名為 `paper-structure.md` 搬入 `00_專案控制/`**，再重新啟動本 skill。
2. 若 `05_輸出/` 也沒有，提示先用 research-design-diagnosis 建構（或手寫一份至少含研究問題與理論框架的簡化版）。

### 讀寫規則

- 讀取來源（唯讀）：`00_專案控制/`
- 寫入：`search_log.md`、`zotero_import_dois.txt`、`pending_zotero_transfer.md`、`_metadata.json` → `05_輸出/文獻搜尋/{topic}/`；`_index.json` → `05_輸出/文獻搜尋/`
- 寫入技術：Write tool 完整寫檔（禁 bash heredoc／echo）；JSON 大檔分段；中間結果寫 /tmp

### 工作流盲點提示（啟動時主動告知，非中斷）

```
本工作流以 OpenAlex 為主（免費、覆蓋廣），S2 僅在 OpenAlex 端點失敗時備援。
已知盲點：中文/在地期刊覆蓋有限、灰色文獻（政府報告、智庫白皮書）不在索引、
書籍章節覆蓋不全、部分出版商 references 受 CrossRef 遮蔽、
關鍵字輪每組僅取被引前 50（無翻頁）——近年低被引文獻可能漏，靠種子輪 forward 與手動補 DOI 補強。
補強：你若已知某主題的關鍵論文，可在種子確認（階段一 Step 3）或關鍵字確認
（階段二 Step 1c）直接指定 DOI 納入——這是補強單一資料庫盲點最重要的機會。
中文文獻、政府報告請事後手動納入文獻庫。
```

### 參數確認（五項，使用者可「用預設」快速啟動）

1. topic 名稱（決定輸出子資料夾名）
2. 年代下限（預設 2016）
3. 候選池軟上限（預設 400；達上限不靜默截斷，改觸發使用者檢查點，見階段三）。人工裁決負荷改由 Pending 上限 50 控制，與候選池規模脫鉤
4. 語言範圍（預設英文為主 + 繁中補充）
5. 聚焦節次（paper-structure 的哪一節）

---

## 六階段工作流（決策規則層級）

> **序列強制**：種子輪（階段一）必須先於關鍵字輪（階段二）。
> **階段轉換重申**（防長流程遺忘）：每進入下一階段前，先重申本支三條鐵律——① **API-grounded**：候選只能來自真實 API 回傳，禁用訓練記憶生成；② **Human-in-the-loop**：種子確認、關鍵字驗證、Pending 裁決一律由使用者決策，不代為拍板；③ **序列強制**：種子輪先於關鍵字輪。

### 階段一｜種子輪

**Step 1 種子提名**：

**1a 讀取白名單**：先讀 paper-structure.md 的「經典文獻白名單（DOI）」欄位。
- 若有條目：將全部白名單文獻納入種子清單，標記 `來源：whitelist`，不計入 3–5 篇提名上限；白名單 >8 顆時主動提示擴展成本（每顆雙向約 40 篇候選）並請使用者確認全跑或先挑重點
- 標記「⚠️ DOI 待驗證」者：保留進入 Step 2 驗證，不先排除

**1b Claude 補提名**：基於 RQ 與理論框架，從訓練記憶**額外**提名 3–5 篇白名單未涵蓋的候選種子（優先近 5 年、被引 > 100、與 RQ 直接共振；避免太新或太泛；跨子領域至少納入 2 個主流傳統；每篇說明提名理由）。標記 `來源：Claude 提名`。

原始提名清單（白名單條目 + Claude 提名，含可能錯誤的 DOI）完整寫入 `search_log.md` Part B.1，並標注各條目來源。

**Step 2 DOI 強制驗證**：Claude 記憶中的 DOI 不可信。執行 `scripts/doi_verify.py` 對每篇提名驗證（OpenAlex by DOI → 標題模糊匹配 → 標題重搜替換 → S2 備援）。結果寫入 Part B.2。
- 決策規則：DOI 不匹配 → 標題重搜，找到則替換；404 或重搜失敗 → 標記「未驗證」請使用者確認或移除。

**Step 3 使用者確認**：呈現已驗證種子清單（含白名單來源與 Claude 提名來源標記）。使用者可 接受 / 替換 / 新增 / 進一步驗證。**每次必說的主動提示**：

```
白名單文獻（來自 paper-structure.md）與 Claude 提名文獻已整合為這份種子清單。
若你心中還有特定關鍵論文（領域奠基文獻、近期讀到的、導師/同儕推薦的）沒被列入，
現在是加入的時機——這些「你知道但清單裡沒有」的論文是覆蓋盲點最重要的補強來源。
請給 DOI 或作者+年代+標題。
```

最終清單寫入 Part B.3。

**Step 4 雙向引用網絡擴展**：執行 `scripts/citation_expand.py`，對每顆種子做 Forward（cites，取前 20）+ Backward（referenced_works，按被引降序取前 20）。OpenAlex 失敗自動降級 S2（腳本內建）。降級事件記錄 Part A.3。腳本輸出含 `env_block_suspected: true` 時，比照階段二 Step 2 規則轉手動匯出模式。每篇捕獲論文在 `_metadata.json` 記錄 provenance。

**Step 5 合併去重**：所有種子的雙向擴展合併去重 → 種子衍生池（預期 80-160 篇）。去重以 DOI 為主鍵、OpenAlex ID 為副鍵，重複條目合併 `source`。

### 階段二｜關鍵字輪

**Step 1 協作式關鍵字組設計**（Human-in-the-loop 的核心決策點）：
- **1a Claude 抽取雙層概念**：讀 RQ 與聚焦節次，抽 Focal concept（核心理論/概念，RQ 主詞）× Domain context（應用領域，RQ 修飾語）。Focal 含 ≤ 4 字元縮寫時主動展開為「縮寫 OR 全稱 OR 變體」（如 TPB → `"TPB" OR "Theory of Planned Behavior"`）。雙層為預設起點，非強制（可三層 focal×method×domain 等）。
- **1b Claude 建議關鍵字組**（**上限 4 組正式搜**，超過主動提示收斂）：依 OpenAlex boolean 語法（AND/OR/NOT 大寫、雙引號鎖片語、括號控序、同類同義詞 OR 合併、跨類 AND 串接）。Domain 同義詞依**學術傳統/子領域分類呈現**讓使用者易判斷。寫入 Part B.4.1/B.4.2。
- **1c 使用者確認**：選 (a) 合理進試搜 / (b) 調整 / (c) 自帶關鍵字組 / (d) 改變概念結構。**確認前必說的主動提示**：已知關鍵論文可直接給 DOI 跳過關鍵字搜尋納入候選池。寫入 Part B.4.3。

**Step 2 試搜**：通過的每組執行 `scripts/keyword_search.py --mode trial`（per_page=10）。Claude **只呈現 API 客觀結果**（總命中數 + top 10 表），不主動判斷通過與否。若腳本輸出含 `env_block_suspected: true` 或 degraded 原因含 403，**不得將 total=0 當作「零命中」呈現**——立即宣告環境阻擋、轉手動匯出模式（見錯誤處理表）。

**Step 3 使用者判斷**：每組選 (a) 通過進正式搜 / (b) 調整關鍵字 / (c) 放棄此組 / (d) 手動補 DOI。寫入 Part B.4.4。

**Step 4 正式搜**：通過試搜的組執行 `keyword_search.py --mode full`（per_page=50）。

**Step 5 合併**：所有關鍵字結果合併去重 → 關鍵字衍生池。

### 階段三｜判讀分桶

**候選池合併**：`候選池 = 種子衍生池 ∪ 關鍵字衍生池`。
- **不再於評分前硬性截前 200**：所有候選一律進入下方 rubric 語義判讀，由分桶閾值（尤其自動排除 relevance=0 或總分≤3）依標準篩除。最終截斷量是標準的產物，不是預設數字。此舉修補「候選池在評分前被靜默截斷」這個召回漏點（殘餘漏點見工作流盲點提示）。
- **軟上限檢查點（成本護欄，非靜默丟棄）**：候選池 > 400 時中斷，向使用者報告（總篇數 + relevance 分數分佈），由使用者擇一：(a) 收緊標準後重跑（縮關鍵字組／上修年代下限／聚焦更窄），(b) 確認全量評分（token 成本較高）。處置記於 Part C，溢出不再靜默發生。

**LLM 語義判讀**：載入 `references/rubric-prompt.md`，對每篇讀 title+abstract（+tldr）套 rubric 四維度（relevance/theory/method/quality，各 0-3）給分 + 理由 + rubricBasis。每批 10 篇，中間結果寫 /tmp。**禁止關鍵字匹配當判讀**。

**分桶閾值規則**（核心，留在本檔）：

| 條件 | 落桶 |
|---|---|
| 總分 ≥ 9 且 relevance = 3 | 納入（自動）|
| relevance = 0 或 總分 ≤ 3 | 排除（自動）|
| 其他 | Pending（使用者裁決）|

- **title_only 保守化**：rubricBasis == title_only 時，排除閾值由 ≤ 3 上修為 ≤ 5
- **Pending 附加欄位**：claudeSuggestion（include/shelf/exclude）+ claudeConfidence（high/low）。總分 6-8 且 relevance ≥ 2 → shelf/high；任一維度接近閾值、venue 弱、年代邊緣 → low
- **特殊處理**：預印本 → pending（include/low）；經典白名單（paper-structure 指定 DOI）→ 跳過 rubric 直接納入；年代老於下限的高被引（>500 且 relevance≥2）→ pending 特殊保留層 ★
- **Pending 上限 50**：超過採兩層——特殊保留層（★，上限 10：高被引老論文、白名單未自動納入者、預印本、年代老但相關性高）+ 分數競爭層（按總分降序前 40）。溢出記「pending 溢出 X 篇」於 Part C

### 階段四｜使用者決策

**必須用互動式 widget**（非 markdown 表格），規格載入 `references/widget-spec.md`；環境不支援 widget 時走錯誤處理表的編號清單降級條目。呈現前說明 ★ 意義與「信心低→高」排序。使用者裁決寫入 Part B.5，計算 Part C.4 一致率。

### 階段五｜DOI 清單產出

對納入桶 + 使用者升級至暫存的 pending，產出 `zotero_import_dois.txt`（納入/暫存分區）。排除桶不寫 DOI 清單。使用者接續步驟（VPN → Zotero Add by Identifier → Export PDF → 更新 pending_zotero_transfer.md → 啟動 literature-analysis）寫入 Part E。

### 階段六｜輸出

產出四檔 + 更新 `_index.json`。格式載入 `references/output-formats.md`。

---

## PRISMA 式透明紀律（選用，內部用途）

為控制文獻擴張並使流程可稽核，search_log 可額外產出一張流程計數：識別 → 去重 → 進入評分 → 自動排除（含理由）→ Pending → 最終納入，數字直接取自既有分桶結果，不需另算。納入與排除標準應錨定 paper-structure.md，在搜尋前即固定，而非每次臨時決定。

注意（學術倫理）：此為敘事型理論回顧的內部透明工具，不得在論文中宣稱為 PRISMA 系統性回顧。僅當該篇確為系統性或範疇回顧時，才正式套用 PRISMA 並輸出標準流程圖。

---

## 介面合約（與其他 Skills）

### 啟動條件
從 paper-structure.md 的「此章可啟動的 Skills」欄位觸發（research-design-diagnosis 在第 2 章某節達小節層級時標記）。

### 下游：literature-analysis（逐篇分析）

**PDF 流向（與 literature-analysis vault 佈局對齊）**：本 skill 產出的納入桶 DOI，由使用者以 Zotero 下載 PDF 後**先暫存於專案 `01_文獻/{topic}/`**（不另設 pdfs 子層；僅納入桶）。使用者再比照知識檔晉升流程，將 PDF 移入自己慣用的文獻管理 vault（例如 Obsidian 中自訂的文獻資料夾）。**literature-analysis 從該 vault 讀取 PDF，不直接讀 `01_文獻/{topic}/`**。`01_文獻/{topic}/` 僅為晉升前的搜尋暫存區。

literature-analysis 啟動時另跨資料夾讀取（仍在 Cowork 專案內）：
- `05_輸出/文獻搜尋/{topic}/_metadata.json`（過濾 `finalBucket == "include"`）
- `05_輸出/文獻搜尋/{topic}/pending_zotero_transfer.md`（檢查「PDF 已晉升至 vault」欄）

literature-analysis 第 0 步必須掃 `pending_zotero_transfer.md` 確認 PDF 已晉升至 vault；某納入桶條目 PDF 未晉升則告知「本次略過 X 篇」。

> **與 literature-analysis 的用語對齊**：下游產出區分「應用檔」（逐篇分析檔）與「知識檔」（供 synthesis 調用的知識節點檔），並回寫 paper-structure.md「文獻分析完成清單」（欄位定義見 research-design-diagnosis `references/paper-structure-template.md` 完成清單表，該檔為此欄位定義的單一權威來源）。

---

## 精簡錯誤處理

| 場景 | 處理 |
|---|---|
| paper-structure.md 缺失 | 中斷，提示先用 research-design-diagnosis |
| 種子 DOI 404 / 標題不匹配 | doi_verify.py 標題重搜；失敗則移除或標「未驗證」請使用者確認 |
| OpenAlex cites / referenced_works 失敗 | citation_expand.py 自動降級 S2（429 指數退避 2→30s，最多 5 次） |
| OpenAlex／S2／CrossRef 被環境 allowlist 阻擋（tunnel 403 Forbidden，非 API 回傳）| 自動化搜尋不可用——若執行環境的網路白名單未放行這些網域，屬環境設定，AI 不可改。**降級為手動匯出模式**：使用者於可連外環境跑 scripts/ 或用 OpenAlex／Zotero 網頁介面搜尋，匯出 DOI 貼回 zotero_import_dois.txt 續走階段五、六。**手動模式合約**：貼回 DOI 未經 rubric 評分，一律以 `finalBucket="include"` 寫入最小 `_metadata.json`（doi＋finalBucket＋`apiSource:"manual"`＋`rubricBasis:"none"`），使下游 literature-analysis 的 include 過濾不落空；pending_zotero_transfer 的標題/年欄由使用者匯出資料或 Zotero 條目補填；search_log 註記「手動模式：無 rubric 評分」。當下明示「API 未連通、本次手動匯出」，**不得以訓練記憶偽造候選池** |
| 關鍵字 boolean 語法錯誤 | keyword_search.py 自動修正（大寫、引號平衡）；連續錯誤中斷請使用者確認 |
| 含 ≥ 2 雙引號短語 timeout | keyword_search.py 降級 title.search → 拆單短語合併 |
| 關鍵字組超過 4 組 | 主動提示收斂，請使用者選優先序 |
| 候選池 > 400（軟上限）| 中斷觸發使用者檢查點，二擇一（收緊標準重跑／確認全量評分），記 Part C，不靜默截斷 |
| Pending > 50 | 依兩層規則控管（★ 保留層 10 + 分數競爭層 40），溢出記 Part C |
| 寫入目標資料夾不存在 | 自建 `05_輸出/文獻搜尋/{topic}/` |
| _index.json 讀取失敗 | 以空 index 繼續，log 警告 |
| widget 點擊無反應 | 檢查 console、data attributes、event listener（見 widget-spec.md） |
| 環境不支援互動 widget（如 CLI／無渲染介面） | 降級為編號清單＋逐項問答完成裁決（裁決一樣寫入 Part B.5、計 Part C.4 一致率）；自我檢核 widget 項標記「N/A：環境不支援」 |

---

## 自我檢核清單（≤10 項）

格式：`[x] 項目 —— 是/否，簡短說明`。

```
[ ] 已讀 paper-structure.md 並提取 RQ/理論/方法/經典白名單；已確認五參數；已提示覆蓋盲點 —— 是/否
[ ] 種子輪先於關鍵字輪；各階段轉換已重申三鐵律；種子原始提名寫入 Part B.1，驗證寫入 B.2，最終清單寫入 B.3 —— 是/否
[ ] 階段一 Step 3 與階段二 Step 1c 均已主動提示使用者補充已知關鍵論文 DOI —— 是/否
[ ] 種子雙向擴展 forward+backward 皆執行（或正確降級並記 Part A.3）；每篇記 provenance —— 是/否
[ ] 關鍵字組 ≤ 4 組、boolean 語法正確、同義詞依學術傳統分類；試搜僅呈中性觀察由使用者判斷 —— 是/否
[ ] rubric 採 LLM 語義判讀（非關鍵字匹配）；rubricBasis 記錄且 title_only 套上修閾值 —— 是/否
[ ] 候選池未在評分前被靜默截斷（>400 已觸發使用者檢查點）；分桶閾值與 Pending 50 兩層控管正確；★ 特殊保留層判定無誤 —— 是/否
[ ] 階段四用互動 widget（非表格）且互動已驗證（高亮/切換/取消）—— 是/否
[ ] 四輸出檔產出，_metadata 僅含 include+shelf+pending（不含 auto-exclude/溢出），_index 已追加 —— 是/否
[ ] 工作區檔案均用 Write tool（完整寫檔、驗證檔尾）；已提醒 VPN + Zotero Add by Identifier —— 是/否
```

---

## 檔尾簽名

通用欄位：執行 skill 與版本（取檔尾版本區當前版）、執行模式、日期、下一步建議 1–3 條。本 skill 專屬欄位：

```
- 執行 Skill：literature-search [現行版，見檔尾版本區]｜rubric prompt：[rubric-prompt.md 檔頭版本]
- 本次 topic / 聚焦節次：[...]
- 候選池規模：[X 篇；若 >400 軟上限，記檢查點處置]
- 分桶結果：納入 X / 暫存 X / 排除 X
- rubricBasis 分佈：[title_only X / title+abstract X / 完整 X]
- 使用者 vs Claude 一致率：X%（Pending 層級）
- 關鍵字組：Claude 建議 X 組 / 使用者採用 X 組（協作度 a/b/c/d）
- API 狀態：OpenAlex cites / referenced_works / S2 備援 [正常/降級]
- 輸出檔案：search_log / zotero_import_dois / pending_zotero_transfer / _metadata
- 下一步建議（1–3 條）：VPN + Zotero Add by Identifier 貼入 X 篇納入 DOI；處理暫存桶；PDF 匯出後啟動 literature-analysis
```

---

## 版本記錄

設計演變、技術限制、決策依據與測試實證見 repo 根目錄 CHANGELOG。本 SKILL.md 為「當前執行規範」。

---

**版本**：v1.0.1｜紅隊審查修訂
