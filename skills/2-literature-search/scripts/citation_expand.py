#!/usr/bin/env python3
"""
citation_expand.py — literature-search 雙向引用網絡擴展腳本

職責：
- Forward（後輩引用）：OpenAlex /works?filter=cites:{id}&sort=cited_by_count:desc&per_page=50 → 取前 20
- Backward（前輩參考）：OpenAlex /works/{id} 的 referenced_works（**僅取前 80 條**）→ 批次 lookup → 按 cited_by_count 降序取前 20（refs>80 的長書目有截斷，屬已知盲點）
- 備援：OpenAlex 端點失敗 → S2 /paper/{id}/citations 或 /references，取 top50 → 按 citationCount 降序保留前 20
- abstract 還原：OpenAlex 回 abstract_inverted_index 倒排索引 → 還原為文字
- 內建 rate limit（OpenAlex 0.5s；S2 1.1s；S2 429 指數退避 2→30s，最多 5 次）

每篇捕獲論文輸出 provenance 欄位（apiSource、apiVersion、queryTimestamp、searchQuery、rankInfo）。

呼叫方式：
    python3 citation_expand.py <seed_doi_or_workid> [--direction forward|backward|both] [--top 20]

輸出（stdout，JSON）：候選論文清單，每筆含
    doi,title,authors,year,venue,citationCount,abstract,source,provenance{...}

設計原則：只負責 API 呼叫與 JSON 輸出，不寫工作區檔案。單次處理 1 顆種子的單方向，
避免 45 秒 bash timeout；both 方向且 backward references 多時，建議改逐方向呼叫。
"""
import sys, json, time, datetime, urllib.parse, urllib.request, urllib.error

OPENALEX = "https://api.openalex.org"
S2 = "https://api.semanticscholar.org/graph/v1"

# 請改為你自己的 email：OpenAlex／Semantic Scholar API 的 polite pool 用途
# （附上聯絡 email 可取得較高速率限制、較穩定的服務）需要換成你自己真實可用的信箱。
MAILTO = "YOUR_EMAIL@example.com"
OA_DELAY = 0.5
S2_DELAY = 1.1
TIMEOUT = 30


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url, timeout=TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": f"litsearch/1.0 (mailto:{MAILTO})"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _s2_get(url, timeout=TIMEOUT, max_retry=5):
    """S2 含 429 指數退避 2→30 秒。"""
    backoff = 2
    for _ in range(max_retry):
        try:
            return _get(url, timeout)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(min(backoff, 30))
                backoff *= 2
                continue
            raise
    raise RuntimeError("S2 429 retries exhausted")


def reconstruct_abstract(inverted_index):
    """OpenAlex abstract_inverted_index → 文字。"""
    if not inverted_index:
        return None
    pos = {}
    for word, positions in inverted_index.items():
        for p in positions:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos.keys()))


def _oa_work_brief(w, source, rank_info, query):
    return {
        "openAlexId": w.get("id", "").replace("https://openalex.org/", ""),
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "title": w.get("title") or w.get("display_name"),
        "authors": [a.get("author", {}).get("display_name") for a in w.get("authorships", [])][:10],
        "year": w.get("publication_year"),
        "venue": (w.get("primary_location") or {}).get("source", {} ).get("display_name")
                 if w.get("primary_location") else None,
        "citationCount": w.get("cited_by_count"),
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "source": source,
        "provenance": {"apiSource": "openalex", "apiVersion": "stable",
                       "queryTimestamp": _now(), "searchQuery": query, "rankInfo": rank_info},
    }


def resolve_workid(seed):
    """接受 DOI 或 OpenAlex work id（W...）。回傳 (work_id, work_obj)。"""
    if seed.upper().startswith("W"):
        url = f"{OPENALEX}/works/{seed}?mailto={MAILTO}"
    else:
        url = f"{OPENALEX}/works/doi:{urllib.parse.quote(seed)}?mailto={MAILTO}"
    w = _get(url)
    return w.get("id", "").replace("https://openalex.org/", ""), w


def forward_oa(work_id, top):
    q = (f"{OPENALEX}/works?filter=cites:{work_id}&sort=cited_by_count:desc"
         f"&per_page=50&mailto={MAILTO}")
    results = _get(q).get("results", [])
    out = []
    for i, w in enumerate(results[:top]):
        out.append(_oa_work_brief(w, f"seed:{work_id}:fwd", f"{i+1}", q))
    time.sleep(OA_DELAY)
    return out


