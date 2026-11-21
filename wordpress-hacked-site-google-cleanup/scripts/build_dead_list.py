#!/usr/bin/env python3
"""
Build a safe dead-URL list from Search Console exports.

Reads CSV / TSV / TXT / XML sitemap files, finds the URL column, normalises
URLs, drops duplicates, other domains, protected WordPress paths and real
pages, then writes:

  dead-urls.txt   one full URL per line
  dead-urls.csv   numbered list with empty status/notes columns to fill in
  dead-urls.xml   sitemap with <lastmod>
  skipped.csv     every URL that was NOT included, with the reason
  summary.txt     counts

Usage:
  python3 build_dead_list.py export1.csv export2.csv \
      --site https://www.example.com \
      --real-pages real_pages.txt \
      --out-dir out

--real-pages is a text file of real page URLs or paths (one per line). Use it.
A spam list that contains a real page would remove that page from Google.

Standard library only. Python 3.8+.
"""
import argparse
import csv
import html
import io
import os
import re
import sys
from datetime import date
from urllib.parse import quote, unquote, urlsplit
from xml.sax.saxutils import escape

PROTECTED_FIRST = {
    "wp-admin", "wp-login.php", "wp-json", "wp-content", "wp-includes",
    "wp-cron.php", "xmlrpc.php", "robots.txt", "favicon.ico",
    "sitemap.xml", "sitemap_index.xml", "wp-sitemap.xml", "dead-urls.xml",
}
URL_HEADER = re.compile(r"url|address|page|link|loc|path", re.I)
MAX_URLS = 50000


def read_text(path):
    raw = open(path, "rb").read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8-sig", errors="replace")


def extract(text):
    """Return raw URL strings from sitemap XML, CSV/TSV or plain lines."""
    if "<loc>" in text.lower():
        return [html.unescape(m.strip()) for m in re.findall(r"<loc>\s*(.*?)\s*</loc>", text, re.I | re.S)]
    lines = [l for l in re.split(r"\r\n|\r|\n", text) if l.strip()]
    if not lines:
        return []
    first = lines[0]
    delim = next((d for d in ("\t", ",", ";") if d in first), None)
    if delim is None:
        start = 1 if re.fullmatch(r"(url|urls|address|page|pages|link|path)", first.strip(), re.I) else 0
        return [l.strip() for l in lines[start:]]
    rows = list(csv.reader(io.StringIO("\n".join(lines)), delimiter=delim))
    col = None
    for i, h in enumerate(rows[0]):
        if URL_HEADER.search(h or ""):
            col = i
            break
    out = []
    for r in rows[1 if col is not None else 0:]:
        if col is not None:
            if col < len(r):
                out.append(r[col].strip())
        else:
            for c in r:
                if re.match(r"(https?://|/)", c.strip(), re.I):
                    out.append(c.strip())
                    break
    return out


def site_parts(site):
    p = urlsplit(site if "//" in site else "https://" + site)
    host = (p.hostname or "").lower()
    return p.scheme or "https", host, re.sub(r"^www\.", "", host)


def to_path(raw, bare_host):
    """Return (path, host) where path is decoded, lower-case, no slashes at the ends."""
    raw = raw.strip().strip("\"'<>")
    host = None
    if re.match(r"(https?:)?//", raw, re.I):
        p = urlsplit(raw if not raw.startswith("//") else "https:" + raw)
        host = (p.hostname or "").lower()
        raw = p.path
    elif raw and not raw.startswith("/") and "/" in raw:
        first = raw.split("/", 1)[0].lower()
        if re.fullmatch(r"(www\.)?([a-z0-9-]+\.)+[a-z]{2,}", first):
            host = first
            raw = raw[len(first):]
    raw = raw.split("#", 1)[0].split("?", 1)[0]
    path = unquote(raw).lower()
    path = re.sub(r"/+", "/", path).strip("/ \t")
    return path, host


def load_real(path, bare_host):
    real = set()
    if not path:
        return real
    for line in read_text(path).splitlines():
        line = line.strip()
        if line:
            p, _ = to_path(line, bare_host)
            if p:
                real.add(p)
    return real


def full_url(scheme, host, path):
    enc = "/".join(quote(seg, safe="") for seg in path.split("/"))
    return f"{scheme}://{host}/{enc}/"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="Search Console exports (csv/tsv/txt/xml)")
    ap.add_argument("--site", required=True, help="Canonical site URL, e.g. https://www.example.com")
    ap.add_argument("--real-pages", help="Text file of real page URLs/paths to exclude")
    ap.add_argument("--out-dir", default="out")
    ap.add_argument("--lastmod", default=date.today().isoformat(), help="lastmod date for the sitemap (YYYY-MM-DD)")
    args = ap.parse_args()

    scheme, host, bare = site_parts(args.site)
    if not host:
        sys.exit("Could not read the site host from --site")
    real = load_real(args.real_pages, bare)
    if not args.real_pages:
        print("WARNING: no --real-pages file. Real pages cannot be excluded. Review the output by hand.", file=sys.stderr)

    raws = []
    for f in args.inputs:
        raws.extend(extract(read_text(f)))

    kept, skipped, seen = [], [], set()
    for raw in raws:
        path, h = to_path(raw, bare)
        if h and re.sub(r"^www\.", "", h) != bare:
            skipped.append((raw, "other domain"))
        elif not path:
            skipped.append((raw, "homepage or empty"))
        elif re.search(r"[\x00-\x1f\x7f]", path) or len(path) > 2000:
            skipped.append((raw, "invalid"))
        elif path in seen:
            skipped.append((raw, "duplicate"))
        elif path.split("/")[0] in PROTECTED_FIRST:
            skipped.append((raw, "protected WordPress path"))
        elif path in real:
            skipped.append((raw, "real page"))
        else:
            seen.add(path)
            kept.append(path)

    if len(kept) > MAX_URLS:
        skipped.extend((p, "over 50,000 per sitemap file") for p in kept[MAX_URLS:])
        kept = kept[:MAX_URLS]

    os.makedirs(args.out_dir, exist_ok=True)
    urls = [full_url(scheme, host, p) for p in kept]
    with open(os.path.join(args.out_dir, "dead-urls.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(urls) + ("\n" if urls else ""))
    with open(os.path.join(args.out_dir, "dead-urls.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["#", "URL", "HTTP status (fill in)", "Notes"])
        for i, u in enumerate(urls, 1):
            w.writerow([i, u, "", ""])
    with open(os.path.join(args.out_dir, "dead-urls.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"<url><loc>{escape(u)}</loc><lastmod>{args.lastmod}</lastmod></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(args.out_dir, "skipped.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Input", "Reason"])
        w.writerows(skipped)

    counts = {}
    for _, reason in skipped:
        counts[reason] = counts.get(reason, 0) + 1
    lines = [
        f"Input rows read:        {len(raws)}",
        f"Included (dead list):   {len(urls)}",
        f"Skipped:                {len(skipped)}",
    ] + [f"  - {k}: {v}" for k, v in sorted(counts.items())]
    summary = "\n".join(lines)
    open(os.path.join(args.out_dir, "summary.txt"), "w", encoding="utf-8").write(summary + "\n")
    print(summary)
    if counts.get("real page"):
        print("\nReal pages were found in your export and excluded. Check skipped.csv.")


if __name__ == "__main__":
    main()
