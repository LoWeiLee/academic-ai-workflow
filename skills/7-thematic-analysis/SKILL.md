---
name: thematic-analysis
description: "質性主題分析技能。當使用者要對一手質性資料（訪談逐字稿、田野筆記、開放式問卷、政策文件）進行主題分析、編碼、建構主題、產出編碼簿或主題地圖時，必須使用此技能。觸發情境包括：「幫我對這批訪談做主題分析」、「這些逐字稿幫我編碼」、「用某理論框架重新編碼」、「建立編碼簿」、「幫我找出主題」、「做 thematic analysis / reflexive TA / 主題分析」、「把訪談資料轉成結果章」。本技能採『一支兩路』：Pre-flight 先定 reflexive TA 或 coding reliability（含 codebook）路線，路內強制知識論一致性、主動攔截兩典範混用（如選 reflexive 卻要報 kappa、選 coding reliability 卻寫 reflexive 知識論語言）。界定：本技能處理**一手質性資料的主題分析**；學術文獻（二手）逐篇分析屬 literature-analysis、跨篇綜整屬 literature-synthesis；把主題結果落筆成結果/討論章正文屬 chapter-drafting；研究設計章結構屬 research-design-diagnosis；審稿/診斷屬 review-diagnosis。即使使用者只說『這些訪談我想開始分析』也應觸發本技能進入 Pre-flight。"
---

> **授權與致謝**：本 skill 係參考 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills)（CC-BY-NC 4.0）改寫，依 CC-BY-NC 4.0 授權發布並署名原作。「一支兩路」（reflexive TA vs coding reliability）之 Pre-flight 設計為本 repo 自有結構。

# 主題分析技能（thematic-analysis）[現行版，見檔尾版本區]

> 本檔守決策層（Pre-flight 分路與守門、共用六階段框架的流程邏輯、引文溯源稽核、路線分岔點、介面合約）。路線專屬的逐階段操作與逐字輸出模板下放 `references/`，於定路與產出時才載入：
> - `references/route-reflexive.md` —— reflexive TA 路線的六階段完整操作、知識論宣告、反身性紀律、為何禁用 ICR（定路為 reflexive 後全程載入）
> - `references/route-coding-reliability.md` —— coding reliability／codebook 路線（骨架版：列齊分岔決策點與信度程序，逐階段操作細節待後續版本補完）
> - `references/phase-templates.md` —— 啟動宣告、編碼簿、主題定義表、主題地圖、引文溯源表、各階段輸出、撰寫交付骨架（產出階段載入）
>
> 變更歷程見 repo CHANGELOG，本檔不嵌補丁說明。

---

## 核心定位

對**一手質性資料**（訪談逐字稿、田野筆記、開放式問卷回應、政策／檔案文件）進行系統化主題分析，產出可溯源的編碼簿、主題定義、主題地圖，並交付 chapter-drafting 作為結果／討論章的素材。

與現有六支的根本差異：本技能吃的是**一手資料**（其餘六支吃文獻與二手綜整），因此上接 `02_資料與證據/` 的去識別化逐字稿，下接 chapter-drafting。

**一支兩路**的設計理由：主題分析存在兩個哲學上不相容的典範——reflexive TA（編碼者主觀性是分析資源，Big-Q 質性）與 coding reliability TA（編碼者間信度確保客觀，後實證／pragmatic）。兩者皆未被學界揚棄、各有適用領域，但最大的方法論錯誤是**混用**（如做 reflexive TA 卻補一個 kappa「證明嚴謹」）。故本技能在入口開放選路，在路內強制內部一致性，並設一致性守門攔截混用。

---

## Pre-flight（任何分析動作之前，無例外）

