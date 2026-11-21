# Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| URL returns 200 | Cached page (plugin cache, CDN, server cache), or a real page now exists | Purge all caches and the CDN; check that the URL is not a real page |
| URL returns 404, not 410 | The 410 rule is not reached (cache or server rule answers first) | Purge caches; check server rules; 404 still works but is slower |
| URL returns 301/302 | A redirect plugin, theme, `.htaccess` or SEO plugin redirects it | Remove the redirect. Redirects keep spam alive |
| Tests show 403/429/503 | Hosting firewall blocks the server's own test requests | Open a few URLs in a private browser window. Not proof Google is blocked |
| Googlebot never visits | Sitemap not read, host blocks Googlebot, or IP header is wrong behind a proxy | Check Sitemaps status; check the firewall allows Googlebot; set the correct IP source |
| Real page caught by a rule | Pattern too broad | Delete or narrow the rule; real-page guard should win; request recrawl of the real page |
| 5xx spike in Search Console | Server overload from crawling, or a broken plugin | Check server logs and PHP errors; ask the host; slow down by not resubmitting repeatedly |
| Indexed count goes up | Google found more spam URLs | Export again and add them |
| Spam returns after cleanup | Site still compromised, or a backdoor remains | Re-scan; check mu-plugins, drop-ins in `wp-content`, `.htaccess`, `wp-config.php`, cron jobs, admin users |
| Spam URLs have no real pages behind them (fake posts) | Injected posts or a rewrite rule serve them | Look for unknown posts/users and rewrite rules; delete the content |
| Test posts or odd slugs appear in the export | Leftover test content, or injected | Search Posts/Pages (including drafts, trash) and the database |
| URL in Google shows a cached snippet after 410 | Google has not recrawled yet | Wait. Use Removals only for the most visible URLs |

## Checks that avoid false alarms
- Compare **status codes from your own computer** with what the plugin tester says. The server's own requests can be blocked or cached differently.
- Test with a normal browser user agent and with a Googlebot-like request only to see differences; remember real Googlebot is verified by IP.
- After a change, wait for the cache to clear before concluding it failed.
