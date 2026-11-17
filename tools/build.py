#!/usr/bin/env python3
"""Build the Leander website prototype.

Reads the page drafts in content/ (Markdown with front matter) and writes static
HTML pages into the repository root, one folder per URL (e.g. squads/pathway/index.html).
The generated HTML is committed, so GitHub Pages serves it with no build step.

Usage:  python3 tools/build.py
Only uses the Python standard library.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
SITE_NAME = "Leander Swimming Club"
CREST_SRC = "assets/leander-crest.png"
import hashlib
VERSION = hashlib.md5((ROOT / "assets/site.css").read_bytes() + (ROOT / "assets/site.js").read_bytes()).hexdigest()[:8]
RTS_URL = "https://aretelic.github.io/race-the-standards/"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from photos import PHOTOS, pick_photo  # noqa: E402
from partials import home_body, timeline_html, style_options_body  # noqa: E402

# --------------------------------------------------------------------------
# Site map and navigation
# --------------------------------------------------------------------------
NAV = [
    ("Learn to Swim", "/learn", [
        ("The Academy", "/learn/academy"),
        ("Fees and term dates", "/learn/fees-and-term-dates"),
        ("Kit by stage", "/learn/kit-by-stage"),
        ("Join the waiting list", "/learn/waiting-list"),
    ]),
    ("Squads", "/squads", [
        ("The pathway", "/squads/pathway"),
        ("Squad standards", "/squads/squad-standards"),
        ("Race the Standards", "/squads/race-the-standards"),
        ("swimmingresults.org explained", "/squads/swimmingresults-explained"),
        ("Athlete support", "/squads/athlete-support"),
        ("Club records", "/squads/club-records"),
        ("University and scholarships", "/squads/university-and-scholarships"),
        ("Book a trial", "/squads/book-a-trial"),
    ]),
    ("Swim for Life", "/swim-for-life", [
        ("Diamond", "/swim-for-life/diamond"),
        ("Masters", "/swim-for-life/masters"),
        ("Inclusive by design", "/swim-for-life/inclusive-by-design"),
    ]),
    ("Galas", "/galas", [
        ("Leander galas 2027", "/galas"),
        ("How galas work", "/galas/how-galas-work"),
        ("The Tadpole Trophy", "/galas/tadpole-trophy"),
        ("The Seahorse Sprint", "/galas/seahorse-sprint"),
        ("The Mercury Open", "/galas/mercury-open"),
        ("Gala calendar", "TU:TeamUnify – calendar"),
    ]),
    ("Club", "/club", [
        ("How the club works", "/club/how-the-club-works"),
        ("Beyond the pool", "/club/beyond-the-pool"),
        ("Volunteer and officiate", "/club/volunteer-and-officiate"),
        ("Coaches and team", "/club/coaches-and-team"),
        ("Our story since 1949", "/club/our-story"),
        ("Where we swim", "/club/where-we-swim"),
        ("Safeguarding and policies", "/club/safeguarding-and-policies"),
        ("Glossary", "/club/glossary"),
    ]),
    ("News", "/news", []),
]

# [LINK: name] -> internal URL. Anything not listed is an external system placeholder.
LINKS = {
    "squad standards": "/squads/squad-standards",
    "join us": "/join-us",
    "swimmingresults explained": "/squads/swimmingresults-explained",
    "race the standards": "/squads/race-the-standards",
    "how the leander pathway works": "/squads/pathway",
    "university and scholarships": "/squads/university-and-scholarships",
    "university & scholarships": "/squads/university-and-scholarships",
    "how galas work": "/galas/how-galas-work",
    "academy waiting list form": "/learn/waiting-list",
    "academy waiting list": "/learn/waiting-list",
    "join the academy waiting list": "/learn/waiting-list",
    "diamond": "/swim-for-life/diamond",
    "beyond the pool": "/club/beyond-the-pool",
    "volunteer & become an official": "/club/volunteer-and-officiate",
    "kit by stage": "/learn/kit-by-stage",
    "join us – swimmers with a disability": "/join-us#disability",
    "join us – masters": "/join-us#adult",
    "join us – diamond": "/join-us#teen",
    "fees and what they buy": "/learn/fees-and-term-dates",
    "athlete support": "/squads/athlete-support",
    "squad trial form": "/squads/book-a-trial#trial-form",
    "book a squad trial": "/squads/book-a-trial#trial-form",
    "request a trial": "#trial-form",
    "safeguarding & policies": "/club/safeguarding-and-policies",
    "our story since 1949": "/club/our-story",
    "news & results": "/news",
    "masters": "/swim-for-life/masters",
    "inclusive by design": "/swim-for-life/inclusive-by-design",
    "glossary": "/club/glossary",
    "use join us": "/join-us",
    "see leander galas 2027 →": "/galas",
    "see leander galas 2027": "/galas",
    "leander galas 2027": "/galas",
    "the seahorse sprint": "/galas/seahorse-sprint",
    "the tadpole trophy": "/galas/tadpole-trophy",
    "the leander pathway": "/squads/pathway",
    "photography policy": "TU:Photography Policy",
    "try your first masters session": "/join-us#adult",
    "ask about diamond": "/join-us#teen",
}
# Friendly names for external placeholders, shown in the toast.
EXTERNAL = {
    "teamunify": "TeamUnify (the members' system)",
    "printmykit": "the club shop on printmykit",
    "mailsports": "Mailsports",
    "swim england": "Swim England's website",
    "privacy notice": "the club's Privacy Notice",
    "policy": "the policy document",
    "code of conduct": "the code of conduct",
}

# Hero calls to action, by page URL. The most likely visitor's next step goes first.
WAITLIST = ("Join the Academy waiting list", "/learn/waiting-list", "primary")
TRIAL = ("Book a squad trial", "/squads/book-a-trial#trial-form", "primary")
MASTERS = ("Try your first Masters session", "/join-us#adult", "primary")
DIAMOND = ("Ask about Diamond", "/join-us#teen", "primary")
JOIN = ("Join us", "/join-us", "primary")


def sec(b):
    return (b[0], b[1], "secondary")


HERO_CTA = {
    "/join-us": [WAITLIST, sec(TRIAL), sec(MASTERS)],
    "/learn": [WAITLIST, ("Explore the Academy", "/learn/academy", "secondary")],
    "/learn/academy": [WAITLIST, ("Fees and term dates", "/learn/fees-and-term-dates", "secondary")],
    "/learn/fees-and-term-dates": [WAITLIST, ("Book a squad trial", "/squads/book-a-trial#trial-form", "secondary")],
    "/learn/kit-by-stage": [WAITLIST, ("Visit the club shop", "TU:Leander club shop on printmykit", "secondary")],
    "/learn/waiting-list": [("Go to the form", "#waiting-list-form", "primary"), ("About the Academy", "/learn/academy", "secondary")],
    "/squads": [TRIAL, ("See the pathway", "/squads/pathway", "secondary")],
    "/squads/pathway": [TRIAL, ("Explore the timeline", "#timeline", "secondary"), sec(WAITLIST)],
    "/squads/squad-standards": [TRIAL, ("Race the Standards", "/squads/race-the-standards", "secondary")],
    "/squads/race-the-standards": [("Race your PB", "#tool", "primary"), sec(TRIAL)],
    "/squads/swimmingresults-explained": [("Open swimmingresults.org", "EXT:https://www.swimmingresults.org/", "primary"), sec(TRIAL)],
    "/squads/athlete-support": [TRIAL],
    "/squads/club-records": [TRIAL, ("Race the Standards", "/squads/race-the-standards", "secondary")],
    "/squads/university-and-scholarships": [TRIAL, ("Squad standards", "/squads/squad-standards", "secondary")],
    "/squads/book-a-trial": [("Request a trial", "#trial-form", "primary"), ("Squad standards", "/squads/squad-standards", "secondary")],
    "/swim-for-life": [MASTERS, sec(DIAMOND)],
    "/swim-for-life/diamond": [DIAMOND],
    "/swim-for-life/masters": [MASTERS],
    "/swim-for-life/inclusive-by-design": [("Start a conversation", "/join-us#disability", "primary"), sec(TRIAL)],
    "/galas": [("Gala calendar", "TU:TeamUnify – calendar", "primary"), ("How galas work", "/galas/how-galas-work", "secondary")],
    "/galas/how-galas-work": [("See Leander galas 2027", "/galas", "primary"), ("Gala calendar", "TU:TeamUnify – calendar", "secondary")],
    "/club": [JOIN, ("Volunteer with us", "/club/volunteer-and-officiate", "secondary")],
    "/club/how-the-club-works": [JOIN, ("Volunteer with us", "/club/volunteer-and-officiate", "secondary")],
    "/club/beyond-the-pool": [TRIAL, ("Become an official", "/club/volunteer-and-officiate", "secondary")],
    "/club/volunteer-and-officiate": [("Sign up to help", "#ways-to-help", "primary"), ("The officials pathway", "#the-officials-pathway-step-by-step", "secondary")],
    "/club/coaches-and-team": [JOIN, ("How the club works", "/club/how-the-club-works", "secondary")],
    "/club/our-story": [JOIN, ("2025/26 round-up", "/news/2025-26-season-round-up", "secondary")],
    "/club/where-we-swim": [JOIN, ("Session times", "#session-times", "secondary")],
    "/club/safeguarding-and-policies": [("Talk to a Welfare Officer", "#worried-about-a-swimmer-talk-to-us", "primary")],
    "/club/glossary": [JOIN, ("The pathway", "/squads/pathway", "secondary")],
    "/news": [JOIN, sec(TRIAL)],
    "/news/2025-26-season-round-up": [TRIAL, sec(WAITLIST)],
    "/news/freya-anderson-clinic-preview": [("Athlete support", "/squads/athlete-support", "primary"), sec(TRIAL)],
}

PAGES = []  # filled by load_pages()

# Mega menu: an intro line and one call to action per section
MEGA = {
    "Learn to Swim": ("Our Academy teaches children aged 5 to 10 to swim properly, in small groups at Ernest Bevin.",
                      ("Join the Academy waiting list", "/learn/waiting-list", "Places are limited, so the first step is the waiting list.")),
    "Squads": ("Training groups for young swimmers who want to race, from first galas to national finals.",
               ("Book a squad trial", "/squads/book-a-trial#trial-form", "Already swimming well? A trial is the place to start.")),
    "Swim for Life": ("Diamond for teenagers, Masters for adults, and squads open to swimmers with a disability.",
                      ("Try your first Masters session", "/join-us#adult", "Coached sessions for adults, whatever your reason for swimming.")),
    "Galas": ("Three Leander galas in 2027, and a plain-English guide to race day.",
              ("How galas work", "/galas/how-galas-work", "New to galas? Here's what happens on the day.")),
    "Club": ("A not-for-profit club since 1949, run by volunteers alongside a professional coaching team.",
             ("Volunteer with us", "/club/volunteer-and-officiate", "Galas can't run without volunteers. Could you help?")),
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\{\{[^}]*\}\}", "", s)
    s = s.lower().replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:60].strip("-")


def out_path(url):
    if url == "/":
        return ROOT / "index.html"
    return ROOT / url.strip("/") / "index.html"


def depth(url):
    return 0 if url == "/" else len(url.strip("/").split("/"))


class Ctx:
    """Per-page rendering context."""

    def __init__(self, url):
        self.url = url
        self.root = "../" * depth(url) or "./"
        self.used_photos = set()
        self.photo_n = 0
        self.warnings = []

    def href(self, target):
        """Resolve an internal URL ('/x/y#z') to a relative link."""
        if target.startswith("#") or target.startswith("http") or target.startswith("mailto:"):
            return target
        path, _, frag = target.partition("#")
        path = path.rstrip("/")
        rel = self.root if path in ("", "/") else self.root + path.strip("/") + "/"
        if path.strip("/") == self.url.strip("/") and frag:
            return "#" + frag
        return rel + ("#" + frag if frag else "")


def ext_dest(name):
    low = name.lower()
    for k, v in EXTERNAL.items():
        if k in low:
            return v
    return name


def link_html(ctx, label_html, target, cls=""):
    """Return an <a> for an internal path, a [LINK: ...] name, email, or external URL."""
    t = target.strip()
    c = f' class="{cls}"' if cls else ""
    if t.startswith("TU:"):
        name = t[3:]
        return f'<a href="#" class="{(cls + " ").strip()} ph-link" data-dest="{esc(ext_dest(name))}" title="Placeholder: {esc(name)}">{label_html}</a>'.replace('class=" ph-link"', 'class="ph-link"')
    if t.startswith("EXT:"):
        return f'<a href="{esc(t[4:])}"{c} rel="noopener" target="_blank">{label_html}<span class="visually-hidden"> (opens in a new tab)</span></a>'
    if "@" in t and " " not in t:
        return f'<a href="mailto:{esc(t)}"{c}>{label_html}</a>'
    if t.startswith("/") or t.startswith("#"):
        return f'<a href="{esc(ctx.href(t))}"{c}>{label_html}</a>'
    if t.startswith("http"):
        return f'<a href="{esc(t)}"{c} rel="noopener">{label_html}</a>'
    # a [LINK: name]
    key = t.lower().strip()
    if key in LINKS:
        return link_html(ctx, label_html, LINKS[key], cls)
    cls2 = (cls + " ph-link").strip()
    return f'<a href="#" class="{cls2}" data-dest="{esc(ext_dest(t))}" title="Placeholder link: {esc(t)}">{label_html}</a>'


# --------------------------------------------------------------------------
# Inline Markdown
# --------------------------------------------------------------------------
def tbc_html(text):
    text = text.strip()
    if text.upper().startswith("TBC"):
        body = text[3:].lstrip(" :").strip()
        if not body:
            return '<mark class="tbc bare" title="To be confirmed"></mark>'
        return f'<mark class="tbc" title="To be confirmed">{esc(body)}</mark>'
    return f'<mark class="tbc">{esc(text)}</mark>'


def inline(ctx, s):
    """Convert inline Markdown to HTML."""
    tokens = {}

    def stash(h):
        k = f"\x00{len(tokens)}\x00"
        tokens[k] = h
        return k

    s = re.sub(r"\{\{(.*?)\}\}", lambda m: stash(tbc_html(m.group(1))), s)
    s = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{esc(m.group(1))}</code>"), s)
    # [label](url)
    s = re.sub(r"\[([^\]\[]+)\]\(([^)\s]+)\)", lambda m: stash(link_html(ctx, inline(ctx, m.group(1)), m.group(2))), s)
    # [LINK: name]
    s = re.sub(r"\[LINK:\s*([^\]]+)\]", lambda m: stash(link_html(ctx, esc(m.group(1).split("–")[-1].strip() if m.group(1).lower().startswith("teamunify") else m.group(1).strip()), m.group(1))), s)
    # bare [Label] that is a known internal page
    def bare(m):
        key = m.group(1).strip().lower()
        if key in LINKS:
            return stash(link_html(ctx, esc(m.group(1)), LINKS[key]))
        ctx.warnings.append(f"unresolved bracket [{m.group(1)}]")
        return m.group(0)
    s = re.sub(r"\[([A-Z][^\]\[:]{1,60})\](?!\()", bare, s)
    # emails and bare URLs
    s = re.sub(r"(?<![\w/@.])([\w.+-]+@leanderswim\.com)", lambda m: stash(f'<a href="mailto:{m.group(1)}">{m.group(1)}</a>'), s)
    s = re.sub(r"(?<![\"(=])(https?://[^\s)<]+[^\s)<.,;])", lambda m: stash(f'<a href="{esc(m.group(1))}" rel="noopener">{esc(m.group(1))}</a>'), s)
    s = esc(s).replace("&#x27;", "'").replace("&quot;", '"')
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])", r"<em>\1</em>", s)
    for _ in range(3):
        for k, v in tokens.items():
            s = s.replace(esc(k), v).replace(k, v)
    return s


# --------------------------------------------------------------------------
# Block parser
# --------------------------------------------------------------------------
BTN_RE = [
    re.compile(r"^\*\*\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)\*\*$"),
    re.compile(r"^\*\*\[(?P<label>[^\]]+)\]\*\*\s*(?:→\s*)?(?P<target>.*)$"),
]
BARE_BTNS = re.compile(r"^(\[[^\]]+\]\s*)+$")


def parse_button_line(line):
    line = line.strip()
    for rx in BTN_RE:
        m = rx.match(line)
        if m:
            label = m.group("label").replace("→", "").strip()
            target = m.group("target").strip()
            lm = re.match(r"^\[LINK:\s*(.+)\]$", target)
            if lm:
                target = lm.group(1)
            elif target.startswith("{{"):
                target = "TU:" + target.strip("{} ").replace("TBC:", "").strip()
            elif not target:
                target = LINKS.get(label.lower(), "/join-us")
            return [(label, target)]
    if BARE_BTNS.match(line) and not line.startswith("[LINK") and not line.startswith("[PHOTO"):
        labels = re.findall(r"\[([^\]]+)\]", line)
        if all(l.lower() in LINKS for l in labels):
            return [(l, LINKS[l.lower()]) for l in labels]
    return None


def parse_blocks(md):
    lines = md.split("\n")
    blocks = []
    i = 0
    para = []

    def flush():
        nonlocal para
        if para:
            blocks.append({"t": "p", "lines": para})
            para = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        st = line.strip()
        if st.startswith("```"):
            flush()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                i += 1
            i += 1
            continue
        if not st:
            flush(); i += 1; continue
        if re.match(r"^\*(Designer note|Form build note|Note for editor|Data note)", st):
            flush(); i += 1; continue
        m = re.match(r"^(#{1,4})\s+(.*)$", st)
        if m:
            flush()
            text = m.group(2).strip()
            anchor = None
            am = re.search(r"\s*\{#([\w-]+)\}$", text)
            if am:
                anchor = am.group(1); text = text[:am.start()].strip()
            blocks.append({"t": "h", "level": len(m.group(1)), "text": text, "id": anchor})
            i += 1; continue
        if re.match(r"^-{3,}$", st):
            flush(); blocks.append({"t": "hr"}); i += 1; continue
        if st.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip()); i += 1
            blocks.append({"t": "table", "rows": rows})
            continue
        if re.match(r"^\[(PHOTO|SCREENSHOT|EMBED|DIAGRAM|NEWS|TIMELINE|FORM)\b", st):
            flush()
            kind = re.match(r"^\[(\w+)", st).group(1)
            body = re.sub(r"^\[\w+:?\s*", "", st)
            body = body[:-1] if body.endswith("]") else body
            blocks.append({"t": kind.lower(), "text": body.strip()})
            i += 1; continue
        btns = parse_button_line(st)
        if btns:
            flush(); blocks.append({"t": "buttons", "items": btns}); i += 1; continue
        if re.match(r"^(→|- →)", st):
            flush(); blocks.append({"t": "links", "text": st.lstrip("-").strip().lstrip("→").strip()}); i += 1; continue
        if re.match(r"^([-*]|\d+\.)\s+", st):
            flush()
            ordered = bool(re.match(r"^\d+\.", st))
            items = []
            while i < len(lines):
                l = lines[i].rstrip()
                s2 = l.strip()
                mm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", l)
                if mm:
                    indent = len(mm.group(1))
                    if indent >= 2 and items:
                        items[-1].setdefault("sub", []).append(mm.group(3))
                    else:
                        items.append({"text": mm.group(3)})
                    i += 1
                elif s2 and items and l.startswith("   "):
                    items[-1]["text"] += " " + s2; i += 1
                else:
                    break
            blocks.append({"t": "ol" if ordered else "ul", "items": items})
            continue
        if st.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip(">").strip()); i += 1
            blocks.append({"t": "quote", "lines": q})
            continue
        para.append(st)
        i += 1
    flush()
    return blocks


def split_cells(row):
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def strip_md(s):
    return re.sub(r"[*_`]", "", s).strip()


# --------------------------------------------------------------------------
# Block renderers
# --------------------------------------------------------------------------
def render_photo(ctx, desc, cls="photo", eager=False, brief=True):
    ph = pick_photo(desc, ctx.used_photos, ctx.photo_n)
    ctx.photo_n += 1
    ctx.used_photos.add(ph["slug"])
    alt = re.sub(r"\{\{.*?\}\}", "", desc).strip(" ,")
    load = "eager" if eager else "lazy"
    prio = ' fetchpriority="high"' if eager else ""
    sizes = "(max-width: 820px) calc(100vw - 40px), 560px" if cls == "photo" else "(max-width: 820px) calc(100vw - 40px), 380px"
    src = f'{ph["image_url"]}?auto=format&fit=crop&w=900&q=60'
    srcset = ", ".join(f'{ph["image_url"]}?auto=format&fit=crop&w={w}&q=60 {w}w' for w in (480, 720, 960, 1200))
    credit = f'<span class="photo-credit">Photo: <a href="{esc(ph["page_url"])}" rel="noopener">{esc(ph["photographer"])} on Unsplash</a></span>'
    b = f'<figcaption class="photo-brief">{inline(ctx, desc)} · {credit}</figcaption>' if brief else ""
    return (f'<figure class="photo-fig"><div class="{cls}"><img src="{esc(src)}" srcset="{esc(srcset)}" sizes="{sizes}" '
            f'alt="Placeholder: {esc(alt)}" loading="{load}" decoding="async"{prio}>'
            f'<span class="photo-label">Placeholder photo</span></div>{b}</figure>')


def render_table(ctx, rows):
    rows = [r for r in rows if not re.match(r"^\|?\s*:?-{2,}", r)]
    if not rows:
        return ""
    head = split_cells(rows[0])
    body = [split_cells(r) for r in rows[1:]]
    low = [strip_md(h).lower() for h in head]
    # Form specification -> mock form
    if low[:3] == ["field", "type", "required"]:
        return render_form_fields(ctx, body)
    # Pathway strip
    if len(head) == 3 and any(x in " ".join(low) for x in ("you are here", "this squad")) and len(body) == 1:
        keys = [strip_md(h) for h in head]
        cells = body[0]
        out = ['<div class="strip">']
        for n, (k, v) in enumerate(zip(keys, cells)):
            here = " here" if n == 1 else ""
            out.append(f'<div class="strip-step{here}"><span class="k">{esc(k)}</span><span>{inline(ctx, v)}</span></div>')
        out.append("</div>")
        return "".join(out)
    # Header-less two-column tables -> facts or stat tiles
    if all(not h for h in head) and len(head) == 2:
        firsts = [strip_md(r[0]) for r in body]
        if all(len(f) <= 6 for f in firsts):
            tiles = "".join(f'<div class="stat"><div class="n">{esc(strip_md(r[0]))}</div><div class="l">{inline(ctx, r[1])}</div></div>' for r in body)
            return f'<div class="stats">{tiles}</div>'
        items = "".join(f'<div><dt>{inline(ctx, strip_md(r[0]))}</dt><dd>{inline(ctx, r[1])}</dd></div>' for r in body if len(r) >= 2)
        return f'<dl class="facts">{items}</dl>'
    wide = " table-wide" if len(head) >= 4 else ""
    first_col_bold = all(r and r[0].startswith("**") for r in body)
    th = "".join(f'<th scope="col">{inline(ctx, h) if h else "<span class=visually-hidden>Item</span>"}</th>' for h in head)
    trs = []
    for r in body:
        cells = []
        for n, c in enumerate(r):
            if n == 0 and first_col_bold:
                cells.append(f'<th scope="row">{inline(ctx, c)}</th>')
            else:
                cells.append(f"<td>{inline(ctx, c)}</td>")
        trs.append("<tr>" + "".join(cells) + "</tr>")
    hint = '<p class="table-hint">Scroll sideways to see the whole table.</p>' if wide else ""
    return f'{hint}<div class="table-wrap{wide}" role="region" aria-label="Table"><table><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>'


FORM_N = [0]


def render_form_fields(ctx, body):
    out = ['<div class="form-grid">']
    for r in body:
        r = (r + ["", "", "", ""])[:4]
        name, ftype, req, notes = r
        FORM_N[0] += 1
        fid = f"f{FORM_N[0]}"
        label = inline(ctx, name)
        required = strip_md(req).lower().startswith("yes")
        req_html = ' <span class="req" aria-hidden="true">*</span>' if required else ' <span class="hint">(optional)</span>'
        req_attr = " required" if required else ""
        hint = f'<span class="hint" id="{fid}-h">{inline(ctx, notes)}</span>' if notes else ""
        desc = f' aria-describedby="{fid}-h"' if notes else ""
        t = strip_md(ftype)
        tl = t.lower()
        full = " full" if tl.startswith(("long", "checkbox")) else ""
        if tl.startswith("dropdown"):
            opts = [o.strip() for o in t.split(":", 1)[1].split("/")] if ":" in t else []
            o = "".join(f"<option>{esc(x)}</option>" for x in opts)
            ctrl = f'<select id="{fid}"{req_attr}{desc}><option value="">Choose…</option>{o}</select>'
        elif tl.startswith("checkboxes"):
            opts = [o.strip() for o in t.split(":", 1)[1].split("/")] if ":" in t else []
            cb = "".join(f'<label><input type="checkbox" name="{fid}"> {esc(x)}</label>' for x in opts)
            out.append(f'<fieldset class="field full"><legend>{label}{req_html}</legend><div class="checks">{cb}</div>{hint}</fieldset>')
            continue
        elif tl == "checkbox":
            out.append(f'<div class="field full"><div class="checks"><label><input type="checkbox" id="{fid}"{req_attr}> {inline(ctx, notes.strip(chr(34)))}</label></div></div>')
            continue
        elif tl.startswith("long"):
            ctrl = f'<textarea id="{fid}"{req_attr}{desc}></textarea>'
        else:
            itype = {"email": "email", "phone": "tel", "date": "date"}.get(tl, "text")
            ac = {"email": ' autocomplete="email"', "tel": ' autocomplete="tel"'}.get(itype, "")
            ctrl = f'<input type="{itype}" id="{fid}"{req_attr}{desc}{ac}>'
        out.append(f'<div class="field{full}"><label for="{fid}">{label}{req_html}</label>{ctrl}{hint}</div>')
    out.append("</div>")
    return "".join(out)


def render_list(ctx, b, cls=""):
    tag = b["t"]
    items = []
    for it in b["items"]:
        sub = ""
        if it.get("sub"):
            sub = "<ul>" + "".join(f"<li>{inline(ctx, x)}</li>" for x in it["sub"]) + "</ul>"
        items.append(f"<li>{inline(ctx, it['text'])}{sub}</li>")
    if tag == "ol" and not cls:
        cls = "steps"
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c}>{''.join(items)}</{tag}>"


def render_buttons(ctx, items, first_primary=True):
    out = []
    for n, (label, target) in enumerate(items):
        kind = "btn-primary" if (n == 0 and first_primary) else "btn-secondary"
        out.append(link_html(ctx, esc(label), target, f"btn {kind}"))
    return f'<div class="btn-row">{"".join(out)}</div>'


def render_para(ctx, lines):
    # FAQ-like or "**Title**\ntext" -> keep line breaks
    return "<p>" + "<br>".join(inline(ctx, l) for l in lines) + "</p>"


def render_block(ctx, b):
    t = b["t"]
    if t == "p":
        return render_para(ctx, b["lines"])
    if t == "h":
        lvl = min(b["level"] + 0, 4)
        hid = b.get("id") or slugify(b["text"])
        return f'<h{lvl} id="{hid}">{inline(ctx, b["text"])}</h{lvl}>'
    if t in ("ul", "ol"):
        return render_list(ctx, b)
    if t == "table":
        return f'<div class="block-wide">{render_table(ctx, b["rows"])}</div>'
    if t == "photo":
        return render_photo(ctx, b["text"])
    if t == "buttons":
        return render_buttons(ctx, b["items"])
    if t == "links":
        return f'<p class="links-line">{inline(ctx, b["text"]).replace(" · ", " ")}</p>'
    if t == "quote":
        return f'<figure class="quote"><blockquote>{"<br>".join(inline(ctx, l) for l in b["lines"])}</blockquote></figure>'
    if t == "screenshot":
        return f'<div class="placeholder-box" role="img" aria-label="Screenshot to add: {esc(b["text"])}"><strong>Screenshot to add</strong><span>{inline(ctx, b["text"])}</span></div>'
    if t == "embed":
        if "race the standards" in b["text"].lower():
            return (f'<div class="embed-frame" id="tool"><div class="embed-bar"><strong>Race the Standards</strong>'
                    f'<a href="{RTS_URL}" target="_blank" rel="noopener">Open the tool in a new tab ↗</a></div>'
                    f'<iframe src="{RTS_URL}" title="Race the Standards: compare a PB with county, regional and national times" loading="lazy"></iframe></div>')
        return f'<div class="placeholder-box"><strong>Embed to add</strong><span>{inline(ctx, b["text"])}</span></div>'
    if t == "timeline":
        return timeline_html(ctx)
    if t == "hr":
        return ""
    return ""


# --------------------------------------------------------------------------
# Section layout
# --------------------------------------------------------------------------
def words(blocks):
    n = 0
    for b in blocks:
        if b["t"] == "p":
            n += sum(len(l.split()) for l in b["lines"])
        elif b["t"] in ("ul", "ol"):
            n += sum(len(i["text"].split()) for i in b["items"])
        elif b["t"] == "table":
            n += 200
    return n


def group_h3(blocks):
    """Split blocks into (intro, [ (h3, blocks) ... ])."""
    intro, groups = [], []
    cur = None
    for b in blocks:
        if b["t"] == "h" and b["level"] == 3:
            cur = (b, [])
            groups.append(cur)
        elif cur is None:
            intro.append(b)
        else:
            cur[1].append(b)
    return intro, groups


def is_faq(heading):
    h = heading.lower()
    return h.startswith("questions") or h.startswith("faq") or "people ask" in h


def render_faq(ctx, blocks):
    out = ['<div class="faq">']
    q, ans = None, []

    def emit():
        if q:
            out.append(f'<details><summary>{inline(ctx, q)}</summary><div class="answer prose">{"".join(ans)}</div></details>')

    for b in blocks:
        if b["t"] == "p" and b["lines"][0].startswith("**") and b["lines"][0].rstrip().endswith("?**"):
            emit()
            q = b["lines"][0].strip("*")
            rest = b["lines"][1:]
            ans = [render_para(ctx, rest)] if rest else []
        elif q is not None:
            ans.append(render_block(ctx, b))
        else:
            out.append(render_block(ctx, b))
    emit()
    out.append("</div>")
    return "".join(out)


def card_html(ctx, h, blocks):
    hid = h.get("id") or slugify(h["text"])
    photo = ""
    body = []
    for b in blocks:
        if b["t"] == "photo" and not photo:
            photo = render_photo(ctx, b["text"], brief=False)
        elif b["t"] == "p" and len(b["lines"]) and re.match(r"^\*\*[^*]+\*\*$", b["lines"][0]) and not body:
            body.append(f'<p class="card-strap">{inline(ctx, b["lines"][0].strip("*"))}</p>')
            if len(b["lines"]) > 1:
                body.append(render_para(ctx, b["lines"][1:]))
        else:
            body.append(render_block(ctx, b))
    return f'<article class="card" id="{hid}">{photo}<div class="card-body"><h3>{inline(ctx, h["text"])}</h3>{"".join(body)}</div></article>'


def render_section(ctx, h2, blocks, alt):
    title = h2["text"]
    sid = h2.get("id") or slugify(title)
    cls = "section alt" if alt else "section"
    blocks = [b for b in blocks if b["t"] != "hr"]
    head = f'<h2 id="{sid}-h">{inline(ctx, title)}</h2>'

    if title.lower() == "related":
        pills = []
        for b in blocks:
            if b["t"] in ("ul",):
                for it in b["items"]:
                    pills.append(inline(ctx, it["text"]))
        rest = [b for b in blocks if b["t"] != "ul"]
        links = "".join(f'<span class="chip-wrap">{p}</span>' for p in pills)
        links = re.sub(r'<a href="([^"]*)"( class="[^"]*")?', lambda m: f'<a href="{m.group(1)}" class="chip-link{" " + m.group(2).split(chr(34))[1] if m.group(2) else ""}"', links)
        tail = render_cta_tail(ctx, rest)
        return (f'<section class="{cls} tight" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">'
                f'<div class="section-head">{head}</div><div class="related">{links}</div>{tail}</div></section>')

    if is_faq(title):
        return (f'<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">'
                f'<div class="section-head">{head}</div>{render_faq(ctx, blocks)}</div></section>')

    kinds = [b["t"] for b in blocks]
    # CTA band: short section that is mostly a button
    if "buttons" in kinds and words(blocks) < 70 and "table" not in kinds and not any(b["t"] == "h" for b in blocks):
        text = [render_block(ctx, b) for b in blocks if b["t"] not in ("buttons", "links")]
        btns = "".join(render_block(ctx, b) for b in blocks if b["t"] == "buttons")
        lnk = "".join(render_block(ctx, b) for b in blocks if b["t"] == "links")
        return (f'<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap"><div class="band">'
                f'<div class="band-text">{head}{"".join(text)}</div><div>{btns}{lnk}</div></div></div></section>')

    intro, groups = group_h3(blocks)
    parts = []
    # Intro: if a single photo and prose, split layout
    intro_photos = [b for b in intro if b["t"] == "photo"]
    intro_other = [b for b in intro if b["t"] != "photo"]
    has_wide = any(b["t"] in ("table",) for b in intro_other)
    if len(intro_photos) == 1 and intro_other and not has_wide and not groups:
        prose = "".join(render_block(ctx, b) for b in intro_other)
        parts.append(f'<div class="split"><div class="prose">{head}{prose}</div>{render_photo(ctx, intro_photos[0]["text"])}</div>')
        head_done = True
    else:
        head_done = False
        inner = []
        for b in intro:
            r = render_block(ctx, b)
            inner.append(r)
        parts.append(f'<div class="section-head">{head}</div>' if not intro else "")
        if intro:
            parts.append(flow(ctx, intro, head))
            head_done = True
    if groups:
        short = all(words(g[1]) <= 95 and not any(b["t"] in ("table", "ol", "h") for b in g[1]) for g in groups) and len(groups) >= 2
        if short:
            cols = " cols-2" if len(groups) in (2, 4) else ""
            parts.append(f'<div class="card-grid{cols}">' + "".join(card_html(ctx, h, bl) for h, bl in groups) + "</div>")
        else:
            for h, bl in groups:
                hid = h.get("id") or slugify(h["text"])
                inner = []
                first = True
                for b in bl:
                    if first and b["t"] == "p" and re.match(r"^\*\*[^*]+\*\*$", b["lines"][0]):
                        inner.append(f'<p class="lead-line">{inline(ctx, b["lines"][0].strip("*"))}</p>')
                        if len(b["lines"]) > 1:
                            inner.append(render_para(ctx, b["lines"][1:]))
                    else:
                        inner.append(render_block(ctx, b))
                    first = False
                parts.append(f'<div class="subblock" id="{hid}"><h3>{inline(ctx, h["text"])}</h3><div class="prose">{"".join(inner)}</div></div>')
    return f'<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">{"".join(parts)}</div></section>'


WIDE = ("table", "timeline", "embed")


def flow(ctx, blocks, head=""):
    """Render blocks, keeping text in a readable column and letting wide blocks use the full width."""
    out, buf = [], [head] if head else []
    for b in blocks:
        if b["t"] in WIDE:
            if buf:
                out.append(f'<div class="prose">{"".join(buf)}</div>')
                buf = []
            out.append(f'<div class="wide-block">{render_block(ctx, b)}</div>')
        else:
            buf.append(render_block(ctx, b))
    if buf:
        out.append(f'<div class="prose">{"".join(buf)}</div>')
    return f'<div class="flow">{"".join(out)}</div>'


def render_cta_tail(ctx, blocks):
    if not blocks:
        return ""
    return '<div class="prose" style="margin-top:28px">' + "".join(render_block(ctx, b) for b in blocks) + "</div>"


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------
def parse_front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def section_of(url):
    seg = url.strip("/").split("/")[0] if url != "/" else ""
    for label, base, kids in NAV:
        if base.strip("/") == seg:
            return label, base, kids
    return None, None, []


def crest_svg(size=50):
    """The Leander crest (from the club's current site)."""
    return (f'<img class="crest" src="{CREST_SRC}" width="{size}" height="{size}" alt="">')



CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>'


def nav_href(ctx, target):
    if target.startswith("TU:"):
        return None
    return ctx.href(target)


def nav_link(ctx, label, target, cls=""):
    cur = ' aria-current="page"' if target == ctx.url else ""
    if target.startswith("TU:"):
        return link_html(ctx, esc(label), target, cls)
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{esc(ctx.href(target))}"{c}{cur}>{esc(label)}</a>'


def header_html(ctx):
    global CREST_SRC
    CREST_SRC = ctx.root + "assets/leander-crest.png"
    sec_label, _, _ = section_of(ctx.url)
    items = []
    for n, (label, base, kids) in enumerate(NAV):
        active = ' aria-current="true"' if label == sec_label else ""
        if kids:
            intro, cta = MEGA[label]
            links = [f"<li>{nav_link(ctx, kl, kt)}</li>" for kl, kt in kids if kt != base]
            overview = nav_link(ctx, f"{label} overview →", base, "mega-overview")
            cta_html = link_html(ctx, esc(cta[0]), cta[1], "btn btn-primary btn-small")
            items.append(f'<li class="nav-item has-dd"><button type="button" class="nav-link" aria-expanded="false" aria-controls="dd{n}"{active}>{esc(label)}{CHEV}</button>'
                         f'<div class="mega" id="dd{n}"><div class="wrap mega-inner">'
                         f'<div class="mega-intro"><p class="mega-title">{esc(label)}</p><p>{esc(intro)}</p>{overview}</div>'
                         f'<ul class="mega-links">{"".join(links)}</ul>'
                         f'<div class="mega-cta"><p>{esc(cta[2])}</p>{cta_html}</div></div></div></li>')
        else:
            cur = ' aria-current="page"' if ctx.url == base else active
            items.append(f'<li class="nav-item"><a class="nav-link" href="{esc(ctx.href(base))}"{cur}>{esc(label)}</a></li>')
    join = f'<a class="btn btn-primary btn-small" href="{esc(ctx.href("/join-us"))}">Join us</a>'
    members = link_html(ctx, "Members' login", "TU:TeamUnify – members' login", "members-link")
    burger = ('<button type="button" class="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">'
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>')
    # Mobile menu
    groups = []
    for n, (label, base, kids) in enumerate(NAV):
        if kids:
            sub = [f'<li>{nav_link(ctx, label + " overview", base)}</li>'] if base not in [k[1] for k in kids] else []
            sub += [f"<li>{nav_link(ctx, kl, kt)}</li>" for kl, kt in kids]
            open_ = label == sec_label
            groups.append(f'<div class="mm-group"><button type="button" aria-expanded="{str(open_).lower()}" aria-controls="mm{n}">{esc(label)}{CHEV}</button>'
                          f'<ul id="mm{n}"{" class=open" if open_ else ""}>{"".join(sub)}</ul></div>')
        else:
            groups.append(f'<a class="mm-single" href="{esc(ctx.href(base))}">{esc(label)}</a>')
    mobile = (f'<div class="mobile-menu" id="mobile-menu" hidden role="dialog" aria-modal="true" aria-label="Menu">'
              f'<div class="mobile-menu-head"><a class="brand" href="{esc(ctx.href("/"))}">{crest_svg(40)}<span class="brand-text"><span class="brand-name">Leander</span></span></a>'
              f'<button type="button" class="menu-toggle menu-close" style="display:inline-flex" aria-label="Close menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>'
              f'<nav aria-label="Main (mobile)">{"".join(groups)}<div class="mm-actions">'
              f'<a class="btn btn-primary" href="{esc(ctx.href("/join-us"))}">Join us</a>'
              f'{link_html(ctx, "Members&#39; login (TeamUnify)", "TU:TeamUnify – members&#39; login", "btn btn-secondary")}</div></nav></div>')
    bar = ('<div class="proto-bar"><div class="wrap"><span><strong>Prototype for feedback, not the live site.</strong> '
           'Copy and photos are drafts and placeholders.</span>'
           '<span class="tbc-key"><mark class="tbc bare"></mark> marks a fact still to confirm</span></div></div>')
    return (f'<a class="skip-link" href="#main">Skip to content</a>{bar}'
            f'<header class="site-header"><div class="wrap">'
            f'<a class="brand" href="{esc(ctx.href("/"))}">{crest_svg()}<span class="brand-text"><span class="brand-name">Leander</span><span class="brand-sub">Swimming Club, South London</span></span></a>'
            f'<nav class="main-nav" aria-label="Main"><ul>{"".join(items)}</ul></nav>'
            f'<div class="header-actions">{members}{join}{burger}</div></div></header>{mobile}')


def subnav_html(ctx):
    """Phones only: an 'In this section' picker. Desktop uses the mega menu and breadcrumb."""
    label, base, kids = section_of(ctx.url)
    if not kids:
        return ""
    entries = []
    if base not in [k[1] for k in kids]:
        entries.append(("Overview", base))
    entries += [(kl, kt) for kl, kt in kids if not kt.startswith("TU:")]
    links = "".join(f"<li>{nav_link(ctx, l, t)}</li>" for l, t in entries)
    current = next((l for l, t in entries if t == ctx.url), "Overview")
    return (f'<nav class="subnav" aria-label="{esc(label)} section"><div class="wrap">'
            f'<details class="subnav-mobile"><summary><span><span class="k">In {esc(label)}</span>{esc(current)}</span>{CHEV}</summary>'
            f'<ul>{links}</ul></details></div></nav>')


def crumbs_html(ctx, title):
    label, base, kids = section_of(ctx.url)
    parts = [f'<li><a href="{esc(ctx.href("/"))}">Home</a></li>']
    if label and ctx.url != base:
        parts.append(f'<li><a href="{esc(ctx.href(base))}">{esc(label)}</a></li>')
    short = next((kl for kl, kt in kids if kt == ctx.url), None) or (label if ctx.url == base else title)
    parts.append(f'<li aria-current="page">{esc(short)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def footer_html(ctx):
    global CREST_SRC
    CREST_SRC = ctx.root + "assets/leander-crest.png"
    def col(title, links):
        lis = "".join(f"<li>{nav_link(ctx, l, t)}</li>" for l, t in links)
        return f'<div><h2>{esc(title)}</h2><ul>{lis}</ul></div>'
    return (
        '<footer class="site-footer"><div class="wrap"><div class="footer-grid">'
        f'<div><a class="brand" href="{esc(ctx.href("/"))}" style="color:#fff">{crest_svg(44)}<span class="brand-text"><span class="brand-name">Leander</span><span class="brand-sub">Swimming Club, South London</span></span></a>'
        '<p style="margin-top:16px">Home pool: Ernest Bevin College, Beechcroft Road, Tooting SW17 7DF</p>'
        '<p><a class="hl" href="mailto:admin@leanderswim.com">admin@leanderswim.com</a></p>'
        '<p>Not-for-profit and volunteer-run since 1949.</p></div>'
        + col("Swim with us", [("Learn to Swim", "/learn"), ("Squads", "/squads"), ("Swim for Life", "/swim-for-life"), ("Book a squad trial", "/squads/book-a-trial"), ("Join us", "/join-us")])
        + col("Families", [("How galas work", "/galas/how-galas-work"), ("Fees and term dates", "/learn/fees-and-term-dates"), ("Kit by stage", "/learn/kit-by-stage"), ("Glossary", "/club/glossary"), ("Members' login", "TU:TeamUnify – members' login")])
        + col("Club", [("How the club works", "/club/how-the-club-works"), ("Coaches and team", "/club/coaches-and-team"), ("Volunteer and officiate", "/club/volunteer-and-officiate"), ("Where we swim", "/club/where-we-swim"), ("News", "/news"), ("Club shop", "TU:Leander club shop on printmykit")])
        + col("Policies", [("Safeguarding and policies", "/club/safeguarding-and-policies"), ("Privacy Notice", "TU:Privacy Notice"), ("Photography policy", "TU:Photography Policy")])
        + '</div>'
        f'<div class="footer-badges" aria-label="Accreditation"><span>Leander is a Swim England affiliated club, accredited under SwimMark and Clubmark.</span>'
        f'<span class="badges"><img src="{ctx.root}assets/swim-england-affiliated.png" width="150" height="65" alt="Swim England Affiliated Club">'
        f'<img src="{ctx.root}assets/swimmark.png" width="95" height="67" alt="SwimMark Essential Club">'
        f'<img src="{ctx.root}assets/clubmark.png" width="85" height="68" alt="Clubmark"></span></div>'
        '<div class="footer-welfare"><span><strong>Welfare.</strong> Worried about a swimmer? Talk to our Welfare Officers, Ruth Lock and Linda Kershaw. '
        'We follow Wavepower, Swim England\'s safeguarding policy.</span>'
        f'<span><a class="hl" href="mailto:welfare@leanderswim.com">welfare@leanderswim.com</a> <mark class="tbc">confirm welfare address</mark> · <a href="{esc(ctx.href("/club/safeguarding-and-policies"))}">Safeguarding</a></span></div>'
        '<div class="footer-bottom"><span>Leander Swimming Club · website prototype for committee feedback, November 2026</span>'
        '<span>Placeholder photos from Unsplash (see CREDITS.md in the repository)</span></div>'
        '</div></footer>')


def page_shell(ctx, title, desc, body, body_class=""):
    full_title = title if SITE_NAME in title or "Leander" in title else f"{title} | {SITE_NAME}"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(full_title)} (prototype)</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&amp;display=swap" rel="stylesheet">
<script>try{{var m=location.search.match(/[?&]style=([abcd])/);if(m)localStorage.setItem("lsc-style",m[1]);var v=localStorage.getItem("lsc-style");if(v&&v!=="a")document.documentElement.setAttribute("data-style",v);}}catch(e){{}}</script>
<link rel="stylesheet" href="{ctx.root}assets/site.css?v={VERSION}">
<link rel="icon" href="{ctx.root}assets/favicon.png" type="image/png">
</head>
<body class="{body_class}">
{header_html(ctx)}
{subnav_html(ctx)}
<main id="main" tabindex="-1">
{body}
</main>
{footer_html(ctx)}
<script src="{ctx.root}assets/site.js?v={VERSION}" defer></script>
</body>
</html>
"""


def render_page(meta, md, url):
    ctx = Ctx(url)
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    blocks = parse_blocks(md)
    # Hero: from H1 to first H2 (an H2 straight after H1 is the hero subtitle) or first hr
    h1 = None
    hero, rest = [], []
    i = 0
    while i < len(blocks) and not (blocks[i]["t"] == "h" and blocks[i]["level"] == 1):
        i += 1
    if i < len(blocks):
        h1 = blocks[i]["text"]
        i += 1
    sub = None
    if i < len(blocks) and blocks[i]["t"] == "h" and blocks[i]["level"] == 2:
        sub = blocks[i]["text"]
        i += 1
    while i < len(blocks) and not (blocks[i]["t"] == "h" and blocks[i]["level"] == 2) and blocks[i]["t"] != "hr":
        hero.append(blocks[i]); i += 1
    rest = blocks[i:]

    # hero pieces
    lede, photo, btns, extra, meta_line = [], None, [], [], None
    for b in hero:
        if b["t"] == "photo" and photo is None:
            photo = b
        elif b["t"] == "buttons":
            btns.extend(b["items"])
        elif b["t"] == "p" and len(lede) < 2 and not extra and not (b["lines"][0].startswith("*News")):
            lede.append(b)
        elif b["t"] == "p" and b["lines"][0].startswith("*News"):
            meta_line = b
        else:
            extra.append(b)
    cta = HERO_CTA.get(url)
    if cta:
        btn_html = '<div class="btn-row">' + "".join(link_html(ctx, esc(l), t, f"btn btn-{k}") for l, t, k in cta) + "</div>"
    elif btns:
        btn_html = render_buttons(ctx, btns)
    else:
        btn_html = '<div class="btn-row">' + link_html(ctx, "Join us", "/join-us", "btn btn-primary") + "</div>"
    # move any hero-listed links that were extra into extra
    sec_label, _, _ = section_of(url)
    eyebrow = esc(sec_label or "Leander")
    if url.startswith("/news/"):
        eyebrow = "News"
    lede_html = "".join(f'<p class="lede">{"<br>".join(inline(ctx, l) for l in b["lines"])}</p>' for b in lede)
    sub_html = f'<p class="sub">{inline(ctx, sub)}</p>' if sub else ""
    meta_html = f'<p class="meta">{inline(ctx, " ".join(meta_line["lines"]))}</p>' if meta_line else ""
    photo_html = f'<div class="hero-photo">{render_photo(ctx, photo["text"], eager=True)}</div>' if photo else ""
    hero_cls = "hero" + ("" if photo else " no-photo")
    out = [f'<section class="{hero_cls}" aria-labelledby="page-title"><div class="wrap"><div class="hero-text">'
           f'{crumbs_html(ctx, re.sub(r"<[^>]+>", "", h1 or ""))}<h1 id="page-title">{inline(ctx, h1 or meta.get("title", ""))}</h1>'
           f'{meta_html}{sub_html}{lede_html}{btn_html}</div>{photo_html}</div></section>']
    if extra:
        out.append(f'<section class="section tight" aria-label="At a glance"><div class="wrap"><div class="prose">{"".join(render_block(ctx, b) for b in extra)}</div></div></section>')

    # sections by H2
    sections = []
    cur = None
    loose = []
    for b in rest:
        if b["t"] == "h" and b["level"] == 2:
            cur = (b, [])
            sections.append(cur)
        elif cur is None:
            loose.append(b)
        else:
            cur[1].append(b)
    if [b for b in loose if b["t"] != "hr"]:
        out.append(f'<section class="section tight"><div class="wrap"><div class="prose">{"".join(render_block(ctx, b) for b in loose)}</div></div></section>')
    alt = True
    for h2, bl in sections:
        out.append(render_section(ctx, h2, bl, alt))
        alt = not alt
    body = "\n".join(out)
    title = meta.get("title", h1 or "")
    return ctx, page_shell(ctx, title, meta.get("seo_description", ""), body)


def load_pages():
    pages = []
    for f in sorted(CONTENT.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        meta, md = parse_front(text)
        url = meta.get("url", "").split(" ")[0].strip() or "/" + str(f.relative_to(CONTENT).with_suffix(""))
        pages.append((f, meta, md, url))
    return pages


def main():
    warnings = []
    count = 0
    for f, meta, md, url in load_pages():
        if url == "/":
            continue
        ctx, page = render_page(meta, md, url)
        p = out_path(url)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(page, encoding="utf-8")
        count += 1
        for w in ctx.warnings:
            warnings.append(f"{f.relative_to(ROOT)}: {w}")
    # Home
    ctx = Ctx("/")
    body = home_body(ctx, inline, render_photo, link_html, esc)
    (ROOT / "index.html").write_text(page_shell(ctx, "Leander Swimming Club | South London", "Learn to swim, race or swim for life at Leander Swimming Club in South London. Swim your best, among friends.", body, "home"), encoding="utf-8")
    count += 1
    ctx = Ctx("/style-options")
    out_path("/style-options").parent.mkdir(parents=True, exist_ok=True)
    out_path("/style-options").write_text(page_shell(ctx, "Corner and button options", "Design options for the prototype.", style_options_body(ctx, render_photo)), encoding="utf-8")
    count += 1
    print(f"Built {count} pages.")
    for w in sorted(set(warnings)):
        print("  warning:", w)


if __name__ == "__main__":
    main()
