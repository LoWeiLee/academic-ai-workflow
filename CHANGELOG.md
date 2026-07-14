# CHANGELOG

## v1.1.1（第二輪紅隊審查修訂，2026-07-14）

依第二輪紅隊審查結果修訂，七支重打包為 `_v1.1.1.skill`。

**修正（阻斷級）**
- literature-search：修正 `citation_expand.py`／`keyword_search.py` 解析 OpenAlex venue 時，`source` 欄位為 null 即拋 AttributeError 導致整批無謂降級的 bug（實測復現）
- chapter-drafting：Part 0.1 對 `paper-structure.md` 缺漏新增「簡化結構模式」逃生門——重寫既有草稿或小規模試用時，可由使用者當場提供研究問題、論述目標與字數目標充當臨時結構錨，不再硬性拒絕啟動（description 明列的「這段草稿幫我重寫」觸發情境原本是死路）

**修正（一致性與可攜性）**
- chapter-drafting：description 與本文對 `folder-instructions.md` 的選配地位對齊（原 description 誤標為強制必讀，會複製 v1.0.1 已修掉的缺檔誤拒）；介面合約「台灣脈絡適用性」欄位名對齊 literature-synthesis 公版「特定研究情境的適用性說明」；必讀清單補 `about-me.md`（3a 列，缺漏不拒絕啟動），使寫作慣性機制讀得到權威來源
- review-diagnosis：嚴格度層級表補「國際 SSCI」對應列（原 Pre-flight 有此選項但表中無錨點）；TSSCI 分級加「臺灣在地示例，請依所屬體系替換」說明
- literature-analysis／literature-synthesis：SKILL.md 內補「3_文獻」vault 慣例名與 starter-kit `01_文獻/` 的橋接說明（原僅存於 starter-kit README，單裝 .skill 者看不到）；literature-synthesis 步驟一補「vault 路徑不存在→視同無知識檔走 Mode A」分支；`split_legacy.py` 版本戳與 SKILL 同步（原滯留 v1.0.1）
- starter-kit：01–05 五份 README 檔名規則統一為含日期版，與 CLAUDE.md 一致（原兩套規則並存）

**文件**
- README：開頭加導讀標示與「名詞速解／你需要準備什麼」導引框（skill 白話定義、Cowork 方案門檻與官方連結）；架構圖改用中文標籤版；回饋管道補 GitHub Issues 落點；DuoDuoRun 改標準連結
- README_CHT／README_EN／白皮書：引用格式版本號由 v1.0.0 對齊為 v1.1.1
- 快速上手指南：A 路徑補 Cowork 取得方式（Pro 起、桌面應用、官方說明連結）；Claude Code 安裝補 skills 目錄具體路徑
- 在 claude.ai 上使用：「付費版」明確為「付費方案（Pro 起）＋桌面應用」

**打包**
- 七支重打包為 `_v1.1.1.skill`（research-design-diagnosis、thematic-analysis 本輪無內容變更，僅版本對齊）。舊版 `_v1.1.0.skill` 請於檔案總管手動刪除（版本回溯依靠 git 歷史）

## v1.1.0（無工作區模式，2026-07-13）

七支 skill 全數改版重打包。本版讓七支工序在**沒有持久工作區資料夾的環境**（claude.ai 網頁版）能自動降級運作，取代 v1.0.2 文件中要求使用者手動貼上的「開場宣告」。

**新增：環境偵測與無工作區模式（七支逐字一致的統一條款）**
- 七支 SKILL.md 於所有讀取動作之前新增「環境偵測」區塊：`00_專案控制/` 路徑不存在時，不得以「檔案缺失」為由拒絕啟動，一律進入無工作區模式
- 無工作區模式三規則：(1) 控制檔改由對話附件 → Project files → 使用者指定位置依序查找，**此規則明文覆蓋各 skill 原有的「缺漏即拒絕啟動」硬閘門**（閘門的實質要求是「讀得到內容」，不是「檔案位於特定路徑」）；(2) 產出改以可下載檔案交付，不寫入 `05_輸出/`，晉升由使用者手動完成；(3) 跨 session 狀態（`progress-log.md`、chapter-drafting 的凍結段）改由使用者於開場提供前輪產出
- 啟動宣告必須載明當前模式（「工作區模式」／「無工作區模式」）
- 修掉的實際故障：chapter-drafting 的 Part 0.1「任一缺漏即拒絕啟動」、thematic-analysis 與 review-diagnosis 的必讀閘門，原本會在 claude.ai 上直接卡死無法啟動

