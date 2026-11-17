"""Hand-built page parts: the home page and the lane-by-lane pathway timeline."""
import json
from html import escape as esc

# --------------------------------------------------------------------------
# Pathway timeline (ported from design-reference/pilot-pathway-timeline, restyled)
# --------------------------------------------------------------------------
LANES = [
    ("learn", "Learn", "The Academy, ages 5–10", [2, 3], "#FFFBEA"),
    ("compete", "Squads", "Train and race", [4, 5], "#F6F9FA"),
    ("race", "Compete", "The competition ladder", [6], "#FFFFFF"),
    ("talent", "Talent", "Swim England, by selection", [7], "#FFFBEA"),
    ("life", "Swim for Life", "Your way, any age", [8], "#F6F9FA"),
    ("beyond", "Beyond", "Teach, officiate, lead", [9, 10], "#FFFFFF"),
]

ITEMS = [
    dict(id="s12", lane="learn", row=2, a=5, b=5, title="Stages 1–2", sub="Age 5", ages="Around age 5", href="/learn/academy#the-stages",
         detail="Water confidence and safety come first, through games and teacher-led exercises. By the end of Stage 2, children swim up to 15m on their front and back without floats."),
    dict(id="s3", lane="learn", row=3, a=6, b=6, title="Stage 3", sub="Age 6", ages="Around age 6", href="/learn/academy#the-stages",
         detail="Correct technique on front crawl and backstroke (arms, legs, body position and breathing), building to 25m without help in shallow and deep water."),
    dict(id="s4", lane="learn", row=2, a=6, b=7, title="Stage 4", sub="Ages 6–7", ages="Around ages 6–7", href="/learn/academy#the-stages",
         detail="Breaststroke is introduced. Swimmers practise their strokes over 25m, and learn to dive in from the side and to glide and kick underwater afterwards."),
    dict(id="s5", lane="learn", row=3, a=7, b=8, title="Stage 5", sub="Ages 7–8", ages="Around ages 7–8", href="/learn/academy#the-stages",
         detail="Up to 50m without stopping. Butterfly is introduced, so swimmers build all four strokes, with feedback from their teacher in groups of up to ten."),
    dict(id="s6", lane="learn", row=2, a=8, b=9, title="Stage 6", sub="Ages 8–9", ages="Around ages 8–9", href="/learn/academy#the-stages",
         detail="Precise technique, legal turns including tumble turns, starts from the blocks and individual medley (all four strokes in one swim). More than 500m a lesson, twice a week."),
    dict(id="pre", lane="learn", row=3, a=9, b=9, title="Pre-Squad", sub="Around 9", ages="Around age 9", href="/learn/academy#the-stages",
         detail="The bridge into competitive swimming: all strokes, turns and IM, working off the pace clock, in two 45-minute sessions a week. Swimmers are then assessed for a squad place."),
    dict(id="sparks", lane="compete", row=4, a=8, b=9, title="Sparks", sub="Age to confirm", ages="Typical age to confirm", tbc=True, href="/squads/squad-standards#sparks",
         detail="Our youngest squad swimmers take their first steps in squad training.\nTypical age and entry standard still to be confirmed by the Head Coach."),
    dict(id="bronze", lane="compete", row=5, a=8, b=10, title="Bronze", sub="10 and under", ages="Around 10 and under", href="/squads/squad-standards#bronze",
         detail="No racing standard is needed, though a first gala helps. Swimmers can swim 200m freestyle without stopping and work on body position, streamlining, breathing, dives and pull-outs. Two sessions a week minimum, four recommended."),
    dict(id="silver", lane="compete", row=4, a=11, b=12, title="Silver", sub="11 girls · 12 boys", ages="Around 11 (girls), 12 (boys)", href="/squads/squad-standards#silver",
         detail="Swimmers have raced most official events and can swim 400m freestyle without stopping, with good dives and technique that holds up over 600m. Three sessions a week minimum, four recommended."),
    dict(id="gold", lane="compete", row=5, a=12, b=13, title="Gold", sub="12 girls · 13 boys", ages="From 12 (girls), 13 (boys)", href="/squads/squad-standards#gold",
         detail="Swimmers have raced every official event except 200m butterfly, 400m IM and the 800m and 1500m freestyle, and hold good technique over 1,000m. Four sessions a week minimum, five recommended."),
    dict(id="platinum", lane="compete", row=4, a=13, b=14, title="Platinum", sub="13 girls · 14 boys", ages="Around 13 (girls), 14 (boys)", href="/squads/squad-standards#platinum",
         detail="County qualifiers who have raced 16 of the 18 official events. They start to specialise in their best strokes and distances and to work more independently. Four sessions a week minimum, five recommended."),
    dict(id="mercury", lane="compete", row=5, a=15, b=18, title="Mercury", sub="14+ girls · 15+ boys", ages="Over 14 (girls), over 15 (boys)", href="/squads/squad-standards#mercury",
         detail="Regional qualifiers in at least two events. Training covers race strategy, breakouts and fine detail, and Mercury swimmers lead warm-ups for the younger squads. Six sessions a week minimum."),
    dict(id="galas", lane="race", row=6, a=8, b=9, title="Club galas", sub="From Bronze", ages="A guide, not a rule", href="/galas/how-galas-work",
         detail="Friendly competitions, including our own Academy galas and the Annual Squad Relay. Licensed meets run from Level 4 (for newer racers) to Level 1, and their times count for rankings."),
    dict(id="county", lane="race", row=6, a=10, b=12, title="Counties", sub="From age 10", ages="County times start at age 10", href="/squads/race-the-standards",
         detail="The Surrey County Age Group Championships. Swimmers need a county qualifying time, or a slightly slower consideration time if places allow. Race the Standards shows how close your swimmer is."),
    dict(id="region", lane="race", row=6, a=13, b=14, title="Regionals", sub="Platinum · Mercury", ages="A guide, not a rule", href="/squads/race-the-standards",
         detail="The Swim England London Region championships, with faster qualifying times than Counties."),
    dict(id="nats", lane="race", row=6, a=15, b=16, title="Nationals", sub="Mercury", ages="A guide, not a rule", href="/news/2025-26-season-round-up",
         detail="Swim England's national championships. Leander swimmers reached finals and won medals here in 2025/26."),
    dict(id="gb", lane="race", row=6, a=17, b=18, title="British / GB", sub="Our fastest", ages="A guide, not a rule", href="/news/2025-26-season-round-up",
         detail="British Championships, GB Trials and GB Summer Championships. In 2025/26, two Leander swimmers qualified for GB Trials and one won a medal at GB Summer Champs."),
    dict(id="cdc", lane="talent", row=7, a=11, b=12, title="County camp", sub="Selected · ages TBC", ages="Ages to confirm", tbc=True, href="#swim-england-talent-pathway",
         detail="County Development camps, run by Surrey, are the first step on Swim England's Talent pathway. Swimmers are selected on their results and World Aquatics points; you can't apply.\nTime and points guidance still to be confirmed with the Head Coach."),
    dict(id="rdc", lane="talent", row=7, a=13, b=14, title="Regional camp", sub="Selected · ages TBC", ages="Ages to confirm", tbc=True, href="#swim-england-talent-pathway",
         detail="Regional Development camps, run by Swim England London, for promising swimmers from across the region. Places are by selection only."),
    dict(id="nag", lane="talent", row=7, a=15, b=15, title="National camps", sub="Selected", ages="Ages to confirm", tbc=True, href="#swim-england-talent-pathway",
         detail="National Age Group development camps, run by Swim England's national talent team, for the fastest swimmers in each age group in England. Places are by selection only."),
    dict(id="dise", lane="talent", row=7, a=16, b=18, title="DiSE", sub="Ages 16–18", ages="Ages 16–18", tbc=True, href="#swim-england-talent-pathway",
         detail="The Diploma in Sporting Excellence is a two-year Swim England programme for talented 16 to 18 year olds, combining full-time education with high-level swimming support.\nHow swimmers qualify is still to be confirmed."),
    dict(id="diamond", lane="life", row=8, a=12, b=17, title="Diamond", sub="Teens · train without the race load", ages="Teenagers (ages to confirm)", tbc=True, href="/swim-for-life/diamond",
         detail="For teenagers who want to keep fit and stay with their friends without the competition load, and for squad swimmers easing off for GCSEs or A levels. One session a week minimum, three recommended. Swimmers can move back to a competitive squad later."),
    dict(id="masters", lane="life", row=8, a=18, b=18, title="Masters", sub="18+", ages="Adults 18+", href="/swim-for-life/masters",
         detail="For adults: fitness swimmers, triathletes and anyone coming back to the water. Two coached sessions a week, with coaches who include triathlon specialists."),
    dict(id="officiate", lane="beyond", row=9, a=15, b=17, title="Teach and officiate", sub="Judge 1 from 15", ages="From 15 (officiating)", tbc=True, href="/club/beyond-the-pool",
         detail="Squad swimmers can train as paid Academy teachers and gain officiating experience at our own Academy galas. The Judge 1 officials course is open from age 15.\nTeaching age, qualification and pay still to be confirmed."),
    dict(id="dofe", lane="beyond", row=10, a=15, b=17, title="DofE volunteering", sub="Silver and Gold", ages="Teenagers", tbc=True, href="/club/beyond-the-pool",
         detail="Students can arrange Duke of Edinburgh's Award volunteering by approaching the club. It can count towards the volunteering section; the level is confirmed by the student's DofE leader."),
    dict(id="uni", lane="beyond", row=9, a=18, b=18, title="University", sub="UK and US", ages="18+", href="/squads/university-and-scholarships",
         detail="Our squad swimmers regularly win places on university swimming programmes in the UK and the US. Families research each programme and contact coaches directly, and we help."),
]

