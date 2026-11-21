# Search Console: what to use and how

## Export the spam URLs
- **Indexing → Pages**: choose the *Indexed* list. Tick **Unsubmitted pages only** to exclude your real sitemap. Click **Export** (CSV/Sheets). Each export is capped at **1,000 rows**; to get more, filter (for example by a sitemap or by a reason such as "Not found") and export again, or use the Search Console API.
- **Performance → Pages**: spam URLs that already get impressions. Set a long date range.
- **Pages report → a specific reason** (e.g. "Crawled – currently not indexed", "Not found (404)") shows more URLs Google knows about.
- Search `site:example.com casino` (and other spam words) in Google to spot patterns. Do not rely on it for counts.

Exports include a URL column and sometimes a last-crawled date. The helper script `scripts/build_dead_list.py` finds the right column automatically.

## Submit the dead-URL sitemap
- **Sitemaps → Add a new sitemap → `dead-urls.xml` → Submit.**
- Each URL should have an accurate `<lastmod>`. To ask for a fresh recrawl later, change the lastmod and **resubmit the same path**.
- Status "Success" and "Discovered pages" matching your list size means Google read it.
- Remove the sitemap from Search Console after about 3–4 weeks.

## Removals tool (optional, temporary)
- **Removals → New request → Temporarily remove URL.**
- Use **Remove this URL only**, one URL at a time, for the most visible spam.
- **Never** use "Remove all URLs with this prefix" with a short prefix (for example the site root): it can hide your real pages.
- It hides results for about 6 months. It does not delete anything; the 410 does the real work.

## URL Inspection
- Use **Inspect any URL** on a few spam URLs to see "Page fetch" and the last crawl date.
- **Test live URL** shows what Google gets right now (should be 404/410 "Not found").
- Do not click **Request indexing** on a spam URL.

## Other checks
- **Security & Manual actions → Security issues / Manual actions**: if there is a hacked-content warning, fix the site, then use **Request review**.
- **Settings → Crawl stats**: shows crawl requests by response. After the sitemap, expect "Not found (404)" requests to rise; 5xx should stay low.

## Reading the Pages report
- "Indexed" should fall over weeks.
- "Not found (404)" should rise as spam URLs are recrawled (410s are counted here).
- Spikes in "Server error (5xx)" need attention (see `troubleshooting.md`).