### 必讀
| 檔案 | 用途 | 缺漏處置 |
|------|------|---------|
| `00_專案控制/research-identity.md` | 研究者的方法論立場、理論偏好 | 回報請補齊 |
| `00_專案控制/paper-structure.md`（在特定論文專案時） | 研究問題、理論框架（deductive／theoretical 編碼的框架來源，如你的論文的理論框架 X／Y）、章節結構 | 非論文專案可略，但須回報「無 paper-structure，編碼框架改由使用者當場界定」 |
| `00_專案控制/writing-standards.md` | 撰寫交付時的學術中文語氣、禁止清單、引用格式 | 回報請補齊 |
| 對應 Paper 的 `folder-instructions.md`（選配） | 專案專屬協作原則與品質閘門（含**訪談資料安全**閘門） | 該檔不存在＝此專案無專屬閘門，僅以 `00_專案控制/` 四份控制檔為準（此為常態，不需提示為缺失）。惟本 skill 的去識別化硬閘門為內建條文，不因此放寬 |

### 必確認（逐項確認，已在指令說明者直接帶過）

1. **路線**：reflexive TA／coding reliability（含 codebook）。選擇輔助見下節「路線選擇」。
2. **知識論立場**：realist／post-positivist ↔ contextualist／constructionist／critical realist。reflexive TA 可彈性，但必須明確宣告，且撰寫用語須與之一致。
3. **編碼取向**：inductive（資料驅動）／deductive（理論驅動）／hybrid。例如以既定理論框架重新編碼既有資料＝deductive／theoretical，但仍可走 reflexive 路線。
4. **分析深度**：semantic（表層、受訪者明說）／latent（潛層、詮釋意義）／both。
5. **去識別化確認（硬閘門）**：送入分析的逐字稿是否已去識別化（移除真實姓名、機構、地點等可識別資訊）、且知情同意書涵蓋 AI／生成式工具處理。**未確認即拒絕啟動**，回報「依研究倫理與 folder 訪談資料安全閘門，未去識別化或同意未涵蓋 AI 處理的資料不得送入分析」。**確認程序**：使用者的宣告須含三要素——資料集版本／批次、知情同意書涵蓋 AI 處理的依據（條款號或說明）、具名確認語（「應該弄好了」不足以過門）；AI 於階段 0 對每場開頭抽掃可識別資訊 pattern（真實姓名、機構、地名），命中即停機回報——宣告制＋抽檢雙保險。
6. **編碼者結構**：reflexive ⇒ 確認單人（或小團隊但不計信度）之 researcher-as-instrument 主體（你的詮釋即分析工具，與路線選擇表一致）；coding reliability ⇒ 確認編碼者數 ≥2 與編碼簿狀態（預先固定／早期鎖定）。
7. **資料前身**：本批資料是否曾以其他典範／編碼簿分析過（如既有學位論文或前期研究的 codebook）？是 → 啟動下方「跨典範重複使用資料提醒」。

### 一致性守門（攔截混用）

確認上述後，檢查組合是否自相矛盾，命中即**攔下並請使用者修正**；使用者聽取風險說明後仍明示堅持（如審稿人要求 reflexive 補 kappa 的真實情境）→ 記錄為使用者裁決、於產出頂部標記【典範混用風險：說明】後續行，不死鎖：
- 選 reflexive TA 卻要求 inter-coder reliability／kappa／Krippendorff's α → reflexive TA 在哲學上拒斥 ICR（編碼者差異是 feature 非 bug），補 kappa 即典範混用。
- 選 coding reliability 卻只有單一編碼者、或撰寫採 reflexive 知識論語言（「主題是研究者建構」）→ 與該路線的後實證前提不符。
- 宣告 realist 知識論卻要做 latent 批判詮釋且宣稱主題「浮現（emerged）」→ 提示「浮現」語言與主動建構立場的張力。

> **跨典範重複使用資料提醒**：若本批資料曾以其他典範／編碼簿分析過（例如先前以 coding reliability／codebook 分析過，本次改採 reflexive TA），等於同一資料跨兩個典範。這不是錯，但正式產出時須明說兩者知識論不同、並交代以新理論框架重新編碼的正當性，否則審稿人會質疑「你站哪個典範」。Pre-flight 命中此情境時主動標記。

