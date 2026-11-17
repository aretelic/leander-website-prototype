# Leander Swimming Club: website prototype

A clickable prototype of Leander's new website in the **"Open water"** design direction, made so the committee can click through the full structure and copy and give feedback. **It is not the live site.** The real site will be built in Squarespace, with TeamUnify as the members' system.

- 37 pages covering the v1 sitemap: Home, Learn to Swim, Squads, Swim for Life, Galas, Club, News and Join us.
- Plain HTML, CSS and JavaScript. GitHub Pages serves the committed HTML, with no build step.
- `noindex` on every page and a `robots.txt` that blocks search engines.

## What reviewers will see

- **Yellow dashed `TBC` labels** mark facts the club still needs to confirm. There are about 650 of them.
- **"Placeholder photo"** labels sit on the free Unsplash images, with a short brief under each one describing the real photo we need. See [CREDITS.md](CREDITS.md).
- Links to systems outside the prototype (TeamUnify, the kit shop, policy documents) show a short "on the live site this goes to…" message.
- The forms (waiting list, squad trial) look real but **send nothing**.
- **Race the Standards** is embedded from its own site: https://aretelic.github.io/race-the-standards/
- No swimmers under 18 are named anywhere. Historic and record-holding swimmers are shown as `TBC: name withheld` until consent is checked.

## How to update it

The words live in Markdown files in `content/`, one per page. Each one starts with a short header (title, URL, description).

1. Edit the page in `content/` (for example `content/learn/academy.md`).
   - Mark anything unconfirmed as `{{TBC: what's needed}}`.
   - Add a photo with `[PHOTO: short description of the shot]`. The script picks a matching placeholder.
   - Link to another page with `[Label](/squads/pathway)`, or add a button on its own line: `**[Book a squad trial]** → /squads/book-a-trial#trial-form`.
2. Rebuild the HTML (needs Python 3, nothing to install):
   ```bash
   python3 tools/build.py
   ```
3. Preview it locally at http://localhost:8000:
   ```bash
   python3 -m http.server 8000
   ```
4. Commit and push. GitHub Pages updates within a minute or two.

Some pages and parts of pages are built in code rather than Markdown:

| What | Where |
|---|---|
| Home page | `tools/partials.py` → `home_body` |
| Lane-by-lane pathway timeline (Squads › The pathway) | `tools/partials.py` → `ITEMS` |
| Navigation, footer and each page's top buttons (`HERO_CTA`) | `tools/build.py` |
| Placeholder photos and their keywords | `tools/photos.py` |
| Look and feel (colours, type, spacing) | `assets/site.css` (tokens at the top) |
| Mobile menu, timeline, forms, waterline animation | `assets/site.js` |

## Design tokens

DM Sans. White base, cream `#FAF6EE` panels, navy `#06303F`, yellow `#FDD32A`, sky `#E4F1F6`. Corners are 20–28px, buttons are pills. Welfare details sit in the footer of every page.

## Source

The copy comes from the drafts in the club's website project (`content/pages/`), with the voice smoothed in places (see `voice-and-templates.md` there). Nothing from the private folder is included.