def backward_oa(work_obj, top):
    refs = work_obj.get("referenced_works", [])[:80]
    if not refs:
        return []
    # 批次 lookup：OpenAlex 支援 filter=openalex_id:W1|W2|...
    works = []
    for chunk_start in range(0, len(refs), 25):
        chunk = refs[chunk_start:chunk_start + 25]
        ids = "|".join(c.replace("https://openalex.org/", "") for c in chunk)
        q = (f"{OPENALEX}/works?filter=openalex_id:{ids}"
             f"&per_page=25&mailto={MAILTO}")
        works.extend(_get(q).get("results", []))
        time.sleep(OA_DELAY)
    works.sort(key=lambda w: w.get("cited_by_count", 0), reverse=True)
    seed_id = work_obj.get("id", "").replace("https://openalex.org/", "")
    return [_oa_work_brief(w, f"seed:{seed_id}:bwd", f"{i+1}", "referenced_works batch")
            for i, w in enumerate(works[:top])]


def s2_fallback(seed, kind, top):
    """kind ∈ citations | references。"""
    pid = f"DOI:{seed}" if not seed.upper().startswith("W") else seed
    fields = "title,year,venue,citationCount,externalIds,abstract,authors"
    url = (f"{S2}/paper/{urllib.parse.quote(pid)}/{kind}"
           f"?fields={fields}&limit=50")
    data = _s2_get(url).get("data", [])
    key = "citingPaper" if kind == "citations" else "citedPaper"
    papers = [d.get(key, {}) for d in data]
    papers.sort(key=lambda p: p.get("citationCount", 0) or 0, reverse=True)
    out = []
    tag = "fwd" if kind == "citations" else "bwd"
    for i, p in enumerate(papers[:top]):
        out.append({
            "doi": (p.get("externalIds") or {}).get("DOI"),
            "title": p.get("title"), "year": p.get("year"),
            "authors": [a.get("name") for a in (p.get("authors") or [])][:10],
            "venue": p.get("venue"), "citationCount": p.get("citationCount"),
            "abstract": p.get("abstract"),
            "source": f"seed:{seed}:{tag}",
            "provenance": {"apiSource": "semantic_scholar", "apiVersion": "graph/v1",
                           "queryTimestamp": _now(), "searchQuery": url, "rankInfo": f"{i+1}"},
        })
    time.sleep(S2_DELAY)
    return out


def _warn_mailto():
    """MAILTO 仍為佔位符時印一行提示（不中斷）。OpenAlex polite pool 為禮貌性建議，非硬性要求。"""
    if MAILTO.startswith("YOUR_EMAIL"):
        print("提示：MAILTO 仍為佔位符，未加入 OpenAlex polite pool（服務品質可能較不穩定，但不影響執行）。"
              "如需設定，請修改你實際安裝的那份 skill 內 scripts/ 三支腳本的 MAILTO 值。", file=sys.stderr)


def main():
    _warn_mailto()
    if len(sys.argv) < 2:
        print("usage: citation_expand.py <seed_doi_or_workid> [--direction forward|backward|both] [--top N]",
              file=sys.stderr)
        sys.exit(1)
    seed = sys.argv[1]
    direction = "both"
    top = 20
    if "--direction" in sys.argv:
        direction = sys.argv[sys.argv.index("--direction") + 1]
    if "--top" in sys.argv:
        top = int(sys.argv[sys.argv.index("--top") + 1])

    out = {"seed": seed, "forward": [], "backward": [], "degraded": []}
    try:
        work_id, work_obj = resolve_workid(seed)
    except Exception as e:
        print(json.dumps({"error": f"resolve seed failed: {e}", "seed": seed,
                          "env_block_suspected": "403" in str(e)}, ensure_ascii=False))
        sys.exit(2)

    if direction in ("forward", "both"):
        try:
            out["forward"] = forward_oa(work_id, top)
        except Exception as e:
            out["degraded"].append({"direction": "forward", "from": "openalex", "to": "s2", "reason": str(e)})
            try:
                out["forward"] = s2_fallback(seed, "citations", top)
            except Exception as e2:
                out["degraded"].append({"direction": "forward", "fatal": str(e2)})

    if direction in ("backward", "both"):
        try:
            out["backward"] = backward_oa(work_obj, top)
            if not out["backward"]:
                raise RuntimeError("referenced_works 為空")
        except Exception as e:
            out["degraded"].append({"direction": "backward", "from": "openalex", "to": "s2", "reason": str(e)})
            try:
                out["backward"] = s2_fallback(seed, "references", top)
            except Exception as e2:
                out["degraded"].append({"direction": "backward", "fatal": str(e2)})

    # 環境阻擋顯性化：degraded 原因含 403 即標旗，供 SKILL 辨別環境阻擋 vs 真零結果
    out["env_block_suspected"] = any(
        "403" in str(d.get("reason", "")) or "403" in str(d.get("fatal", ""))
        for d in out["degraded"])
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
