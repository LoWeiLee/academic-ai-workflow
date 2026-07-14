#!/usr/bin/env python3
"""
keyword_search.py — literature-search 關鍵字搜尋腳本

職責：
- 對 OpenAlex title_and_abstract.search 執行 boolean 查詢
- 試搜（per_page=10）與正式搜（per_page=50），均 sort=cited_by_count:desc
- URL encoding（urllib.parse.quote_plus）
- timeout 降級鏈：title_and_abstract.search (10s) → title.search → 拆分單短語多次查詢本地合併去重
- boolean 語法驗證與修正（運算子大寫、雙引號平衡）

OpenAlex boolean 語法（必守）：
- AND / OR / NOT 必須大寫
- 半形雙引號鎖精確片語："policy capacity"
- 半形括號控制順序：A AND (B OR C)
- 自動 stemming（government 匹配 governments）；stop words 自動移除

呼叫方式：
    python3 keyword_search.py '<boolean_query>' [--mode trial|full]
    trial → per_page=10；full → per_page=50（預設 trial）

輸出（stdout，JSON）：
    {"query","encoded_url","total","mode","strategy","results":[{title,year,venue,doi,citationCount,abstract}],"degraded":[...]}

設計原則：只負責 API 呼叫與 JSON 輸出，不寫工作區檔案，不做相關性判斷
（rubric 判讀由 Claude 依 references/rubric-prompt.md 執行，禁止關鍵字匹配當判讀）。
"""
import sys, re, json, time, urllib.parse, urllib.request

OPENALEX = "https://api.openalex.org"

# 請改為你自己的 email：OpenAlex API 的 polite pool 用途
# （附上聯絡 email 可取得較高速率限制、較穩定的服務）需要換成你自己真實可用的信箱。
MAILTO = "YOUR_EMAIL@example.com"
TRIAL_TIMEOUT = 10
FULL_TIMEOUT = 30
DELAY = 0.5


def _get(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": f"litsearch/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def validate_fix(query):
    """boolean 運算子大寫化；檢查雙引號平衡。回傳 (fixed_query, notes)。"""
    notes = []
    # 只對「雙引號片語之外」的 boolean 運算子大寫化——片語內的 and/or/not 是檢索詞的一部分，
    # 誤大寫會改變 OpenAlex 的片語比對結果（例："trust and control" -> "trust AND control"）。
    def _upper_outside_quotes(q):
        parts = q.split('"')
        for i in range(0, len(parts), 2):  # 偶數索引＝引號外
            parts[i] = re.sub(r"\b(and|or|not)\b", lambda m: m.group(1).upper(), parts[i])
        return '"'.join(parts)
    fixed = _upper_outside_quotes(query)
    if fixed != query:
        notes.append("已將小寫 boolean 運算子大寫化")
    if fixed.count('"') % 2 != 0:
        notes.append("⚠️ 雙引號不平衡，請人工確認（仍嘗試送出）")
    return fixed, notes


def extract_phrases(query):
    """抽出所有雙引號片語，供降級拆分用。"""
    return re.findall(r'"([^"]+)"', query)


def brief(w):
    return {
        "title": w.get("title") or w.get("display_name"),
        "year": w.get("publication_year"),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
                 if w.get("primary_location") else None,
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "citationCount": w.get("cited_by_count"),
        "openAlexId": w.get("id", "").replace("https://openalex.org/", ""),
    }


def search(field, query, per_page, timeout):
    enc = urllib.parse.quote_plus(query)
    url = (f"{OPENALEX}/works?filter={field}.search:{enc}"
           f"&per_page={per_page}&sort=cited_by_count:desc&mailto={MAILTO}")
    data = _get(url, timeout)
    return url, data.get("meta", {}).get("count", 0), data.get("results", [])


def _finalize(out):
    """環境阻擋顯性化：degraded 原因含 403 即標 env_block_suspected，
    供 SKILL 階段規則辨別「環境阻擋」與「真零命中」，避免 total=0 被誤讀。"""
    out["env_block_suspected"] = any("403" in str(d.get("reason", "")) for d in out.get("degraded", []))
    return out


def run(query, mode):
    per_page = 10 if mode == "trial" else 50
    timeout = TRIAL_TIMEOUT if mode == "trial" else FULL_TIMEOUT
    fixed, notes = validate_fix(query)
    out = {"query": fixed, "mode": mode, "degraded": [], "syntax_notes": notes}

    phrases = extract_phrases(fixed)
    # 主策略：title_and_abstract.search
    try:
        url, total, results = search("title_and_abstract", fixed, per_page, timeout)
        out.update(encoded_url=url, total=total, strategy="title_and_abstract.search",
                   results=[brief(w) for w in results])
        return _finalize(out)
    except Exception as e:
        # 降級條件：含 ≥ 2 雙引號片語且 timeout（或任何失敗）
        out["degraded"].append({"from": "title_and_abstract.search", "reason": str(e)})

    # 降級 1：title.search
    try:
        url, total, results = search("title", fixed, per_page, FULL_TIMEOUT)
        out.update(encoded_url=url, total=total, strategy="title.search(降級1)",
                   results=[brief(w) for w in results])
        out["degraded"].append({"to": "title.search"})
        return _finalize(out)
    except Exception as e:
        out["degraded"].append({"from": "title.search", "reason": str(e)})

    # 降級 2：拆分單短語多次查詢，本地合併去重
    if len(phrases) >= 2:
        merged, seen = [], set()
        for ph in phrases:
            try:
                url, total, results = search("title_and_abstract", f'"{ph}"', per_page, FULL_TIMEOUT)
                for w in results:
                    b = brief(w)
                    k = b["doi"] or b["openAlexId"]
                    if k and k not in seen:
                        seen.add(k)
                        merged.append(b)
                time.sleep(DELAY)
            except Exception as e:
                out["degraded"].append({"phrase": ph, "reason": str(e)})
        out.update(encoded_url="(多次單短語查詢)", total=len(merged),
                   strategy="單短語拆分合併(降級2)", results=merged)
        return _finalize(out)

    out.update(total=0, strategy="全部降級失敗", results=[])
    return _finalize(out)


def _warn_mailto():
    """MAILTO 仍為佔位符時印一行提示（不中斷）。OpenAlex polite pool 為禮貌性建議，非硬性要求。"""
    if MAILTO.startswith("YOUR_EMAIL"):
        print("提示：MAILTO 仍為佔位符，未加入 OpenAlex polite pool（服務品質可能較不穩定，但不影響執行）。"
              "如需設定，請修改你實際安裝的那份 skill 內 scripts/ 三支腳本的 MAILTO 值。", file=sys.stderr)


def main():
    _warn_mailto()
    if len(sys.argv) < 2:
        print("usage: keyword_search.py '<boolean_query>' [--mode trial|full]", file=sys.stderr)
        sys.exit(1)
    query = sys.argv[1]
    mode = "trial"
    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
    print(json.dumps(run(query, mode), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
