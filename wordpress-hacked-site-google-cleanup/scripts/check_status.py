#!/usr/bin/env python3
"""
Check what HTTP status each URL returns. Spam URLs should return 410.

Usage:
  python3 check_status.py dead-urls.txt --out results.csv [--workers 4] [--delay 0.2]

Run it from your own computer. Do not hammer a client's server: the defaults
are gentle. A hosting firewall may block bulk requests (403/429/503); that does
not mean Google is blocked, so open a few URLs in a private browser window.

Redirects are NOT followed, because a redirect is a problem for this job.
Standard library only. Python 3.8+.
"""
import argparse
import csv
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

CHALLENGE = re.compile(r"One moment, please|captcha|cf-chl|challenge-platform|Just a moment|imunify|bot verification", re.I)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)


def check(url, delay, timeout):
    time.sleep(delay)
    req = urllib.request.Request(url, headers={"User-Agent": "dead-url-status-check/1.0"})
    try:
        with OPENER.open(req, timeout=timeout) as r:
            code, body, loc = r.status, r.read(8192).decode("utf-8", "replace"), ""
    except urllib.error.HTTPError as e:
        code = e.code
        loc = e.headers.get("Location", "") if e.headers else ""
        try:
            body = e.read(8192).decode("utf-8", "replace")
        except Exception:
            body = ""
    except Exception as e:  # timeouts, DNS, TLS
        return url, 0, "error: %s" % e

    if code == 410:
        return url, code, "OK"
    if 300 <= code < 400:
        return url, code, "redirects to %s (Google keeps redirected URLs)" % (loc or "?")
    if code in (403, 429, 503) or (code == 200 and CHALLENGE.search(body)):
        return url, code, "blocked by host (firewall or bot check): check in a browser"
    if code == 404:
        return url, code, "404, not 410 (works, but slower; check cache or server rule)"
    if code == 200:
        return url, code, "page loads (200): cached copy or a real page"
    return url, code, "unexpected status"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", help="Text file, one URL per line")
    ap.add_argument("--out", default="results.csv")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--delay", type=float, default=0.2, help="seconds to wait before each request")
    ap.add_argument("--timeout", type=float, default=15)
    args = ap.parse_args()

    urls = [l.strip() for l in open(args.urls, encoding="utf-8-sig") if l.strip()]
    if not urls:
        sys.exit("No URLs found")
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 10))) as ex:
        results = list(ex.map(lambda u: check(u, args.delay, args.timeout), urls))

    with open(args.out, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["URL", "Status", "Note"])
        w.writerows(results)

    tally = {}
    for _, code, note in results:
        key = "410 OK" if code == 410 else ("blocked by host" if note.startswith("blocked") else "issue (%s)" % code)
        tally[key] = tally.get(key, 0) + 1
    print("Tested %d URLs" % len(results))
    for k, v in sorted(tally.items()):
        print("  %-22s %d" % (k, v))
    print("Details: %s" % args.out)


if __name__ == "__main__":
    main()
