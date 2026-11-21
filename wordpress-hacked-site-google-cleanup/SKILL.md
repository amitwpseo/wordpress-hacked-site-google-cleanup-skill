---
name: wordpress-hacked-site-google-cleanup
description: Clean up Google's index after a WordPress hack (casino, pharma, Japanese keyword spam, doorway pages). Use when a user has thousands of spam URLs indexed, wants them removed from Google, needs a dead-URL list or sitemap, wants to verify 410 responses, monitor Search Console progress, or write a client update or progress report. Covers 410 vs 404 vs redirects, Search Console exports and Removals, monitoring, troubleshooting and client communication. Does not remove malware.
---

# WordPress hacked-site Google cleanup

Get injected spam URLs out of Google after a WordPress hack, and show the client proof that it is working.

This skill is about **Google's index**, not malware removal. A site that is still infected will keep producing spam, so the cleanup comes first (step 0).

## Ground rules for the AI

1. **Audit and advise by default.** Read data, explain, draft files and messages. Do not change the live site, run commands on it, or submit anything in Search Console unless the user clearly asks for that action.
2. **Never invent numbers.** Report only what the user's exports, screenshots or tools show, with the date of the data.
3. **Keep client data out of public places.** If the user will publish anything (a repo, a post), remove client names, domains, URLs and counts first.
4. **Be honest about timing.** Google decides when it recrawls. Expect weeks, not days. Never promise a date.
5. **Say what you could not verify.** If you could not test on a real site, say so.

## The workflow

### 0. Make sure the site is clean
Do not start de-indexing while the hack is still active. Check `references/site-cleanup-checklist.md` with the user: malware scan, rogue admin users, unknown plugins and mu-plugins, modified core files, `.htaccess`, `wp-config.php`, updates, password and salt rotation, and Search Console **Security issues** and **Manual actions**.

### 1. Collect the spam URLs
Sources, best first:
- Search Console **Indexing → Pages**: tick *Unsubmitted pages only*, open the *Indexed* list, **Export** (1,000-row cap per export; repeat with filters to get more).
- Search Console **Performance → Pages** export (spam that already gets impressions).
- The 404 Monitor in the companion plugin (below), server logs, and `site:example.com casino` style Google searches for patterns.
- Patterns: note shared prefixes, odd languages, long hyphenated slugs, `/?s=` search URLs.

Details and tips: `references/search-console-guide.md`.

### 2. Build the dead list safely
Use `scripts/build_dead_list.py`. It reads Search Console exports (CSV, TSV, XML, TXT, UTF-16), normalises URLs, removes duplicates and other domains, protects system paths, **excludes real pages** (from a list of real slugs the user provides) and writes `dead-urls.txt`, `.csv`, `.xml` (with `<lastmod>`) and a summary.

Always ask for or build the list of real pages first (all published posts, pages, products). A spam list that contains a real page would take that page out of Google.

### 3. Serve 410 Gone for those URLs
Use the free plugin **Hacked Site Index Cleaner** (https://github.com/amitwpseo/hacked-site-index-cleaner): 410 + `noindex`, a dead-URL sitemap, pattern rules, 404 monitor, search-spam protection, verified Googlebot tracking, weekly re-test with alerts, and a client report. Alternatives (server rules, other CMSs): `references/other-platforms.md`.

Why 410 and never a redirect or robots.txt: `references/why-410.md`.

### 4. Verify
- Test every URL returns **410** (plugin tester or `scripts/check_status.py`).
- Open 3 spam URLs and 2 real pages in a private window.
- Make sure no cache or CDN serves the old page. See `references/troubleshooting.md`.

### 5. Tell Google
- Search Console → **Sitemaps** → submit `dead-urls.xml`. To refresh later, resubmit the same path.
- Optionally use **Removals → New request → Remove this URL only** for the most visible spam URLs. It hides for about 6 months; it does not delete. Never use a short prefix such as the site root.
- Do **not** block the URLs in `robots.txt`.

### 6. Monitor
Weekly, record: Indexed pages, Not found (404), 5xx, pages from the dead-URL sitemap, and verified Googlebot revisits. See `references/monitoring.md` for what to read, what is normal and when to worry.

### 7. Report to the client
Plain language, honest, no jargon, no secrets. Use `templates/client-updates.md`. The plugin can also produce a one-page report. Keep a short list of what is still open.

### 8. Wrap up (after about 3–4 weeks)
Remove `dead-urls.xml` from Search Console. Keep the 410 rules active as long as the URLs should stay gone. If the plugin is deleted, the URLs fall back to 404, which still works but slower.

## When something looks wrong
`references/troubleshooting.md` covers: URLs not returning 410, hosting firewall blocking tests, real page caught by a rule, 5xx spikes, Googlebot not visiting, counts going up, and spam coming back.

## Files
| File | Use |
|---|---|
| `scripts/build_dead_list.py` | Build the safe dead-URL list and sitemap from exports |
| `scripts/check_status.py` | Test that URLs return 410 (run from your own machine) |
| `references/why-410.md` | 410 vs 404 vs redirect vs robots.txt |
| `references/search-console-guide.md` | Exports, Sitemaps, Removals, URL Inspection |
| `references/monitoring.md` | What to track and how to read it |
| `references/troubleshooting.md` | Common problems and fixes |
| `references/site-cleanup-checklist.md` | Step 0 checklist |
| `references/other-platforms.md` | Non-WordPress sites |
| `templates/client-updates.md` | Client message templates |
