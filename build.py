#!/usr/bin/env python3
"""Build the City of San Ramon Aquatics preview: Aquatics, the San Ramon Olympic Pool & Aquatic Park, the Dougherty Valley
Aquatic Center, Lap Swim, Teams & Other Services, Classes, and Pool Closure Dates, with every hour, practice, class and
closure read live from Pool Relay by finder.js (#finder, #today, #week, data-live). Nothing about WHEN a pool is open is
typed here; only prices, ages, policies and facts about the water.
Run: python3 build.py"""
import hashlib, html, json

E = html.escape
V = {"srop": "crpwBd7tJOeik4pmuAR3ID", "dvac": "v0jSpnBF5QDS1Yb8kKWGnq"}  # Pool Relay share tokens, lane by lane
FEED = ",".join(V.values())
BOTH = "srop|dvac"
SITE = "https://www.sanramon.ca.gov/our_city/departments_and_divisions/parks_community_services/aquatics"
REG = "https://www.sanramonrecguide.com"
POOLS = [
    dict(slug="srop", name="San Ramon Olympic Pool & Aquatic Park", short="Olympic Pool", facility="San Ramon Olympic Pool & Aquatic Park",
         area="San Ramon", kind="yearRound", address="9900 Broadmoor Dr, San Ramon, CA 94583", phone="(925) 973-3240", href="olympic-pool.html",
         blurb="A 50-meter Olympic pool with diving boards, a 25-yard lap pool and the Aquatic Park play pool, next to California High "
               "School. Lap swim, swim teams, Masters and aqua aerobics, year-round."),
    dict(slug="dvac", name="Dougherty Valley Aquatic Center", short="Dougherty Valley", facility="Dougherty Valley Aquatic Center",
         area="San Ramon", kind="yearRound", address="10550 Albion Rd, San Ramon, CA 94582", phone="(925) 973-3335", href="dougherty-valley.html",
         blurb="A 50-meter Olympic pool with diving boards and a water play pool for small children, next to Dougherty Valley High "
               "School. Opened in 2007."),
]

def live(mode, pool, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    view = FEED if "|" in pool else V[pool]
    return f'data-live="{mode}" data-view="{view}" data-pool="{pool}"{attrs}'

MENU = [("Aquatics", "index.html", 0), ("San Ramon Olympic Pool", "olympic-pool.html", 1),
        ("Dougherty Valley Aquatic Center", "dougherty-valley.html", 1), ("Lap Swim", "lap-swim.html", 1),
        ("Swim Lessons", None, 1), ("Recreation Swim", None, 1), ("Classes & Camps", "classes.html", 1),
        ("Teams & Other Services", "teams.html", 1), ("Pool Closure Dates", "closures.html", 1), ("Training & Employment", None, 1)]

VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]  # cache-busts both on change

def page(file, title, body, contact=None):
    menu = "".join(f'<a class="{"sub" if sub else ""}{" here" if href == file else ""}" href="{href or "#"}">{E(label)}</a>'
                   for label, href, sub in MENU)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a City of San Ramon website. A mock-up of {SITE}
     with the City's two aquatic centers on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | City of San Ramon Aquatics preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Condensed:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a City of San Ramon page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">the City's Aquatics pages</a> with both aquatic centers on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><small>City of San Ramon</small><span>Parks &amp; Community Services</span></a>
  <div class="right"><div class="util"><span>Register at SanRamonRecGuide.com</span><span>Contact</span><span>Search</span></div>
    <nav aria-label="Main"><span>Our City</span><span>Residents</span><span>Business</span><span>Visitors</span><span>How Do I…</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>Aquatics</h2><nav aria-label="Aquatics">{menu}</nav></aside>
  <main class="main"><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact</h2>{contact or CONTACT}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>City of San Ramon</h4><p>7000 Bollinger Canyon Rd, San Ramon, CA 94583<br>(925) 973-2500<br>aquatics@sanramon.ca.gov</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with the City of San Ramon. Schedules entered on November 3, 2026 from the City's Fall Swim Hours, Classes &amp; Camps and Pool Closure Dates pages, and from San Ramon Valley Aquatics' and ElitSwim's practice schedules. Which pool and lanes each program uses is our estimate until the City's lane plan is entered.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps([{k: v for k, v in p.items() if k != "blurb"} for p in POOLS])};</script>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>San Ramon Olympic Pool</b>9900 Broadmoor Dr<br>San Ramon, CA 94583<br>(925) 973-3240</p>
