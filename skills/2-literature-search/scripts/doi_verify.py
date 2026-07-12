#!/usr/bin/env python3
"""
doi_verify.py — literature-search 種子 DOI 驗證腳本

職責：
- Claude 訓練記憶中的 DOI 不可信，逐篇對 OpenAlex /works/doi:{doi} 驗證
- 驗證項：DOI 是否存在、回傳標題與提名標題模糊匹配、回傳年份匹配
- DOI 不匹配 → 以標題在 OpenAlex title.search 重搜，找到正確 DOI 則替換
- DOI 404 / 重搜失敗 → 一律標 unverified（OpenAlex 404 ≠ DOI 無效；是否移除由使用者裁決）
- OpenAlex 失敗時以 Semantic Scholar /paper/DOI:{doi} 備援

呼叫方式：
    python3 doi_verify.py '<json>'
其中 <json> 為提名清單：
    [{"doi": "10.x/y", "title": "...", "year": 2015}, ...]
亦可：python3 doi_verify.py --file nominations.json

輸出（stdout，JSON）：{"env_block_suspected": bool, "results": [每筆含
    {"input_doi","verified","status","final_doi","final_title","year","method","note"}]}
    status ∈ verified | replaced | unverified | removed
    env_block_suspected=true（note 含 403）＝環境 allowlist 阻擋，非 DOI 無效，轉手動匯出模式

設計原則（對應 45 秒 bash timeout；工作區落檔由 Claude 用 Write tool 完成）：
- 本腳本只負責 API 呼叫與 JSON 輸出到 stdout，不寫工作區檔案（由 Claude 用 Write tool 落檔）
- 每次呼叫處理的提名數不宜過多（建議 ≤ 5 篇），避免單次 bash 逾時
"""
import sys, json, time, urllib.parse, urllib.request, urllib.error

OPENALEX = "https://api.openalex.org"
S2 = "https://api.semanticscholar.org/graph/v1"
RATE_DELAY = 0.5          # OpenAlex 固定延遲
TIMEOUT = 30             # 一般端點 timeout

# 請改為你自己的 email：OpenAlex／Semantic Scholar API 的 polite pool 用途
# （附上聯絡 email 可取得較高速率限制、較穩定的服務）需要換成你自己真實可用的信箱。
MAILTO = "YOUR_EMAIL@example.com"  # OpenAlex polite pool


def _get(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": f"litsearch/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _norm(s):
    return "".join(c.lower() for c in (s or "") if c.isalnum())


def _title_match(a, b):
    """模糊匹配：正規化後一方包含另一方，或共同前綴足夠長。"""
    na, nb = _norm(a), _norm(b)
    if not na or not nb:
        return False
    if na in nb or nb in na:
        return True
    short = min(len(na), len(nb))
    common = sum(1 for i in range(short) if na[i] == nb[i])
    return short > 0 and common / short >= 0.85


def openalex_by_doi(doi):
    url = f"{OPENALEX}/works/doi:{urllib.parse.quote(doi)}?mailto={MAILTO}"
    return _get(url)


def openalex_title_search(title):
    q = urllib.parse.quote_plus(title)
    url = f"{OPENALEX}/works?filter=title.search:{q}&per_page=5&sort=cited_by_count:desc&mailto={MAILTO}"
    return _get(url).get("results", [])


def s2_by_doi(doi):
    url = f"{S2}/paper/DOI:{urllib.parse.quote(doi)}?fields=title,year,externalIds"
    return _get(url)


def verify_one(item):
    doi = (item.get("doi") or "").strip()
    title = item.get("title") or ""
    year = item.get("year")
    out = {"input_doi": doi, "verified": False, "status": "unverified",
           "final_doi": doi, "final_title": title, "year": year,
           "method": "", "note": ""}

    # 1) OpenAlex by DOI
    if doi:
        try:
            w = openalex_by_doi(doi)
            w_title = w.get("title") or w.get("display_name") or ""
            w_year = w.get("publication_year")
            if _title_match(title, w_title):
                out.update(verified=True, status="verified", final_doi=doi,
                           final_title=w_title, year=w_year, method="openalex_doi")
                if year and w_year and abs(int(year) - int(w_year)) > 1:
                    out["note"] = f"年份提示：提名 {year} vs OpenAlex {w_year}"
                return out
            else:
                out["note"] = f"DOI 存在但標題不符（OpenAlex：{w_title[:60]}）"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                out["note"] = "DOI 在 OpenAlex 為 404"
            else:
                out["note"] = f"OpenAlex HTTP {e.code}"
        except Exception as e:
            out["note"] = f"OpenAlex 錯誤：{e}"
        time.sleep(RATE_DELAY)

    # 2) 標題重搜（DOI 不符或缺 DOI）
    if title:
        try:
            results = openalex_title_search(title)
            for r in results:
                r_title = r.get("title") or r.get("display_name") or ""
                if _title_match(title, r_title):
                    new_doi = (r.get("doi") or "").replace("https://doi.org/", "")
                    if new_doi:
                        out.update(verified=True, status="replaced", final_doi=new_doi,
                                   final_title=r_title, year=r.get("publication_year"),
                                   method="openalex_title_research",
                                   note=(out["note"] + "｜已由標題重搜取得正確 DOI").strip("｜"))
                        return out
            out["note"] = (out["note"] + "｜標題重搜無足夠匹配").strip("｜")
        except Exception as e:
            out["note"] = (out["note"] + f"｜重搜錯誤：{e}").strip("｜")
        time.sleep(RATE_DELAY)

    # 3) S2 備援（僅確認存在性）
    if doi:
        try:
            p = s2_by_doi(doi)
            if p and p.get("title") and _title_match(title, p.get("title")):
                out.update(verified=True, status="verified", final_doi=doi,
                           final_title=p.get("title"), year=p.get("year"),
                           method="s2_doi_fallback",
                           note=(out["note"] + "｜OpenAlex 未果，S2 備援確認").strip("｜"))
                return out
        except Exception:
            pass

    # 404 不自動判 removed（OpenAlex 404 ≠ DOI 無效，書籍章節常見）；一律 unverified 交使用者裁決
    out["status"] = "unverified"
    return out


def _warn_mailto():
    """MAILTO 仍為佔位符時印一行提示（不中斷）。OpenAlex polite pool 為禮貌性建議，非硬性要求。"""
    if MAILTO.startswith("YOUR_EMAIL"):
        print("提示：MAILTO 仍為佔位符，未加入 OpenAlex polite pool（服務品質可能較不穩定，但不影響執行）。"
              "如需設定，請修改你實際安裝的那份 skill 內 scripts/ 三支腳本的 MAILTO 值。", file=sys.stderr)


def main():
    _warn_mailto()
    if len(sys.argv) >= 3 and sys.argv[1] == "--file":
        with open(sys.argv[2], encoding="utf-8") as f:
            items = json.load(f)
    elif len(sys.argv) >= 2:
        items = json.loads(sys.argv[1])
    else:
        print("usage: doi_verify.py '<json-list>' | --file path", file=sys.stderr)
        sys.exit(1)

    results = [verify_one(it) for it in items]
    out = {"env_block_suspected": any("403" in (r.get("note") or "") for r in results),
           "results": results}
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
