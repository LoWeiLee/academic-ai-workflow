# rubric-prompt.md — literature-search 階段三 rubric 判讀參考檔

> 進入階段三（判讀分桶）時載入。本檔承載 rubric 四維度定義、anchor examples 與 LLM 判讀的 prompt 結構。
> **prompt 版本**：v1.0.1｜紅隊審查修訂。版本號寫入 search_log 簽名區。
> **硬性規則**：rubric 判讀一律採 LLM 語義判讀；**禁止使用關鍵字匹配**（如 `if 'keyword' in text`）作為判讀方式。

---

## LLM 判讀的 prompt 結構

對每篇論文讀 title + abstract（+ tldr 若有），基於 paper-structure.md 脈絡套用下列 prompt：

```
## 研究脈絡
- RQ：{從 paper-structure.md 抽取}
- 理論框架：{同上}
- 方法論：{同上}
- 本節處理的核心議題：{同上}

## Rubric 四維度定義與 anchor examples
{下方四維度完整定義}

## 本批待判讀論文（共 10 篇）
### 候選論文 1
- Title / Authors / Year / Venue / Abstract / TLDR（若有）
...

## 輸出要求
每篇論文輸出：
- rubricScores: {relevance: 0-3, theory: 0-3, method: 0-3, quality: 0-3}
- rubricReasoning: {四維度各 1-2 句判斷理由}
- rubricBasis: title_only / title+abstract / title+abstract+tldr
```

**批次規模**：每批 10 篇，批次間的中間結果寫入 `/tmp/*.json`。

---

## Rubric 四維度定義與 anchor examples

> 下列 anchor examples 為通用示例，示意各分數等級的判斷方式；實際使用時請依你的 RQ、理論框架、方法論替換為你自己的主題語彙。

### D1. 主題相關性（Relevance）

| 分 | 定義 | anchor example（以「組織韌性」為 RQ 為例）|
|---|---|---|
| 3 | abstract 明確處理 RQ 核心概念，且為該論文主題 | "This paper examines **how digital transformation reshapes organizational resilience** in regulatory agencies..." |
| 2 | abstract 提及 RQ 核心概念但非主題（作為背景/變項）| "Drawing on **organizational resilience** literature, we examine street-level discretion..." |
| 1 | abstract 涉及 RQ 相鄰概念（同領域但不同焦點）| "This paper examines **organizational adaptability** in crisis governance..." |
| 0 | abstract 明顯處理無關主題 | "This study uses a resilience-like framework in industrial engineering..." |

### D2. 理論契合（Theory）

| 分 | 定義 | anchor example（以「資源依賴理論」為理論框架為例）|
|---|---|---|
| 3 | 明確使用、批判、擴展 paper-structure 的理論框架 | "Building on **Pfeffer and Salancik's resource dependence theory**, we..." |
| 2 | 使用同傳統或對話傳統的理論 | "Drawing on **organizational ecology** and network theory..." |
| 1 | 使用競爭或替代理論但仍有對話價值 | "This paper adopts a **rational choice** perspective..." |
| 0 | 理論取向完全無關或無明確理論框架 | "This descriptive study documents..." |

### D3. 方法契合（Method）

| 分 | 定義 | anchor example（以「質性訪談」為方法為例）|
|---|---|---|
| 3 | 方法論相同或能直接對話 | "We conducted **semi-structured interviews** with 45 officials..." |
| 2 | 方法論相容（混合方法、案例研究） | "This **multi-case study** uses document analysis and interviews..." |
| 1 | 方法論不同但結論可引用 | "We use **SEM** on survey data of 1200 citizens..." |
| 0 | 方法論無法對話 | "We develop a **mathematical model** of bureaucratic decisions..." |

### D4. 品質訊號（Quality）

| 分 | 定義 | anchor example |
|---|---|---|
| 3 | Top venue（你的領域公認頂尖期刊）且 citation 符合年代表現 | 2020 年論文，領域頂尖期刊，87 cites |
| 2 | 合格 SSCI/TSSCI venue 或 top venue 但 citation 偏低 | 領域一般期刊，25 cites（2021）|
| 1 | 合格但邊緣 venue，或預印本但作者具聲望 | 新興期刊 / SSRN working paper by 知名學者 |
| 0 | 掠奪性期刊、非同儕審查、citation 異常低 | 邊緣期刊 / 0 cites after 3 years |

> 註：SSCI／TSSCI 為在地示例的期刊分級，請依你所屬學術體系的分級標準替換。

---

## rubricBasis 記錄

每篇論文記錄 `rubricBasis` 欄位於 `_metadata.json`：
- `title_only`：僅有標題可用
- `title+abstract`：標題與摘要皆有
- `title+abstract+tldr`：三者齊備

---

## 分桶規則（與 SKILL.md「分桶閾值規則」一致，此處為 rubric 判讀後的落桶參照）

- 總分 ≥ 9 且主題相關性 = 3 → **納入**（自動）
- 主題相關性 = 0 或總分 ≤ 3 → **排除**（自動）
- 其他 → **Pending**（使用者裁決）
- **title_only 保守化**：`rubricBasis == "title_only"` 時，排除閾值由 ≤ 3 上修為 ≤ 5

### Pending 桶附加欄位
- `claudeSuggestion`：include / shelf / exclude
- `claudeConfidence`：high / low
- 總分 6–8 且主題相關性 ≥ 2 → suggestion: shelf，confidence: high
- 總分 6–8 且主題相關性 < 2 → suggestion: exclude，confidence: low
- 總分 4–5（未觸自動排除）→ suggestion: exclude，confidence: low
- **confidence 降 low 的操作條件（任一命中即 low，優先於上列 high）**：(a) 接近閾值＝總分與任一自動分桶閾值差 ≤1 分；(b) venue 弱＝D4 品質分 ≤1；(c) 年代邊緣＝出版年距年代下限 ≤2 年

### 特殊處理
- **預印本**：進 pending，suggestion: include, confidence: low
- **經典白名單**：paper-structure.md 指定 DOI 跳過 rubric 直接納入
- **年代老於下限的高被引（citationCount > 500 且相關性 ≥ 2）**：進 pending 特殊保留層（★）