LEGEND = [("learn", "Learn"), ("compete", "Squads"), ("race", "Competitions"), ("talent", "Swim England talent (by selection)"), ("life", "Swim for Life"), ("beyond", "Beyond the pool")]


def timeline_html(ctx, picked="bronze"):
    cells = []
    for lid, name, note, rows, bg in LANES:
        r0, r1 = rows[0], rows[-1] + 1
        cells.append(f'<div class="tl-lane-bg" aria-hidden="true" style="grid-row:{r0} / {r1};background:{bg}"></div>')
        cells.append(f'<div class="tl-lane-label" style="grid-row:{r0} / {r1}"><span class="n">{esc(name)}</span><span class="d">{esc(note)}</span></div>')
    cells.append('<div class="tl-age-label" aria-hidden="true">Age</div>')
    for a in range(5, 19):
        cells.append(f'<div class="tl-age" aria-hidden="true" style="grid-column:{a - 3}"><span>{"18+" if a == 18 else a}</span></div>')
    lane_names = {l[0]: l[1] for l in LANES}
    for it in ITEMS:
        on = "true" if it["id"] == picked else "false"
        label = f'{it["title"]}, {lane_names[it["lane"]]}, {it["ages"]}'
        cells.append(f'<button type="button" class="tl-chip tone-{it["lane"]}" data-id="{it["id"]}" aria-pressed="{on}" aria-controls="tl-detail" aria-label="{esc(label)}" '
                     f'style="grid-column:{it["a"] - 3} / {it["b"] - 2};grid-row:{it["row"]}"><span class="t">{esc(it["title"])}</span><span class="s">{esc(it["sub"])}</span></button>')
    sel = next(i for i in ITEMS if i["id"] == picked)
    data = {"lanes": lane_names, "items": [dict(i, href=ctx.href(i["href"]), linkText=f'More about {i["title"]}') for i in ITEMS]}
    legend = "".join(f'<span><i class="tone-{k}"></i>{esc(v)}</span>' for k, v in LEGEND)
    return f"""
<div class="tl" id="timeline">
  <div class="tl-head">
    <div><span class="eyebrow">The talent pathway</span><h3 style="font-size:clamp(26px,3vw,36px);margin-top:8px">Your swimmer's pathway, lane by lane</h3></div>
    <p style="margin:0;font-size:18px">The ages along the top are a guide. Every swimmer grows at their own pace. <strong>Select any step</strong> to see what it means.</p>
  </div>
  <p class="tl-scroll-hint">Scroll sideways to see the whole timeline, then tap a step.</p>
  <div class="tl-scroll" tabindex="0" role="region" aria-label="Pathway timeline by age (scrollable)">
    <div class="tl-grid" role="group" aria-label="Leander pathway timeline, ages 5 to 18 and over">{''.join(cells)}</div>
  </div>
  <div class="tl-detail" id="tl-detail" aria-live="polite">
    <div><span class="k">{esc(lane_names[sel['lane']])} · {esc(sel['ages'])}</span><h3>{esc(sel['title'])}</h3><span class="tl-tbc" {'' if sel.get('tbc') else 'hidden'}>Details to confirm</span></div>
    <div><p>{esc(sel['detail'])}</p><a class="tl-more text-cta" style="color:#FDD32A;display:inline-block;margin-top:14px" href="{esc(ctx.href(sel['href']))}">More about {esc(sel['title'])} →</a></div>
  </div>
  <div class="tl-legend" aria-hidden="true">{legend}</div>
  <script type="application/json" id="timeline-data">{json.dumps(data)}</script>
</div>"""


