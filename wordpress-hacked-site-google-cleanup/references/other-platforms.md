# Other platforms (short note)

The Google side of this skill (410 vs redirect vs robots.txt, the dead-URL sitemap, Search Console exports, Removals, monitoring) is the same for any website. Only *how you return a 410* differs. The WordPress plugin does not apply elsewhere. This has not been tested outside WordPress.

| Platform | Way to return 410 |
|---|---|
| Apache | `Redirect gone /path` or `RewriteRule ^path/?$ - [G]` in `.htaccess` |
| Nginx | `location = /path/ { return 410; }` (use a `map` for long lists) |
| Cloudflare / CDN | A rule or Worker that returns status 410 for a list of paths |
| Shopify | Native 410 is limited; the nearest option is a 404 (delete the page/product) |
| Joomla / Drupal / Magento / custom | Use a redirect/error manager that supports 410, or a server rule |

Rules:
- Match **exact paths** and test that real pages still load.
- Do not redirect spam URLs to the homepage.
- Do not block them in `robots.txt`.
- Build the list and sitemap with `scripts/build_dead_list.py`, and test with `scripts/check_status.py`; both are platform-independent.
