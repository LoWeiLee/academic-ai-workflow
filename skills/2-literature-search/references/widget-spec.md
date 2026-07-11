# widget-spec.md — literature-search 階段四 Pending 裁決 Widget 實作規範

> 進入階段四（使用者決策）時載入。**必須使用互動式 widget 呈現 pending 條目，不得使用 markdown 表格。**

## 視覺規格

```
┌─────────────────────────────────────────────────────────────────────┐
│ Pending 裁決｜共 X 筆（★ 特殊保留 Y 筆｜分數競爭 Z 筆）              │
│ 排序：信心低→高（低信心先處理）｜一頁 20 筆｜第 N / M 頁             │
├─────────────────────────────────────────────────────────────────────┤
│ # 1  ★                                                              │
│ Wu et al. (2015) — Organizational Resilience in the Digital Age     │
│ Public Administration Review · 2015 · Cited 568                     │
│ DOI: 10.xxxx/yyy                                                    │
│                                                                      │
│ rubric: 9/12 | basis: title+abstract | Claude: 納入 | 信心: 高      │
│ 建議理由：主題核心契合，理論與方法均對話 paper-structure            │
│ 他處已收錄：Paper A / 主題X                                          │
│                                                                      │
│ [ 納入 ]  [ 暫存 ]  [ 排除 ]                                         │
├─────────────────────────────────────────────────────────────────────┤
│ # 2 ...                                                             │
└─────────────────────────────────────────────────────────────────────┘

[ 送出本頁裁決 ]  [ 上一頁 ]  [ 下一頁 ]
```

## 欄位規格

每條目依序顯示：
1. 編號 + ★ 標記（特殊保留層時）
2. 作者（首作者姓 + et al.）+ 年 + 標題
3. Venue · 年 · Cited N
4. DOI（可複製）
5. 空行
6. 「rubric: X/12 | basis: {basis} | Claude: {建議} | 信心: {高/低}」
7. 「建議理由: {rubricReasoning 四維度濃縮成一句}」
8. 「他處已收錄: {若 _index.json 有對應條目}」否則不顯示此行
9. 三個按鈕：納入 / 暫存 / 排除

## 互動規格

| 動作 | 視覺反應 |
|---|---|
| 點選「納入」 | 該按鈕變為綠色填滿（#22c55e、白字）；同列其他按鈕變未選（灰邊框、白底、黑字）|
| 點選「暫存」 | 該按鈕變黃色填滿（#eab308、白字）；同列其他變灰 |
| 點選「排除」 | 該按鈕變紅色填滿（#ef4444、白字）；同列其他變灰 |
| 再點同一按鈕 | 取消選擇，三按鈕回初始樣式 |
| 點選其他按鈕 | 切換選擇，只有最新點選的高亮 |
| 點「送出本頁裁決」 | 若有未裁決條目，提示「第 X 筆未裁決」並滾動到該條目；全部已裁決則呼叫 `sendPrompt(JSON.stringify({page: N, decisions}))` 將本頁裁決回傳對話（Claude 據此寫入 search_log Part B.5），再進入下一頁 |
| 「上一頁」/「下一頁」| 切換頁面；已裁決狀態保留在記憶體 |

## 技術實作模式（必守，避免 onclick 引號爆炸與高亮未運作等已知問題）

1. **使用 data attributes，禁止 onclick 內嵌字串**：
   ```html
   <button data-doi="10.xxx/yyy" data-action="include">納入</button>
   ```

2. **單一 event listener 綁容器，用 event delegation**：
   ```javascript
   document.getElementById('pending-container').addEventListener('click', (e) => {
     if (e.target.tagName !== 'BUTTON') return;
     const doi = e.target.dataset.doi;
     const action = e.target.dataset.action;
     if (!doi || !action) return;
     handleDecision(doi, action, e.target);
   });
   ```

3. **裁決狀態存純 JS 物件，非 DOM 屬性**：
   ```javascript
   const decisions = {};  // { doi: 'include' | 'shelf' | 'exclude' }
   ```

4. **按鈕樣式切換透過 className，非 inline style**：
   ```javascript
   const buttonGroup = clickedButton.parentElement;
   buttonGroup.querySelectorAll('button').forEach(b => { b.className = 'decision-btn'; });
   if (decisions[doi] !== action) {
     clickedButton.className = `decision-btn selected-${action}`;
     decisions[doi] = action;
   } else {
     delete decisions[doi];
   }
   ```

5. **CSS class 定義**：
   ```css
   .decision-btn { /* 初始：灰邊框、白底、黑字 */ }
   .decision-btn.selected-include { background: #22c55e; color: white; border-color: #22c55e; }
   .decision-btn.selected-shelf   { background: #eab308; color: white; border-color: #eab308; }
   .decision-btn.selected-exclude { background: #ef4444; color: white; border-color: #ef4444; }
   ```

## 呈現前 Claude 先說明

```
以下 X 筆 pending 條目待你裁決（★ 特殊保留 Y 筆｜分數競爭 Z 筆）。

★ 標記意義：因學術判斷上重要性而保留的條目（高被引老論文、經典白名單、
預印本、年代邊緣但相關性高），不是依 rubric 分數進 pending 的，判讀時
建議特別注意。

Pending 按信心排序——低信心先處理（校對模式、快），高信心後處理
（前瞻判斷、慢）。一頁 20 筆。
```

## 實作完成檢查項

**靜態自查（Claude 能做）**：
- [ ] 所有按鈕綁定透過 data attributes，程式碼中無 onclick="..." 字串
- [ ] decisions 物件＋className 切換邏輯完整；「送出本頁裁決」呼叫 sendPrompt 回傳 decisions JSON

**互動實測（使用者回報——Claude 無法點擊自產 widget 或讀取 console，不得宣稱已驗證互動）**：
- [ ] 高亮／切換／取消行為正常；送出後 Claude 有收到裁決 JSON 並寫入 Part B.5——異常時回報 Claude 修正
