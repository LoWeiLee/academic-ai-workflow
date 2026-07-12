# CHANGELOG

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
