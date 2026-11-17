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
- The home page hero is a looping clip of a Leander swimmer at the London Regionals (muted, pausable, and still when the device asks for reduced motion). Club media lives in `assets/media/`.
- The real Leander crest, plus the Swim England Affiliated Club, SwimMark and Clubmark marks in the footer.
- [`/style-options/`](https://preview.leanderswim.com/style-options/) compares four corner and button styles; **D · Lane line** is the default. Adding `?style=a`, `b`, `c` or `d` to any page switches the whole prototype on that device.
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
| Home page (and its hero video) | `tools/partials.py` → `home_body`, `HERO_VIDEO` |
| Corner and button options | `assets/site.css` (`data-style` blocks at the top), `tools/partials.py` → `OPTIONS` |
| Lane-by-lane pathway timeline (Squads › The pathway) | `tools/partials.py` → `ITEMS` |
| Navigation and mega menu (`NAV`, `MEGA`), footer and each page's top buttons (`HERO_CTA`) | `tools/build.py` |
| Placeholder photos and their keywords | `tools/photos.py` |
| Social sharing image (1200×630) | `tools/share-card/card.html`, rendered to `assets/share-card.jpg` (see below) |
| Look and feel (colours, type, spacing) | `assets/site.css` (tokens at the top) |
| Mobile menu, timeline, forms, waterline animation | `assets/site.js` |

## Sharing card

Every page has Open Graph and Twitter/X tags, so links shared on WhatsApp, Facebook, LinkedIn, Slack and X show a preview with the page title, its description and `assets/share-card.jpg`. To change the image, edit `tools/share-card/card.html` and re-render it:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1200,630 --virtual-time-budget=6000 --screenshot="$PWD/assets/share-card.png" "file://$PWD/tools/share-card/card.html"
```

Then convert it to JPEG (or keep the PNG and update the filename in `tools/build.py`). Apps cache previews, so a link already shared may show the old card for a while.

## Checking speed and accessibility

`python3 tools/pagespeed.py` runs Google PageSpeed Insights (Lighthouse) on every published page, mobile and desktop, and writes `reports/pagespeed.md`. Run it after publishing. An optional `PSI_KEY` environment variable raises Google's rate limit.

## Design tokens

DM Sans. White base, cream `#FAF6EE` panels, navy `#06303F`, yellow `#FDD32A`, sky `#E4F1F6`. Corners are 20–28px, buttons are pills. Welfare details sit in the footer of every page.

## Source

The copy comes from the drafts in the club's website project (`content/pages/`), with the voice smoothed in places (see `voice-and-templates.md` there). Nothing from the private folder is included.