---

## 路線選擇（決策輔助）

| 判準 | 傾向 reflexive TA | 傾向 coding reliability／codebook |
|------|------------------|----------------------------------|
| 編碼者 | 單人（或小團隊但不算信度） | ≥2 獨立編碼者 |
| 對「主觀性」的態度 | 資源、深度來源 | 雜訊、需以信度控制 |
| 主題的性質 | 研究者建構的「共享意義模式」 | 編碼者共識的主題／領域桶 |
| 嚴謹度依據 | 反身性、審計軌跡、理論透徹度 | 信度係數、編碼簿透明度、可複製 |
| 常見領域 | 詮釋取向社科、批判研究 | 健康、應用、混合方法、政策評估 |
| 與單作者 TSSCI 的契合 | 高（不需第二編碼者） | 低（需協作編碼資源） |

預設建議：單作者、詮釋取向、以既定理論透鏡重新編碼既有資料者 → reflexive TA。

---

## 共用六階段框架（Braun & Clarke）

兩路線共用此骨架，於特定階段分岔（分岔點見後表；逐階段操作載入對應 `references/route-*.md`）。**互動模式：階段逐一確認**——每階段產出後等使用者確認再進下一階段，因質性編碼每階段都需人類判斷，不可一次跑完。**跨 session 續作（S-0）**：各階段產出即落檔 `05_輸出/`，並於 `05_輸出/progress-log.md` 追加一行「日期｜thematic-analysis｜階段 N 完成｜產物檔路徑」；新 session 續作時先回讀 progress-log 與對應產物恢復斷點，不重跑已確認階段。長資料集全程本就橫跨多個 session，斷點續作是預設而非例外。

- **階段 0｜資料準備與去識別化驗證**：清點逐字稿；產出**帶行號的 .md 工作副本**至 `05_輸出/逐字稿工作副本/`（統一命名 `p01-[化名].md`；`02_資料與證據/` 唯讀不得改動原檔；非 .md 格式一律先轉換）——行號是引文溯源「檔:行」錨定與定向回讀的基礎；確認 Pre-flight 第 5 項去識別化硬閘門已過。
- **階段 1｜熟悉資料（familiarisation）**：通讀全部資料，產出沉浸式筆記與初步觀察，不急著編碼。
- **階段 2｜產生初始編碼（coding）**：對資料逐段編碼。reflexive＝開放、可演化的編碼；coding reliability＝依（早期鎖定的）編碼簿編碼並準備信度計算。
- **階段 3｜建構初始主題（generating initial themes）**：將編碼聚類為候選主題（reflexive：主題為意義模式，非編碼桶）。
- **階段 4｜發展與檢視主題（developing & reviewing themes）**：對照編碼摘錄與整體資料集雙層檢視；確保主題內部連貫、彼此區隔。
- **階段 5｜精煉、定義、命名主題（refining, defining & naming）**：為每個主題寫定義、命名、確立其在分析中的角色與邊界。
- **階段 6｜撰寫（writing up）**：產出主題敘事與摘要，交付 chapter-drafting 作為結果／討論章素材（不在本技能落成最終正文——正文屬 chapter-drafting）。

---

## 引文溯源稽核（硬規則，防 qualitative deepfake）

每一個 code 與每一個 theme 的支撐摘錄，必須能回溯到**真實逐字稿的具體位置**（檔名＋段落／行號）。產出時逐筆登錄於「引文溯源表」（見 phase-templates）。

- 任一摘錄無法精確比對原逐字稿 → **標記刪除**，不得保留為支撐證據。
- 禁止改寫受訪者原話後仍以引號呈現為直接引文；需要節略以 `[...]` 標示。
- 階段 6 撰寫交付前，對所有引用摘錄執行一次全量回溯核對：**每筆摘錄以 Read 重新讀取來源逐字稿該位置（±10 行）逐字比對**，禁止憑 context 記憶勾核；比對不符者刪除並於引文溯源表登錄「✗ 已刪（原因）」保留審計軌跡。未通過者不交付。

