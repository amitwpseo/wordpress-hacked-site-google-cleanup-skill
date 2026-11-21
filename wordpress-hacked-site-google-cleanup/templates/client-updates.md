# Client update templates

Rules: plain language, honest, no jargon, no credentials, no blame. State what was done, what the numbers say (with the date), what is next and what is still open. Never promise dates. Fill the [brackets].

---

## 1. First update (just after starting)

Subject: Search cleanup: what we did and what to expect

Hi [Name],

Quick update on removing the spam pages left behind by the hack.

What we did
- Collected [N] spam addresses that Google had stored for your website.
- Set each one to tell Google clearly that the page is permanently gone.
- Gave Google a list of those addresses so it comes back and checks them sooner.

What to expect
Google decides when it rechecks each page. With this many addresses it usually takes several weeks. You may still see some spam in Google during that time.

Your real pages are not affected. We checked them separately.

I'll send another update in [a week / two weeks].

[Your name]

---

## 2. Progress update

Subject: Search cleanup progress ([date])

Hi [Name],

Progress as of [data date]:
- Spam addresses on the cleanup list: [N]
- Google has revisited: [X] of them ([P]%)
- Pages Google still shows for the site: [before] → [now]

What this means: Google is working through the list. Each page it rechecks and finds gone is removed from search results. This is on track / slower than expected because [reason].

Next: we keep monitoring and add any new spam addresses we find.
Still open on our side: [list].

[Your name]

---

## 3. Technical update (for a technical contact)

Subject: Technical status: hacked-URL de-indexing ([date])

- Spam URLs served 410 Gone with `X-Robots-Tag: noindex`: [N] (verified [N] OK, [N] issues).
- `dead-urls.xml` submitted [date], [N] discovered pages, last read [date].
- Search Console ([data date]): Indexed [a]→[b]; Not found (404) [c]→[d]; 5xx [e]→[f].
- Verified Googlebot revisits: [X]/[N] ([P]%).
- Open items: [list, e.g. plugin removal, server file review, 2FA].
- Next: re-export Pages report on [date], add new spam URLs, remove the sitemap after [date].

---

## 4. Wrap-up

Subject: Search cleanup: completed

Hi [Name],

The spam pages are now out of Google (or: [P]% are out and the rest are being rechecked). We removed the temporary list we had given Google. The removal rules stay active so the addresses stay gone.

To keep the site safe: [updates, 2FA, backups, monitoring]. Tell me if you see spam results again.

[Your name]