<p><b>Dougherty Valley Aquatic Center</b>10550 Albion Rd<br>San Ramon, CA 94582<br>(925) 973-3335</p>
<p><b>Email</b>aquatics@sanramon.ca.gov</p><p><b>Pool rentals</b>SRAquaticRental@sanramon.ca.gov</p>"""

def frame(pool, title, height=820):
    return f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{V[pool]}" height="{height}" title="{E(title)}" loading="lazy"></iframe></div>'

# ── Aquatics ─────────────────────────────────────────────────────────────────
cards = "".join(f"""<div class="card"><h3><a href="{p['href']}">{E(p['name'])}</a></h3><p class="small muted">{E(p['address'])} · {E(p['phone'])}</p>
  <p>{E(p['blurb'])}</p>
  <p class="small" {live("swims", p['slug'])}>…</p></div>""" for p in POOLS)
page("index.html", "Aquatics", f"""
    <p class="lede">The City of San Ramon runs two outdoor aquatic centers, both heated to 80–82 degrees year-round. Every time on these pages
      comes from the pools' live schedule, so when the City changes it, these pages change with it.</p>
    <h2 id="find">Where can I swim right now?</h2>
    <div id="finder" class="finder" data-view="{FEED}" data-all-label="Both centers"></div>
    <h2>The aquatic centers</h2>
    <div class="cards">{cards}</div>
    <div class="adjusted" {live("closures", BOTH, ahead=120)} hidden></div>

    <h2>Who can swim</h2>
    <p>Lap swim is drop-in: pay at the front desk with a swim pass, card or cash. One All Swim Pass covers lap swim, water walking and, in
      summer, recreation swim at either center. See <a href="lap-swim.html">Lap Swim</a> for prices.</p>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>Lap swim hours in a picture.</b> The fall hours are a flyer image on the Lap Swim page, readable only by eye and only until it is
          replaced. Here they are text that updates itself.</li>
        <li><b>An empty Aquatics Calendar.</b> The City's aquatics calendar shows no events at all. Here every lap swim, class, practice and
          closure is on one calendar.</li>
        <li><b>Teams with no times.</b> Teams &amp; Other Services lists eleven rental groups but none of their practice times; those live on
          each club's own website. Here practices sit beside lap swim, pool by pool.</li>
        <li><b>Closures in a separate list.</b> Holidays and special events are on their own page. Here a closure also clears that day from every
          schedule on the site.</li>
      </ul>
    </div>
