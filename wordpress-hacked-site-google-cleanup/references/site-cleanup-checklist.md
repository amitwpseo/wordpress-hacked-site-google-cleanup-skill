# Step 0: clean the site first

This skill does not remove malware. Confirm these with the user before de-indexing:

- [ ] Full malware scan done (a security plugin and, ideally, a server-side scan). Infected files cleaned or replaced from clean copies.
- [ ] WordPress core, themes and plugins updated; unused ones deleted. Nulled/pirated plugins removed.
- [ ] Unknown administrator users removed; user roles reviewed.
- [ ] Passwords changed for WordPress admins, hosting, FTP/SFTP, database. Salts in `wp-config.php` regenerated.
- [ ] Unknown files checked: `wp-content/mu-plugins/`, drop-ins in `wp-content/` (for example `maintenance.php`, `advanced-cache.php`, `object-cache.php` that you did not install), `.htaccess`, `wp-config.php`, `index.php` files in odd places, files in `uploads/` with `.php` extension.
- [ ] Scheduled tasks (WP-Cron) and the database reviewed for injected options, posts, and rewrite rules.
- [ ] Two-factor login on admin accounts. File editing disabled where possible.
- [ ] Backups: a clean backup exists before and after cleanup.
- [ ] Search Console: **Security issues** and **Manual actions** reviewed. If a hacked-content issue exists, fix it, then **Request review**.
- [ ] The spam pages no longer exist as real content (so a 410 is truthful).

If the hack is still active, de-indexing will not hold. Fix that first.