# --------------------------------------------------------------------------
# Home page
# --------------------------------------------------------------------------
def home_body(ctx, inline, render_photo, link_html, esc_):
    h = ctx.href

    def photo(desc):
        return render_photo(ctx, desc, brief=False)

    hero_ph = render_photo(ctx, "swimmers in lanes, squad training, seen from above", eager=True, brief=False)
    # pull the img out of the figure so the hero photo can be full-bleed with the waterline
    ways = [
        ("Ages 5 to 10", "Learn to swim",
         "Our Academy teaches children to swim well, the way competitive swimmers are taught, in small groups at Ernest Bevin. Plenty of families join simply to raise a strong, safe swimmer.",
         "About the Academy", "/learn/academy", "young swimmer gliding underwater academy kickboard lesson"),
        ("Sparks to Mercury", "Squads",
         "For young swimmers who want to train and race, from first club galas up to national championships. We publish what each squad expects, so you always know what comes next.",
         "See the pathway", "/squads/pathway", "race start dive gala blocks swimmers"),
        ("Teens and adults", "Swim for Life",
         "Diamond lets teenagers keep training without the pressure of racing, including through exams. Masters is for adults. Swimmers with a disability, including Down Syndrome, train with us in our squads.",
         "About Swim for Life", "/swim-for-life", "adult swimmers lap masters"),
    ]
    cards = "".join(
        f'<article class="card">{photo(p)}<div class="card-body"><span class="card-tag">{esc(tag)}</span><h3>{esc(t)}</h3><p>{esc(txt)}</p>'
        f'<p class="links-line"><a href="{h(href)}">{esc(link)}</a></p></div></article>' for tag, t, txt, link, href, p in ways)
    why = [
        ("Fit and strong for every sport", "Swimming works the heart, lungs and every major muscle group, and it's gentle on growing joints. That fitness carries straight over to rugby, hockey, netball, running and the rest."),
        ("Confidence they carry into school", "Setting a goal, training for it and racing under pressure builds a quiet self-belief. Children learn that steady effort pays off, and that habit serves them well in the classroom and in exams."),
        ("Friends across schools and ages", "Our swimmers come from schools all over South London, and the younger and older squads cheer each other on at galas. Many of those friendships last well beyond the pool."),
        ("Works alongside school sport", "Leander training fits around school swimming, water polo and swim teams, and a school squad session counts towards a swimmer's weekly training. Plenty of our swimmers do both."),
    ]
    why_html = "".join(f"<div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>" for a, b in why)
    steps = [
        ("1", "Academy", "ages 5 to 10", "Learn to swim properly, one stage at a time."),
        ("2", "Pre-Squad", "around 9", "The bridge into squad training."),
        ("3", "Squads", "Sparks to Mercury", "Train and race at club, county and regional level."),
        ("4", "Championships", "for our fastest", "Nationals and the GB pathway."),
        ("5", "Beyond the pool", "teenagers and up", "Teaching, officiating and swimming at university."),
    ]
    steps_html = "".join(f'<li class="{"last" if n == "5" else ""}"><span class="disc" aria-hidden="true">{n}</span><strong>{t}</strong><span class="age">{a}</span><span class="txt">{x}</span></li>' for n, t, a, x in steps)
    stats = [("55", "championship qualifications"), ("29", "finals reached"), ("25", "championship medals"), ("29", "club records broken")]
    stats_html = "".join(f'<div class="stat"><div class="n">{n}</div><div class="l">{l}</div></div>' for n, l in stats)
    gala_tbc = inline(ctx, "{{TBC: dates and venues for the three 2027 Leander galas}}")
    news = [
        ("9 January 2027", "Olympian Freya Anderson to lead a Leander clinic", "Team GB swimmer Freya Anderson (Tokyo and Paris) is coming to Ernest Bevin for a clinic with our Platinum and Mercury swimmers, with an education session from Dr Emily Jevons.", "/news/freya-anderson-clinic-preview", "Read the preview"),
        ("2025/26 season", "Our season in numbers", "55 championship qualifications, 29 finals and 25 medals, from the Surrey County Championships to GB Trials, and a squad programme that grew from 118 to 143 swimmers.", "/news/2025-26-season-round-up", "Read the round-up"),
        ("2027", "Three Leander galas", f"We're hosting two Academy galas for first-time racers and the Mercury Open, a Level 3 meet for developing swimmers. {gala_tbc}", "/galas", "See Leander galas 2027"),
    ]
    news_html = "".join(f'<article class="card"><div class="card-body"><span class="news-date">{d}</span><h3>{esc(t)}</h3><p>{x}</p><p class="links-line"><a href="{h(u)}">{esc(l)}</a></p></div></article>' for d, t, x, u, l in news)
    venues_tbc = inline(ctx, "{{TBC: confirm which squad venues are still in use}}")
    joins = [("My child is learning to swim", "/learn/waiting-list"), ("My child already swims", "/squads/book-a-trial#trial-form"), ("I'm an adult", "/join-us#adult"), ("A teenager who doesn't want to race", "/join-us#teen"), ("My swimmer has a disability", "/join-us#disability"), ("I'd like to volunteer", "/club/volunteer-and-officiate")]
    joins_html = "".join(f'<a href="{h(u)}">{esc(t)}</a>' for t, u in joins)
    quote_tbc = inline(ctx, "{{TBC: a parent or swimmer quote, in their own words, about the friends they've made and the feel of the club. Needs consent.}}")

    return f"""
<section class="home-hero" aria-labelledby="page-title"><div class="wrap">
  <div class="home-hero-photo">{hero_ph.replace('<figure class="photo-fig"><div class="photo">', '').replace('</div></figure>', '')}<canvas id="waterline" aria-hidden="true"></canvas></div>
  <div class="home-hero-card">
    <span class="eyebrow" style="text-transform:none;letter-spacing:0;font-weight:600">Leander Swimming Club · South London · since 1949</span>
    <h1 id="page-title">Swim your best, among friends</h1>
    <p class="lede">We help children become confident, fit, capable swimmers, with friendships and achievements that carry them through school and beyond. From first lessons at five to national finals, in a club that's friendly, supportive and proud of all of them.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="{h('/learn/waiting-list')}">Join the Academy waiting list</a>
      <a class="btn btn-secondary" href="{h('/squads/book-a-trial#trial-form')}">Book a squad trial</a>
    </div>
    <a class="text-cta" href="{h('/join-us#adult')}">Swimming for yourself? Try your first Masters session →</a>
  </div>
</div></section>

<section class="section ways" aria-labelledby="ways-h"><div class="wrap">
  <div class="section-head"><h2 id="ways-h">Where would your swimmer start?</h2></div>
  <div class="card-grid">{cards}</div>
</div></section>

<section class="section alt" aria-labelledby="why-h"><div class="wrap">
  <div class="section-head"><h2 id="why-h">What swimming at Leander gives you or your child</h2>
  <p>Swimming is a life skill first. Done well, it also shapes who you become: fit, confident, and used to working hard for something you care about. That's as true for our Masters swimmers as for our five-year-olds.</p></div>
  <div class="why-grid">{why_html}</div>
</div></section>

<section class="section" aria-labelledby="path-h"><div class="wrap">
  <div class="section-head"><h2 id="path-h">How the pathway works</h2>
  <p>Most swimmers start in the Academy and move up when they're ready. Swimmers can switch to Diamond or Masters at any point, and many of our older swimmers go on to teach in the Academy.</p></div>
  <ol class="path-steps">{steps_html}</ol>
  <div class="btn-row" style="margin-top:28px"><a class="btn btn-secondary" href="{h('/squads/pathway#timeline')}">Explore the full pathway, lane by lane</a><a class="text-cta" href="{h('/squads/squad-standards')}">What each squad expects →</a></div>
</div></section>

<section class="section navy" aria-labelledby="res-h"><div class="wrap results">
  <div><h2 id="res-h">A good year in the pool</h2>
  <p style="font-size:19px;margin-top:16px">In 2025/26 our swimmers qualified for championships 55 times, reached 29 finals and won 25 medals. Two raced at GB Trials, and between them our swimmers broke 29 club records.</p>
  <p class="proud">We're just as proud of the eight-year-old who finally nails a tumble turn.</p>
  <p><a href="{h('/news/2025-26-season-round-up')}" style="color:#fff;font-weight:700">Read the season round-up →</a></p></div>
  <div class="stats">{stats_html}</div>
</div></section>

<section class="section" aria-labelledby="beyond-h"><div class="wrap two-col">
  {render_photo(ctx, "teenage swimmer on poolside holding a kickboard for a younger group, teaching lesson", brief=False)}
  <div class="prose"><h2 id="beyond-h">Beyond the pool</h2>
  <p>Swimming at Leander leads to more than times. Our squad swimmers can train as paid Academy teachers, learn to officiate at our own galas, volunteer towards their Duke of Edinburgh's Award, lead warm-ups for the younger squads, and take their swimming on to university.</p>
  <p class="links-line"><a href="{h('/club/beyond-the-pool')}">What swimming at Leander leads to</a></p></div>
</div></section>

<section class="section alt" aria-labelledby="news-h"><div class="wrap">
  <div class="section-head"><h2 id="news-h">Galas and news</h2></div>
  <div class="news-list">{news_html}</div>
  <p class="links-line" style="margin-top:24px"><a href="{h('/news')}">All news and results</a>{link_html(ctx, 'Gala calendar on TeamUnify', 'TU:TeamUnify – calendar')}</p>
</div></section>

<section class="section" aria-labelledby="club-h"><div class="wrap two-col">
  <div class="prose"><h2 id="club-h">A proper club, run by the people in it</h2>
  <p>Alongside training there's the Annual Squad Relay, where nine-year-olds race alongside seventeen-year-olds, Academy galas for first-time racers, a summer social and our Tenerife training camp, helped along by cake sales on Saturday mornings at Ernest Bevin.</p>
  <p>Leander is run by volunteers, so if you can spare a little time, we'd love your help.</p>
  <p class="links-line"><a href="{h('/club/how-the-club-works')}">How the club works</a><a href="{h('/club/volunteer-and-officiate')}">Volunteer with us</a></p></div>
  <figure class="quote" style="background:var(--cream)"><blockquote>{quote_tbc}</blockquote><figcaption>Name and role, e.g. Academy parent since 2022</figcaption></figure>
</div></section>

<section class="section alt" aria-labelledby="where-h"><div class="wrap two-col">
  <div class="prose"><h2 id="where-h">Where we swim</h2>
  <p>Our home pool is <strong>Ernest Bevin College, Beechcroft Road, Tooting SW17 7DF</strong>, where the Academy is taught. Our squads also train at other pools across South London, so families come to us from all over. {venues_tbc}</p>
  <p class="links-line"><a href="{h('/club/where-we-swim')}">Venues and session times</a></p></div>
  {render_photo(ctx, "empty indoor pool with lane ropes, no people", brief=False)}
</div></section>

<section class="section" aria-labelledby="join-h"><div class="wrap"><div class="band">
  <div class="band-text"><h2 id="join-h">Come and swim with us</h2>
  <p style="font-size:18px">Tell us who's swimming and we'll point you to the right place. There's often a waiting list, and we'll be upfront about how long it might take.</p>
  <p>Questions? Email <a href="mailto:admin@leanderswim.com">admin@leanderswim.com</a></p></div>
  <div class="join-routes">{joins_html}</div>
</div></div></section>
"""
