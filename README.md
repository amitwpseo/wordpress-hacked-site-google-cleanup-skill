<div align="center">

# WordPress Hacked-Site Google Cleanup (AI Skill)

**A playbook any AI can follow to get hacked-site spam out of Google, and to prove it to the client.**

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![Works with](https://img.shields.io/badge/works%20with-Claude%20%7C%20ChatGPT%20%7C%20Gemini%20%7C%20any%20AI-2563eb?style=flat-square)
![Scope](https://img.shields.io/badge/scope-WordPress-21759b?style=flat-square)

</div>

> [!IMPORTANT]
> This skill cleans up **Google's index** after a hack. It does **not** remove malware. Clean the site first (the skill includes a checklist).

## What it does

After a WordPress hack (casino, pharma, Japanese keyword spam, doorway pages), thousands of spam URLs can stay in Google for months. This skill walks an AI assistant, and you, through the whole job:

1. **Check the site is clean** (checklist).
2. **Collect the spam URLs** from Search Console and other sources.
3. **Build a safe dead-URL list** that never includes real pages (script included).
4. **Serve 410 Gone** (companion plugin, or server rules).
5. **Verify** every URL really returns 410 (script included).
6. **Tell Google**: dead-URL sitemap, Removals tool, what *not* to do.
7. **Monitor** Search Console and know what is normal.
8. **Report to the client** in plain language (templates included).

## What's inside

```
wordpress-hacked-site-google-cleanup/
├── SKILL.md                     # the workflow and ground rules
├── scripts/
│   ├── build_dead_list.py       # exports → safe dead list + sitemap (stdlib only)
│   └── check_status.py          # test that URLs return 410 (stdlib only)
├── references/
│   ├── why-410.md               # 410 vs 404 vs redirect vs robots.txt
│   ├── search-console-guide.md  # exports, sitemaps, removals, inspection
│   ├── monitoring.md            # what to track, what is normal
│   ├── troubleshooting.md       # symptoms → fixes
│   ├── site-cleanup-checklist.md
│   └── other-platforms.md       # short note for non-WordPress sites
└── templates/
    └── client-updates.md        # four client message templates
```

## How to use it

**Claude (skills):** zip the `wordpress-hacked-site-google-cleanup` folder and add it under *Customize → Skills*, or place the folder in your skills directory. Then ask, for example: *"Help me clean up Google after my WordPress site was hacked. Here is my Search Console export."*

**ChatGPT, Gemini or any other AI:** the skill is plain Markdown and Python.
- Paste `SKILL.md` as the instructions (system prompt, custom GPT, Gem or project instructions) and upload the `references/` and `templates/` files as knowledge.
- If the AI can run code, give it the `scripts/` folder. If not, run the scripts yourself and paste the results.

**By hand:** read `SKILL.md` and follow the steps. The scripts need only Python 3.8+.

```bash
# 1. Build the dead list from your Search Console exports
python3 scripts/build_dead_list.py export1.csv export2.csv \
    --site https://www.example.com --real-pages real_pages.txt --out-dir out

# 2. Check they return 410 (run from your own computer, gently)
python3 scripts/check_status.py out/dead-urls.txt --out results.csv
```

## Companion plugin

To actually serve the 410s, a dead-URL sitemap, pattern rules, a 404 monitor and client reports, use the free plugin
[**Hacked Site Index Cleaner**](https://github.com/amitwpseo/hacked-site-index-cleaner). The skill also explains how to do it with server rules instead.

## Ground rules built into the skill

- Audit and advise by default; no changes to a live site or Search Console without the user's say-so.
- No invented numbers; report only what the data shows, with its date.
- Honest timing: weeks, not days.
- Client data stays out of public places.

## Limits

- It is instructions and scripts. It cannot log in to Search Console or a website on its own.
- Written from WordPress experience. The Google-side advice applies to any site, but the 410 steps for other platforms are untested (see `other-platforms.md`).
- Results depend on Google. Nothing here guarantees a removal date.

## Contributing

Issues and pull requests are welcome, especially real-world troubleshooting cases (with client details removed).

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">

Built by [**BLSS – Best Local SEO Services & Development**](https://bestlocalseoservices.com/)

</div>