此規則對應 literature-analysis 的 claim-audit 同源精神：AI 在質性資料上最危險的失效是捏造逼真但不存在的引語。

---

## 路線分岔點摘要

| 分岔點 | reflexive TA | coding reliability／codebook |
|--------|--------------|------------------------------|
| 知識論 | constructionist／contextualist／critical realist（須宣告） | realist／post-positivist |
| 編碼者 | 單一 researcher-as-instrument | ≥2 獨立編碼者 |
| 編碼簿 | 演化中、不預先固定 | 預先固定／早期鎖定 |
| 信度 | **不用** kappa／ICR（用即混用） | kappa／Krippendorff's α＋% agreement，須報告 |
| 主題性質 | 研究者建構的共享意義模式 | 編碼者共識的主題桶 |
| 嚴謹度語言 | 反身性、審計軌跡、理論透徹 | 信度係數、透明度、可複製 |
| 主題生成語言 | 「建構／發展主題」 | 「浮現／辨識主題」可接受 |

---

## 輸出檔案規範

- 輸出位置：當前專案 `05_輸出/`（**絕不寫入** `02_資料與證據/` 或 `00_專案控制/`；`02_資料與證據/` 唯讀）。
- 命名：`主題分析_[資料集或研究代稱]_[reflexive|coding]_[產物]_YYYYMMDD_vX.md`（例：`主題分析_案例訪談_reflexive_編碼簿_20260706_v1.md`；可依你的專案命名慣例調整）。
- 主要產物：編碼簿、主題定義表、主題地圖（文字階層或 mermaid）、引文溯源表、交付 chapter-drafting 的主題敘事骨架。
- 寫入規範：一律 Write tool 完整寫檔（禁 bash heredoc／echo）；寫後重讀驗證結尾完整、無 NULL。

---

## 與其他 skill 的介面合約

- **上游資料**：`02_資料與證據/` 的去識別化逐字稿（唯讀）。
- **上游框架**：`paper-structure.md` 提供 deductive／theoretical 編碼的理論框架（如你的論文的理論框架 X／Y）。本技能不更改 paper-structure.md。
- **下游**：chapter-drafting——本技能階段 6 的主題敘事骨架，作為結果／討論章的素材；不在本技能寫最終正文。
- **下游**：review-diagnosis——第二階段面向三的「質性反身性／主導敘事偏誤」檢查，可讀本技能的反身性紀錄與引文溯源表作為佐證。

---

## 自我檢核清單（產出前確認，≤10 項）

格式：`[x] 項目 —— 是/否，簡短說明`。
```
[ ] Pre-flight 必讀齊備；路線、知識論、編碼取向、分析深度、編碼者結構已定 —— 是/否
[ ] 去識別化硬閘門已過（資料已去識別化且同意涵蓋 AI 處理）—— 是/否
[ ] 一致性守門已執行，無典範混用（reflexive 無 kappa／coding 有信度且非單人）—— 是/否
[ ] 六階段逐一確認，未一次跑完跳過人類判斷 —— 是/否
[ ] 知識論立場與撰寫用語、主題生成語言一致 —— 是/否
[ ] 引文溯源稽核全量通過：每摘錄回溯到逐字稿具體位置，無法比對者已刪 —— 是/否
[ ] 主題內部連貫、彼此區隔（階段 4 雙層檢視已做）—— 是/否
[ ] （deductive／hybrid）理論框架來源已對齊 paper-structure.md，未私自更動框架 —— 是/否
[ ] （沿用既有資料集時）跨典範議題已標記、正當性已提示 —— 是/否/不適用
[ ] 輸出寫入 05_輸出/，未誤寫 02_資料與證據 或 00_專案控制；命名合規 —— 是/否
```

---

## 版本資訊

**版本**：v1.0.1｜紅隊審查修訂
**變更歷程**：詳見 repo CHANGELOG

---