**literature-search：環境限制明文化**
- 錯誤處理表補入具體事實：claude.ai 沙盒核准網域為固定白名單（PyPI／npm／GitHub／Ubuntu／crates.io ＋ Anthropic API），**不含** `api.openalex.org` 與 `api.semanticscholar.org`，Free／Pro／Max 無法自行增加網域（僅 Team／Enterprise 擁有者可自訂）。此環境下不必試搜，直接宣告環境阻擋並轉手動匯出模式

**環境代名詞收斂為環境中立表述（10 處）**
- 範本頁尾「分析者：Claude（Cowork 模式）」×5（skill 3、4 的四份範本與 skill 4 SKILL.md）、「撰寫協作：Claude（Cowork 模式）」×1（skill 5 format-templates）——**這一行會被複製進使用者的每一份產出檔**，等於在產出上蓋一個錯的環境戳章
- `file-specs.md` 的「Cowork 端」→「工作流端」；skill 2 description 的「Cowork 沙盒限制」→「執行環境的沙盒限制」；skill 4 晉升流程補上無工作區模式的對應動作

**打包**
- 七支重打包為 `_v1.1.0.skill`，依白皮書「唯一正本、整包重打」紀律刪除 `_v1.0.1.skill`（版本回溯依靠 git 歷史）
- 打包檔已驗證不含 `__pycache__`／`.pyc`

## v1.0.2（環境路徑澄清，2026-07-12）

僅文件變更，skill 原始碼與打包檔未動（維持 v1.0.1）。

**新增 claude.ai 單支使用路徑**
- 新增 `docs/在-claude-ai-上使用.md`：七支 skill 在 claude.ai 網頁版的單支獨立使用手冊，含安裝步驟、Project files 準備、開場宣告模板、七支的單支使用卡、手動交接流程、三個真實限制
- 澄清一項此前未載明的事實：**Skills 在 claude.ai 自 Free 方案起即可用**，`.skill` 打包檔（含 `references/`、`scripts/`）可直接上傳、不需拆解。過往文件將 Cowork／Claude Code 隱含為唯一入口，形成不必要的採用門檻
- 快速上手指南「事前準備」改寫為兩種用法的分岔（A. 管線用法／B. 單支工具用法），附能力對照表與路徑指引；FAQ 增列「我只有 claude.ai，能用嗎？」
- README（根／CHT／EN）修正「以 Claude Cowork 平台搭建」的絕對化表述，並補上 claude.ai 路徑的指引

**環境限制的顯性化**
- 明載 claude.ai 沙盒的網域白名單（PyPI／npm／GitHub／Ubuntu／crates.io ＋ Anthropic API）**不含** `api.openalex.org` 與 `api.semanticscholar.org`，故 literature-search 的自動搜尋在 Free／Pro／Max 上必然被擋，只能走 skill 內建的手動匯出模式；Team／Enterprise 擁有者可自訂網域白名單解除此限制
- 明載跨對話狀態（`progress-log.md`、chapter-drafting 的段落凍結）在無持久檔案系統時失效，並給出人工替代動作
- 明載 skill 內文的 `00_專案控制/` 路徑錨點在 claude.ai 上不存在，提供一次性的開場宣告模板繞過；skill 內建的自動降級分支列為下一版待辦
- 白皮書 §7.1 補「環境的一則說明」，指出 §2.4（唯一寫入區）與 §5（狀態必須落檔）預設持久檔案系統，並指向 claude.ai 路徑
- `docs/進階_知識庫與Obsidian整合.md`：frontmatter 的消費端由「Cowork 端」改為「工作流端」（不限執行環境）

**控制檔口徑統一為「四份就位、兩份必填」**
- 修掉五份文件的三種說法：`starter-kit/README.md` 說「使用前請完整填寫」（最嚴）、白皮書 §7.1 與 README×2 說「填寫四份」（中）、快速上手指南說「首跑只需兩份」（最寬）。歧異的根源是「填」這個動詞混用了「檔案就位」與「客製化撰寫」兩個動作
- 統一表述：**四份模板都必須留在 `00_專案控制/`**——skill 直接讀取，缺檔會使工序中斷（chapter-drafting 缺 `writing-standards.md` 即停止，thematic-analysis 缺 `research-identity.md` 亦然）；**但首跑只需動筆客製化兩份**（`about-me.md`、`research-identity.md`），`writing-standards.md` 沿用模板預設條文、`portfolio-status.md` 可留空
- 修掉快速上手指南第二步的內部打架：標題說「四份」、內文說「兩份」、下一段又給四份的填寫順序
- 四份控制檔模板的 frontmatter `note` 同步校正（原本一律寫「使用前請完整填寫」，`writing-standards.md` 改為「首跑不必動筆，但必須留在資料夾」、`portfolio-status.md` 改為「首跑可留空，但必須留在資料夾」）
- `starter-kit/README.md` 另補 claude.ai 使用者的 Project files 替代路徑（原文只講 Cowork 的資料夾入口）

