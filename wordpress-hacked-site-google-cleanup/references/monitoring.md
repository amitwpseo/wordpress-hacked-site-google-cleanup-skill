# Monitoring progress

## What to record each week
| Metric | Where | Healthy direction |
|---|---|---|
| Indexed pages | Indexing → Pages | Down |
| Not found (404) | Indexing → Pages | Up while Google recrawls spam URLs |
| Server error (5xx) | Indexing → Pages | Flat or low |
| Pages from the dead-URL sitemap: indexed vs not indexed | Pages → filter by the sitemap | Indexed down, not indexed up |
| Googlebot revisits of the list | Plugin dashboard, or server logs | Up |
| Real pages still indexed | URL Inspection on key pages | Unchanged |

Always note the **date of the data**. Search Console reports lag a few days.

## What is normal
- Revisits of the list usually start within hours to days after the sitemap is submitted, then continue over weeks.
- Large lists (thousands of URLs) usually take **several weeks** to clear. Google decides the pace.
- Counts can move in steps, and "Indexed" can go up briefly if Google discovers more spam URLs. Keep adding them.

## Example (one cleanup, illustrative only)
A site with about 2,300 spam URLs: the first verified Googlebot revisits arrived within minutes of resubmitting the sitemap; over about a week "Indexed" fell from roughly 2.8k to 2.3k while "Not found (404)" rose from several hundred to over a thousand. Your numbers will differ.

## When to worry
- Real pages dropping out of the index: stop, check the rules for a pattern that is too broad, restore.
- No revisits after about a week: check the sitemap status, that URLs return 410 to Googlebot, and that the host is not blocking Googlebot.
- 5xx rising: the server may be struggling with crawl load or spam; see `troubleshooting.md`.
- New spam appearing: the site is probably still compromised. Go back to step 0.

## Verified Googlebot
A hit counts as Googlebot only if the user agent claims it **and** the IP passes a reverse DNS lookup to `googlebot.com` / `google.com` and a forward lookup back to the same IP. Anything else is an imitation. Behind Cloudflare or a proxy, the real client IP must be read from the correct header.