""")

# ── San Ramon Olympic Pool ───────────────────────────────────────────────────
sr = POOLS[0]
page("olympic-pool.html", "San Ramon Olympic Pool & Aquatic Park", f"""
    <p class="lede">{E(sr['blurb'])}</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['srop']}" data-pool="srop"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Lap swim</h2>
        <div {live("hours", "srop", format="dl", group="San Ramon Aquatics / Lap Swim", whole=0)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", "srop", group="San Ramon Aquatics / Lap Swim")} hidden></div>
        <p class="small muted" style="margin:6px 0 0">Locker rooms close 20 minutes after lap swim ends.</p>
      </aside>
    </div>
    <h2>This week, pool by pool</h2>
    <div id="week" data-view="{V['srop']}" data-pool="srop" data-pools="Olympic Pool|Lap Pool"><p class="muted">Loading the week…</p></div>
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see who is in each of the Olympic Pool's short-course lanes and the Lap Pool's eight lanes.</p>
    {frame("srop", "San Ramon Olympic Pool & Aquatic Park, lane by lane")}
    <h2>The pools</h2>
    <div class="facts">
      <div><h3>Olympic Pool</h3><ul><li>50 meters long course, or 25 yards short course</li><li>4 to 12 feet deep · 680,000 gallons · 80°F</li>
        <li>Two 3-meter and two 1-meter diving boards</li><li>Colorado Time Systems scoreboard for meets</li></ul></div>
      <div><h3>Lap Pool</h3><ul><li>25 yards · 3.5 to 6 feet deep</li><li>187,000 gallons · 82°F</li><li>Behind the picnic area, to the left of the lobby</li></ul></div>
      <div><h3>Aquatic Park</h3><ul><li>Play pool with a new play structure · zero-depth entry to 1.5 feet</li><li>Home of the Splash N' Dash inflatable obstacle course</li><li>Recreation swim, May to September</li></ul></div>
    </div>
    <p class="small muted">Full-service locker rooms with showers, lockers (bring a lock) and suit spinners, and a family changing room. Every pool has
      easy-entry stairs, a swim lift and water wheelchairs. Established 1975; the aquatic center building was completed in 1999.</p>
""", f"""<p><b>San Ramon Olympic Pool</b>{E(sr['address'])}<br>{E(sr['phone'])}</p><p><b>Email</b>aquatics@sanramon.ca.gov</p>
<p><b>Nearby</b>CVS at Broadmoor Dr and Alcosta Blvd</p>""")

# ── Dougherty Valley ─────────────────────────────────────────────────────────
dv = POOLS[1]
page("dougherty-valley.html", "Dougherty Valley Aquatic Center", f"""
    <p class="lede">{E(dv['blurb'])}</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Today</h2>
        <div id="today" data-view="{V['dvac']}" data-pool="dvac"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>In the pool</h2>
        <div {live("hours", "dvac", format="dl")}><p class="muted">…</p></div>
        <p class="small muted" style="margin:0">First session to last. Team practices are on <a href="teams.html">Teams &amp; Other Services</a>.</p>
        <div class="adjusted" {live("closures", "dvac", ahead=120)} hidden></div>
      </aside>
    </div>
    <h2>This week</h2>
    <div id="week" data-view="{V['dvac']}" data-pool="dvac"><p class="muted">Loading the week…</p></div>
    <h2>Lane by lane</h2>
    {frame("dvac", "Dougherty Valley Aquatic Center, lane by lane", 720)}
    <h2>The pools</h2>
    <ul><li>50-meter pool, swum 50 meters long course or 25 yards short course · 4 to 14 feet deep · diving boards</li>
      <li>Play pool for small children · zero-depth entry to 3 feet</li><li>Picnic areas, available to reserve</li>
      <li>Full-service, ADA-accessible locker rooms with showers, lockers and suit spinners</li></ul>
""", f"""<p><b>Dougherty Valley Aquatic Center</b>{E(dv['address'])}<br>{E(dv['phone'])}</p><p><b>Email</b>aquatics@sanramon.ca.gov</p>
<p><b>Nearby</b>Safeway on Bollinger Canyon Rd</p>""")

# ── Lap Swim ─────────────────────────────────────────────────────────────────
page("lap-swim.html", "Lap Swim", f"""
    <p class="lede">Year-round lap swimming in pools heated to 80 degrees. Beginners to experts are welcome, and you can come any time during
      lap swim hours. Lanes are usually available for water walking, but not guaranteed.</p>
    <div class="top2">
      <aside class="hours"><h2>Lap swim hours</h2>
        <p style="margin:0" {live("when", BOTH, group="San Ramon Aquatics / Lap Swim")}>…</p>
        <div class="adjusted" {live("exceptions", "srop", group="San Ramon Aquatics / Lap Swim")} hidden></div></aside>
      <section class="now"><h2>Daily swim &amp; All Swim Pass</h2>
        <table class="fees"><tr><th>Daily swim</th><td>$8</td></tr><tr><th>10 swims (5% off)</th><td>$76</td></tr><tr><th>20 swims (10% off)</th><td>$144</td></tr>
          <tr><th>40 swims (15% off)</th><td>$272</td></tr><tr><th>60 swims (20% off)</th><td>$384</td></tr></table>
        <p class="small muted" style="margin:6px 0 0">Passes are non-refundable, valid for a year, one entry per person per visit. Buy at
          <a href="{REG}" target="_blank" rel="noopener">SanRamonRecGuide.com</a>.</p></section>
    </div>
    <h2>Before you swim</h2>
    <ul><li>Lap lanes are for exercise only; no recreational swimming, horseplay, coaching or lessons.</li>
      <li>Children 12 and under swim with an adult or guardian watching; depending on ability, a chaperone may need to be in the water.</li>
      <li>Share a lane when it's busy: split it with one other swimmer, or circle swim with more, keeping to the right.</li>
      <li>If others are waiting, keep to 30 minutes or invite them to share.</li>
      <li>Kickboards are provided; bring your own goggles, pull buoys and fins.</li></ul>
    <h2>Lane by lane</h2>
    <p class="small muted">Which lanes lap swim has, beside the teams and classes sharing the water.</p>
    {frame("srop", "San Ramon Olympic Pool & Aquatic Park, lane by lane")}
""")

# ── Teams & Other Services ───────────────────────────────────────────────────
SRVA = "San Ramon Valley Aquatics"
GROUPS = [("Senior Performance", "Coach David"), ("Senior 2", "Coach Patrick"), ("Senior 1", "Coach Natalie"),
          ("Pre-Senior 2", "Coach Jake"), ("Pre-Senior 1", "Coach Patrick"), ("Competitive 2", "Coach Jake"),
          ("Competitive 1", "Coach Danielle"), ("Novice 2", "Coach Audra"), ("Novice 1", "Coach Audra"),
          ("Varsity 2", "Coach Danielle"), ("Varsity 1", "Coach Audra")]
def row(name, note, group):
    return (f'<tr><th>{E(name)}<div class="small muted" style="font-weight:400">{E(note)}</div></th>'
            f'<td class="when" {live("when", BOTH, group=group, gap=-1)}>…</td></tr>')
srva_rows = "".join(row(n, c, f"{SRVA} / {n}") for n, c in GROUPS)
OTHERS = [("San Ramon Aqua Bears", "VSL Swim League · seasonal, May–July"),
          ("San Ramon Aquacats", "VSA Swim League · May–July, with a spring clinic and fall program"),
          ("California High School", "Swimming February–May · water polo August–November"),
          ("Dougherty Valley High School", "Swimming February–May · water polo August–November"),
          ("California Diving Academy", "Springboard diving, USA Diving & AAU · Head Coach Eric Holzheimer"),
          ("Nu Wave Water Aerobics", "Contact: Sue Morrison"),
          ("Dive N Trips", "Basic and instructor-level PADI scuba courses · Contact: Michael Shahani")]
page("teams.html", "Teams & Other Services", f"""
    <p class="lede">Swim teams, Masters, diving, water polo and scuba groups rent the City's pools. Practice times below come from the same
      live schedule as the pool calendars, so they show which center and pool each group is in.</p>
    <h2>San Ramon Valley Aquatics</h2>
    <p>Year-round competitive swimming, Pacific Swimming · Head Coach David Tambuwun · one of ASCA's top 50 USA age-group teams.</p>
    <div class="tblwrap"><table class="prog">{srva_rows}</table></div>
    <h2>San Ramon Valley Aquatics Masters</h2>
    <p>Adults of every level, Pacific Masters Swimming · Head Coach Greg Lynch · about 80 swimmers since 2012.</p>
    <div class="tblwrap"><table class="prog">{row("Workouts", "Trial swims by appointment", f"{SRVA} / Masters")}</table></div>
    <h2>ElitSwim</h2>
    <p>Year-round competitive swimming, Pacific Swimming · Head Coach Paschalis Ntatsos. Pre-competitive training for ages 6 and up.</p>
    <div class="tblwrap"><table class="prog">{row("Pre-Competitive", "Times shift a little around high school programs", "ElitSwim / Pre-Competitive")}</table></div>
    <h2>Other groups using the pools</h2>
    <div class="tblwrap"><table class="prog">{''.join(f'<tr><th>{E(n)}</th><td>{E(d)}</td></tr>' for n, d in OTHERS)}</table></div>
    <p class="small muted">These groups haven't published practice times. When they are entered, they appear here and on the pool calendars.
      To rent pool space for your team, email SRAquaticRental@sanramon.ca.gov.</p>
""")

# ── Classes ──────────────────────────────────────────────────────────────────
page("classes.html", "Classes & Camps", f"""
    <p class="lede">Aqua aerobics, CPR and lifeguard courses, and summer camps at the pools. Days and times below come from the live schedule;
      register at <a href="{REG}" target="_blank" rel="noopener">SanRamonRecGuide.com</a>.</p>
    <h2>Aqua Aerobics</h2>
    <p>A total-body workout set to music: the water's buoyancy is easy on joints, and its resistance builds strength. Shallow-water classes
      are low impact, and no swimming experience is needed.</p>
    <div class="tblwrap"><table class="prog">
      <tr><th>Shallow water</th><td class="when" {live("when", BOTH, group="San Ramon Aquatics / Aqua Aerobics", gap=-1)}>…</td></tr>
      <tr><th>Ages</th><td>18 and up</td></tr><tr><th>Cost</th><td>$30–$40 residents, $37.50–$50 non-residents; new sessions each month</td></tr></table></div>
    <h2>CPR, First Aid, Lifeguard &amp; Water Safety Instructor</h2>
    <p>Community CPR/AED and First Aid (ages 12 and up, $80 residents / $100 non-residents) runs at the Adams Safety Training Center, with
      2027 dates coming soon. Lifeguard, Lifeguard Instructor and Water Safety Instructor courses are listed under Training &amp; Employment.</p>
    <h2>Aquatic Summer Camps</h2>
    <p>Junior Lifeguards, Star Guards and more return next summer; details on SanRamonRecGuide.com from mid-February.</p>
""")

# ── Pool Closure Dates ───────────────────────────────────────────────────────
page("closures.html", "Pool Closure Dates", f"""
    <p class="lede">The days normal programming is cancelled for holidays and special events. These come from the live schedule, so a
      closure added there appears here and clears that day from every schedule on this site.</p>
    <div class="top2">
      <section class="now"><h2>San Ramon Olympic Pool</h2><div class="small" {live("closures", "srop", ahead=400, label="Closed")}>No closures scheduled.</div></section>
      <section class="now"><h2>Dougherty Valley Aquatic Center</h2><div class="small" {live("closures", "dvac", ahead=400, label="Closed")}>No closures scheduled.</div></section>
    </div>
""")
print("built 7 pages, assets", VER)