**下一版待辦（v1.1）**：已於 v1.1.0 完成，見上。

## v1.0.1（紅隊審查修訂，2026-07-12）

**新手上手路徑（阻斷性修正）**
- 快速上手指南新增「第 3.5 步：把工作區交給 Claude」——原指南全篇未教使用者把工作區資料夾連接給 Cowork，導致照做也啟動不了整條鏈條
- 最小起步組合統一為 research-design-diagnosis + literature-analysis（原三份文件互相矛盾：README 說 1+3、指南與白皮書說 2+3）；literature-search 改列為選配的第五步
- .skill 安裝步驟改為具體點擊路徑（Settings → Capabilities → Skills → Upload skill）
- 指南明示 `paper-structure.md` 的正本化步驟（`05_輸出/` → 改名搬入 `00_專案控制/`）；skill 1 與 skill 2 兩端同步補上此指示與 fallback，修掉 skill 1↔2 之間的交接斷點
- 首跑控制檔減量：只需填 `about-me.md` 與 `research-identity.md`

**治理規則的可執行性**
- starter-kit 新增 `CLAUDE.md`：掛載後自動載入的治理規則常駐版本，使唯讀分區與晉升流程在未觸發 skill 的一般對話中同樣有效
- 修正「權責分離由檔案系統強制」的過度宣稱（README ×2、白皮書 §2.4）——實際由工作流制度與各工序條文強制，並補上誠實聲明
- skill 3 的完成清單回寫授權改為自足表述，不再引用不存在的「全域協作規範」；starter-kit README 與指南同步標明此唯一例外
- 刪除 skill 4/5/7 對不存在的「Global Instructions」的懸空引用；`folder-instructions.md` 改列為選配，不存在時不視為缺失

**skill 內部一致性**
- skill 6 frontmatter description 補上 Mode E（AI 使用揭露）與其觸發詞——原描述僅列四種模式，Mode E 為觸發死路徑
- `reasoning-framework.md` 四份副本（skills 1/4/5/6）收斂為逐字一致，刪除互相矛盾的 canonical／控制中樞宣稱
- skill 3 範本殘留的私人版本號 v4.1（6 處）修正
- skill 4 兩份範本的 frontmatter 解除 ```yaml 圍欄，改為真 frontmatter（避免產出檔破壞 `covers_citation_keys` 增量偵測與 Obsidian 解析）
- 路徑分隔符、機制範本名稱、vault 晉升措辭、TSSCI／國科會在地示例註記等一致性修正

**腳本**
- 三支搜尋腳本：MAILTO 仍為佔位符時印 stderr 提示（不中斷）；`urllib.error` 顯式匯入
- `keyword_search.py`：boolean 運算子大寫化改為只作用於雙引號片語之外，不再誤傷 `"trust and control"` 這類片語
- `citation_expand.py`：`utcnow()` → `now(timezone.utc)`
- `split_legacy.py`：`--pdf-dir` 的配對結果現在真正反映在 PDF wikilink；移除未使用的死參數

**其他**
- `.gitignore` 補 `__pycache__/`、`*.pyc`、`.DS_Store`
- README 的 skill 名稱錯字（×2）與其他錯字、LICENSE 授權範圍表述、白皮書資料夾計數等修正
- 七支 skill 全數重打包為 v1.0.1

## v1.0.0（公版初版，2026-07）
- 七支研究工作流 skill 公版發布：research-design-diagnosis、literature-search、literature-analysis、literature-synthesis、chapter-drafting、review-diagnosis、thematic-analysis
- starter-kit：00_專案控制 控制檔模板 ×4＋00–05 資料夾骨架與 01–05 各層 README
- 授權：文件與 skill 主體 CC BY 4.0；scripts/ MIT；thematic-analysis CC BY-NC 4.0（見 LICENSE.md）
