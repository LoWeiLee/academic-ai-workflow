# academic-ai-workflow starter kit

本工作區採三層架構（**規則層、思考層、執行層**），三層之下另有一個治理基座（資料夾讀寫規則）。分層的依據不是「檔案放在哪裡」，而是「人與 AI 各自把什麼外化給對方」：規則層寫給 AI 看，思考層寫給自己看，執行層是人機共同工作的地方。clone 後請依序完成三件事：填寫控制檔、安裝七道工序 skill、依骨架建立你的專案資料夾。

**規則層｜寫給 AI 看的判斷力外化（`00_專案控制/`）**：`about-me.md`（你是誰、目標與優先序，含寫作慣性自我申報）、`research-identity.md`（研究定位與理論版圖）、`writing-standards.md`（寫作規範與個人風格庫）、`portfolio-status.md`（發表組合動態儀表板）。四檔皆為欄位模板，內含填寫指引與虛構範例句。**四份都必須留在 `00_專案控制/`**——skill 會直接讀取，缺檔會導致工序中斷（例如 chapter-drafting 缺 `writing-standards.md` 即停止）。但**首跑只需要動筆客製化兩份**：`about-me.md` 與 `research-identity.md`。另兩份留在原地即可：`writing-standards.md` 的多數條文可直接沿用預設（個人風格庫先留空，日後累積），`portfolio-status.md` 等你真的有多篇論文在跑時再補。動筆的兩份請用你自己的話寫，別把虛構範例句留著。填寫後任務執行時視為唯讀，僅在你主動更新進度時修改。

**思考層｜寫給自己看的思考外顯化（`00_專案控制/paper-structure.md`）**：你要回答什麼問題、核心命題是什麼、論證路徑怎麼走、用什麼支撐，以及誠實標記的卡關點。由工序一（research-design-diagnosis）協作產出，是整條管線的中樞，AI 的所有下游工作都錨定在你寫下的思考上；你還沒想清楚的地方誠實標記，不由 AI 代想。

**執行層｜人機共同工作的七道工序 skill**：research-design-diagnosis（研究設計）→ literature-search（找文獻）→ literature-analysis（逐篇分析）→ literature-synthesis（跨篇綜整）→ chapter-drafting（章節撰寫）→ review-diagnosis（審稿診斷）→ thematic-analysis（質性主題分析，視研究類型選用）。各 skill 會讀取規則層以調整協作策略，不在本骨架內另行安裝，請依你使用的 skill 套件另行掛載。

**治理基座｜資料夾讀寫規則**：`00_專案控制/`、`01_文獻/`、`02_資料與證據/`、`03_寫作/`、`04_審稿與回應/`、`05_輸出/` 六夾對應研究流程的不同階段。00–04 五夾在任務執行時唯讀，AI 只讀取不寫入；`05_輸出/` 是所有 AI 產出的唯一寫入區，依專案建子資料夾分流。**唯一例外**：literature-analysis 依其協議回寫 `00_專案控制/paper-structure.md` 的「文獻分析完成清單」，這是唯讀規則明文授權的單一破口，除此之外 00–04 一律不得寫入。各夾詳細讀寫紀律與檔名規則見各自的 `README.md`，本工作區根目錄的 `CLAUDE.md` 則是同一套規則的 AI 開場版本（掛載後自動載入，不觸發 skill 時亦有效）。

**開工前**：使用前請先把整個工作區資料夾連接給 Claude（Cowork 的資料夾入口；每次開新對話都要確認），否則上述所有規則與控制檔 AI 都讀不到。步驟見 [docs/快速上手指南.md](../docs/快速上手指南.md) 第 3.5 步。**若你只有 claude.ai 網頁版**（無 Cowork／Claude Code），沒有工作區資料夾可以連接，改把控制檔放進 claude.ai 的 Project files；此時七道工序退化為七把獨立的工具，操作見 [docs/在-claude-ai-上使用.md](../docs/在-claude-ai-上使用.md)。（本段兩個連結以完整 repo 目錄結構為準；若你只單獨複製了 starter-kit 資料夾，連結會失效，請直接到 https://github.com/LoWeiLee/academic-ai-workflow 的 docs/ 查看。）

**四者對應關係**：規則層決定「AI 如何跟你協作」，思考層決定「這篇論文要論證什麼」，執行層決定「AI 做什麼工序」，治理基座決定「產出放哪裡、誰能寫」。四者分工清楚、互不重複，是讓多人／多專案共用同一套工作流時仍保持秩序的基礎。
