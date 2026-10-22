#!/usr/bin/env python3
"""Builds the A-one Caterers static site.
dist/      -> full HTML pages, ready to host anywhere
artifact/  -> same pages; index has no document skeleton (for preview publishing)
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")

PHONE = "+91 95445 41075"
PHONE_RAW = "919544541075"
IG_URL = "https://www.instagram.com/aone_caterers_/"
IG_HANDLE = "@aone_caterers_"
PHONES = [("+91 95445 41075","919544541075"),("+91 99953 27413","919995327413"),("+91 70126 90063","917012690063")]
def phone_links(sep="<br>"):
    return sep.join(f'<a href="tel:+{r}">{n}</a>' for n,r in PHONES)

# Real A-one event photos (assets/img/events). Add new ones here, then use the key in media().
IMG = {
    "counter-fruit":  "centre-counter-fruit-carving",
    "counter-blue":   "centre-counter-blue-trees",
    "counter-chef":   "centre-counter-chef",
    "hall-buffet":    "hall-buffet-line",
    "buffet-wide":    "buffet-line-wide",
    "buffet-night":   "buffet-line-night",
    "buffet-labels":  "buffet-dish-labels",
    "gold-chafers":   "gold-chafers-row",
    "gold-chef":      "gold-buffet-line-chef",
    "clay-pots":      "clay-pot-counter",
    "outdoor":        "outdoor-buffet-arches",
    "d-umali":        "dessert-umali-table",
    "d-pannacotta":   "dessert-pannacotta",
    "d-pudding":      "dessert-puddings-eclairs",
    "d-falooda":      "dessert-falooda-cake",
    "d-sago":         "dessert-rose-sago",
    "d-sundae":       "dessert-hazelnut-sundae",
    "d-brownie":      "dessert-brownie-tarts",
}

def media(key, label, cls="", w=None, alt=None, pos=None, style=None):
    st = f' style="object-position:{pos}"' if pos else ""
    box = f' style="{style}"' if style else ""
    return (f'<div class="media {cls}"{box} data-label="{label}">'
            f'<img src="assets/img/events/{IMG[key]}.jpg" alt="{alt or label}" loading="lazy" decoding="async"{st}></div>')

# Instagram reels shown on the Home page.
# Drop the reel videos into src/assets/video/ as reel-1.mp4 ... reel-4.mp4 (newest first)
# and paste each reel's Instagram link below. Cards without a video show the poster
# photo and open Instagram instead.
REELS = [
    {"file": "reel-1.mp4", "poster": "reels/reel-1", "link": "https://www.instagram.com/reel/DXHUDw0k05S/", "title": "Wedding day buffet"},
    {"file": "reel-2.mp4", "poster": "reels/reel-2", "link": "https://www.instagram.com/reel/CvPrpKZJLu9/", "title": "Biriyani &amp; live counters"},
    {"file": "reel-3.mp4", "poster": "reels/reel-3", "link": "", "title": "Reception night counters"},
    {"file": "reel-4.mp4", "poster": "reels/reel-4", "link": "", "title": "Mocktails &amp; desserts"},
]

def reels_section():
    cards = []
    for i, r in enumerate(REELS):
        has_video = os.path.exists(os.path.join(SRC, "assets", "video", r["file"]))
        poster = f"assets/img/{r['poster']}.jpg" if "/" in r["poster"] else f"assets/img/events/{r['poster']}.jpg"
        link = r["link"] or IG_URL
        if has_video:
            inner = (f'<video class="reel-video" src="assets/video/{r["file"]}" poster="{poster}" muted loop playsinline preload="metadata" aria-label="A-one wedding reel {i+1}"></video>'
                     f'<button class="reel-sound" type="button" aria-pressed="false" aria-label="Unmute">'
                     f'<svg class="i-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4z"/><path d="m22 9-6 6M16 9l6 6"/></svg>'
                     f'<svg class="i-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>'
                     f'<span>Tap for sound</span></button>'
                     f'<button class="reel-play" type="button" aria-label="Play">▶</button>')
        else:
            inner = (f'<img src="{poster}" alt="A-one wedding reel {i+1}" loading="lazy" decoding="async">'
                     f'<span class="reel-play static" aria-hidden="true">▶</span>')
        ig = f'<a class="reel-ig" href="{link}" target="_blank" rel="noopener" aria-label="Open this reel on Instagram">{ICON["ig"]}</a>'
        if has_video:
            cards.append(f'<div class="reel" data-reveal="{i*80}"><div class="reel-frame">{inner}{ig}</div></div>')
        else:
            cards.append(f'<div class="reel no-video" data-reveal="{i*80}"><a class="reel-frame" href="{link}" target="_blank" rel="noopener" aria-label="Watch on Instagram">{inner}</a></div>')
    return f'''<section class="section reels-band"><div class="wrap">
  <div class="head center"><span class="eyebrow">On Instagram</span><h2>Inside our weddings</h2><p class="lead">The food, the service and the stage, as our guests see it. Tap any reel for sound.</p></div>
  <div class="reels">{"".join(cards)}</div>
  <div class="reels-cta"><a class="btn btn-gold ig-btn" href="{IG_URL}" target="_blank" rel="noopener">{ICON["ig"]} Follow {IG_HANDLE}</a><span>New reels from every event</span></div>
</div></section>'''

ICON = {
 "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20c0-9 6-15 16-16-1 10-7 16-16 16Z"/><path d="M4 20 14 10"/></svg>',
 "chef": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 13.9V20h12v-6.1A4 4 0 0 0 17 6a5 5 0 0 0-10 0 4 4 0 0 0-1 7.9Z"/><path d="M6 17h12"/></svg>',
 "tray": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17h18M4 17a8 8 0 0 1 16 0M12 7V5M10 5h4M2 20h20"/></svg>',
 "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/></svg>',
 "people": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2a5 5 0 0 1 5.5 5.8"/></svg>',
 "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6Z"/><path d="m9 12 2 2 4-4"/></svg>',
 "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18H6z"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2Z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4a.5.5 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .1-1.2c0-.2-.2-.3-.4-.4Z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H8v4h2v8h4v-8h3l1-4h-4V8.5a.5.5 0 0 1 .5-.5Z"/></svg>',
}

NAV = [("index.html","Home"),("about.html","About"),("services.html","Services"),("gallery.html","Gallery"),("contact.html","Contact")]

def header(active):
    items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a></li>' for h,t in NAV)
    return f'''<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="index.html" aria-label="A-one Caterers and Events home">
      <img src="assets/img/aone-logo.png" alt="A-one Caterers and Events logo" width="54" height="54">
      <span class="brand-text"><b>A-one</b><small>Caterers &amp; Events</small></span>
    </a>
    <nav aria-label="Main">
      <ul class="menu" id="menu">{items}<li class="menu-cta"><a href="contact.html">Get a quote</a></li></ul>
    </nav>
    <a class="btn btn-primary nav-cta" href="contact.html">Get a quote {ICON["arrow"]}</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu"><span></span></button>
  </div>
</header>
<div class="scrim"></div>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/aone-logo.png" alt="" width="72" height="72"><span class="brand-text"><b>A-one</b><small>Caterers &amp; Events</small></span></a>
        <p class="script">“We know how you love it.”</p>
        <p>Home-style Kerala cooking and full event catering since 1999. Based in Kothamangalam, catering across Kerala.</p>
        <div class="social">
          <a href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON["wa"]}</a>
          <a href="{IG_URL}" target="_blank" rel="noopener" aria-label="Instagram {IG_HANDLE}">{ICON["ig"]}</a>
          <a href="#" aria-label="Facebook">{ICON["fb"]}</a>
        </div>
      </div>
      <div><h4>Explore</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)}</ul></div>
      <div><h4>We cater</h4><ul><li><a href="services.html#weddings">Weddings</a></li><li><a href="services.html#sadya">Kerala Sadya</a></li><li><a href="services.html#celebrations">Family celebrations</a></li><li><a href="services.html#corporate">Corporate events</a></li><li><a href="services.html#outdoor">Outdoor &amp; live counters</a></li><li><a href="services.html#desserts">Dessert stations</a></li></ul></div>
      <div><h4>Talk to us</h4><ul>
        <li><span>Call us</span><br>{phone_links()}</li><li><span>Instagram</span><br><a href="{IG_URL}" target="_blank" rel="noopener">{IG_HANDLE}</a></li><li><span>WhatsApp</span><br><a href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener">{PHONE}</a></li>
        <li><span>Based in</span><br>Kothamangalam, Ernakulam, Kerala</li>
        <li><span>Bookings</span><br>Open all days</li>
      </ul></div>
    </div>
    <div class="copy"><span>© <span data-year>2026</span> A-one Caterers &amp; Events. All rights reserved.</span><span>Website by Codescape Innovations</span></div>
  </div>
</footer>
<a class="wa" href="https://wa.me/{PHONE_RAW}?text=Hi%20A-one%20Caterers%2C%20I%27d%20like%20to%20know%20more%20about%20your%20catering." target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON["wa"]}<span>Chat on WhatsApp</span></a>'''

HEAD = '''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,500;1,600&family=Figtree:wght@400;500;600&family=Marcellus&display=swap">
<link rel="stylesheet" href="assets/css/style.css">'''

def page_hero(eyebrow, title, text, crumb):
    return f'''<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="index.html">Home</a> / {crumb}</div>
    <span class="eyebrow">{eyebrow}</span>
    <h1>{title}</h1>
    <p>{text}</p>
  </div>
</section>'''

CTA = f'''<section class="section"><div class="wrap">
  <div class="cta" data-reveal>
    <div><h2>Planning a wedding, sadya or party?</h2><p>Tell us the date, guest count and venue. We'll come back with a menu and a clear quote.</p></div>
    <div class="actions"><a class="btn btn-gold" href="contact.html">Get a quote {ICON["arrow"]}</a><a class="btn btn-ghost" href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener">WhatsApp us</a></div>
  </div>
</div></section>'''

# ---------------- Pages ----------------
HOME = f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <span class="eyebrow">Caterers &amp; Events · Since 1999</span>
    <h1>Let us be your <em>personal chef</em> for your special occasion</h1>
    <p class="lead">From a wedding sadya for 1,000+ guests to a birthday party for 10, A-one cooks, serves and manages the food so you can enjoy the day with your people.</p>
    <div class="hero-actions"><a class="btn btn-primary" href="contact.html">Plan my event {ICON["arrow"]}</a><a class="btn btn-ghost" href="services.html">See our menus</a></div>
    <div class="hero-meta"><div><b>1999</b><span>Serving since</span></div><div><b>27 yrs</b><span>Of Kerala kitchens</span></div><div><b>10 to 1,000+</b><span>Guests per event</span></div></div>
  </div>
  <div class="plate">
    <div class="ring"></div>
    {media("counter-fruit","A-one fruit and dessert counter at a wedding reception", pos="50% 62%")}
    <span class="tag">We know how you love it</span>
    <div class="badge"><img src="assets/img/aone-logo.png" alt=""><div><b>A-one</b><small>Caterers &amp; Events</small></div></div>
  </div>
</div></section>

<section class="section band"><div class="wrap">
  <div class="head center"><span class="eyebrow">Why families choose us</span><h2>Good food, served on time, every time</h2><p class="lead">The things our guests remember are the taste and the care. The things our hosts remember are that nothing went wrong.</p></div>
  <div class="grid g4">
    <div class="feature" data-reveal><div class="icon">{ICON["chef"]}</div><h3>Experienced cooks</h3><p>Our kitchen team has cooked for Kerala weddings and feasts for over two decades.</p></div>
    <div class="feature" data-reveal="80"><div class="icon">{ICON["leaf"]}</div><h3>Fresh, every batch</h3><p>Vegetables, meat and fish bought fresh for each event. Nothing cooked days ahead.</p></div>
    <div class="feature" data-reveal="160"><div class="icon">{ICON["menu"]}</div><h3>Menus you choose</h3><p>Pick from our set menus or build your own, from sadya to biryani to continental.</p></div>
    <div class="feature" data-reveal="240"><div class="icon">{ICON["clock"]}</div><h3>On-time service</h3><p>Food ready and counters set before your first guest arrives.</p></div>
    <div class="feature" data-reveal><div class="icon">{ICON["people"]}</div><h3>Trained servers</h3><p>Uniformed service staff for banana-leaf serving, buffets and plated dinners.</p></div>
    <div class="feature" data-reveal="80"><div class="icon">{ICON["shield"]}</div><h3>Clean kitchens</h3><p>Hygienic preparation and packing, with hot food kept hot until it's served.</p></div>
    <div class="feature" data-reveal="160"><div class="icon">{ICON["tray"]}</div><h3>Full setup</h3><p>Counters, chafing dishes, crockery and cleanup handled by our team.</p></div>
    <div class="feature" data-reveal="240"><div class="icon">{ICON["spark"]}</div><h3>Event support</h3><p>Help with decor and the event flow, so the food and the day work together.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="head"><span class="eyebrow">What we cater</span><h2>One kitchen for every occasion</h2></div>
  <div class="grid g3">
    <a class="card zoom" href="services.html#weddings" data-reveal>{media("hall-buffet","Wedding buffet line by A-one", pos="50% 62%")}<h3>Weddings &amp; receptions</h3><p>Traditional sadya, Malabar biryani or a reception buffet, served for every guest.</p><span class="more">View menus {ICON["arrow"]}</span></a>
    <a class="card zoom" href="services.html#celebrations" data-reveal="100">{media("d-umali","Dessert table at a family celebration", pos="50% 70%")}<h3>Family celebrations</h3><p>Baptisms, first communions, engagements, birthdays and house-warmings.</p><span class="more">View menus {ICON["arrow"]}</span></a>
    <a class="card zoom" href="services.html#corporate" data-reveal="200">{media("clay-pots","Gold buffet counter with clay pots", pos="50% 70%")}<h3>Corporate events</h3><p>Office lunches, conferences and staff celebrations, with packed or buffet service.</p><span class="more">View menus {ICON["arrow"]}</span></a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="leaf" data-reveal>
    <div class="stack"><span class="eyebrow">Our signature</span><h2>The Kerala sadya, served on banana leaf</h2><p>Every leaf is served in order, the way it should be: salt and banana chips first, curries in their place, two payasams to finish. Tell us your guest count and we'll plan the rows, the servers and the timing.</p><div><a class="btn btn-gold" href="services.html#sadya">Sadya menus {ICON["arrow"]}</a></div></div>
    <ul class="dishes" aria-label="Typical sadya dishes">
      <li>Chor (rice)</li><li>Parippu &amp; ghee</li><li>Sambar</li><li>Avial</li><li>Olan</li><li>Kaalan</li><li>Thoran</li><li>Kootu curry</li><li>Erissery</li><li>Pachadi</li><li>Kichadi</li><li>Inji puli</li><li>Naranga achar</li><li>Mango pickle</li><li>Pappadam</li><li>Banana chips</li><li>Sharkara upperi</li><li>Rasam</li><li>Moru (buttermilk)</li><li>Pal payasam</li><li>Ada pradhaman</li><li>Banana</li>
    </ul>
  </div>
</div></section>

<section class="section band"><div class="wrap split">
  <div class="collage" data-reveal>{media("gold-chef","A-one team at the buffet line", pos="50% 55%")}{media("d-falooda","Short falooda and chocolate pastry","small", pos="50% 70%")}</div>
  <div class="stack" data-reveal="120">
    <span class="eyebrow">Our story</span>
    <h2>Cooking for Kerala's big days since 1999</h2>
    <p class="lead">A-one started as a family kitchen in Kothamangalam. Today we cater weddings, celebrations and corporate events wherever our clients need us, with the same recipes and the same care.</p>
    <ul class="checks"><li>Traditional recipes, cooked the way your family expects</li><li>Veg, non-veg and mixed menus</li><li>From 10-guest parties to weddings of 1,000+ plates</li></ul>
    <div><a class="btn btn-ghost" href="about.html">About A-one {ICON["arrow"]}</a></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="head center"><span class="eyebrow">How it works</span><h2>From first call to last plate</h2></div>
  <ol class="steps" style="padding:0;margin:0">
    <li data-reveal><h3>Tell us your event</h3><p>Date, venue, guest count and the kind of food you have in mind.</p></li>
    <li data-reveal="80"><h3>Choose the menu</h3><p>We suggest menus and adjust them to your family's taste and budget.</p></li>
    <li data-reveal="160"><h3>Confirm &amp; relax</h3><p>A clear quote, an advance to book the date, and we take it from there.</p></li>
    <li data-reveal="240"><h3>We cook &amp; serve</h3><p>Our team sets up, serves your guests and clears up after.</p></li>
  </ol>
</div></section>

<section class="section band"><div class="wrap">
  <div class="head center"><span class="eyebrow">Moments we've fed</span><h2>A taste of our events</h2></div>
  <div class="grid g4">
    {media("buffet-labels","Beef peralan, duck mappas and nool porotta","zoom", pos="50% 62%", style="aspect-ratio:3/4").replace('class="media zoom"','class="media zoom" data-reveal')}
    {media("counter-blue","Fruit carving centre counter","zoom", pos="50% 62%", style="aspect-ratio:3/4").replace('class="media zoom"','class="media zoom" data-reveal="80"')}
    {media("d-brownie","Walnut brownies and fruit tarts","zoom", pos="50% 70%", style="aspect-ratio:3/4").replace('class="media zoom"','class="media zoom" data-reveal="160"')}
    {media("outdoor","Outdoor buffet with lit arches","zoom", pos="50% 65%", style="aspect-ratio:3/4").replace('class="media zoom"','class="media zoom" data-reveal="240"')}
  </div>
  <div style="text-align:center;margin-top:32px"><a class="btn btn-primary" href="gallery.html">Open gallery {ICON["arrow"]}</a></div>
</div></section>
{reels_section()}
{CTA}
'''

ABOUT = page_hero("About A-one", "A family kitchen that grew into a full catering team",
    "Since 1999 we've cooked for weddings, feasts and family days across Kerala. The recipes have stayed the same. The team has grown.", "About") + f'''
<section class="section"><div class="wrap split">
  <div class="stack" data-reveal>
    <span class="eyebrow">Our story</span>
    <h2>“Let us be your personal chef for your special occasion”</h2>
    <p class="lead">That line has been our promise from the first wedding we cooked for. A host should spend the day with guests, not in the kitchen. So we take the whole food side off your hands: planning the menu, buying fresh, cooking, serving and cleaning up.</p>
    <p class="lead">Over the years we've added reception buffets, live counters and event support, but our kitchen still runs on the dishes Kerala families know and love.</p>
  </div>
  <div class="collage" data-reveal="120">{media("buffet-night","A-one buffet line at an evening reception", pos="50% 62%")}{media("d-sago","Sugar-free rose sago pudding","small", pos="50% 70%")}</div>
</div></section>

<section class="section band"><div class="wrap split rev">
  <div class="stack" data-reveal>
    <span class="eyebrow">Our journey</span>
    <h2>Twenty-seven years of feasts</h2>
    <div class="timeline">
      <div><b>1999</b><p>A-one Caterers begins in Kothamangalam, cooking sadya and biryani for local weddings.</p></div>
      <div><b>Growing</b><p>More families, more venues. We add buffet service, non-veg banquets and a trained serving team.</p></div>
      <div><b>A-one Caterers &amp; Events</b><p>Event support joins catering, so hosts can plan food and the day with one team.</p></div>
      <div><b>Today</b><p>Events from 10 guests to more than 1,000 plates, in Kothamangalam and across Kerala.</p></div>
    </div>
  </div>
  <div data-reveal="120">{media("counter-chef","Centre counter with our chef", pos="50% 60%", style="aspect-ratio:4/5;border-radius:28px")}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="head center"><span class="eyebrow">What we stand for</span><h2>The way we cook and serve</h2></div>
  <div class="grid g3">
    <div class="feature" data-reveal><div class="icon">{ICON["leaf"]}</div><h3>Taste first</h3><p>Fresh ingredients, freshly ground masalas and recipes we don't cut corners on.</p></div>
    <div class="feature" data-reveal="100"><div class="icon">{ICON["shield"]}</div><h3>Clean and safe</h3><p>Hygienic kitchens, careful handling and food kept at the right temperature.</p></div>
    <div class="feature" data-reveal="200"><div class="icon">{ICON["people"]}</div><h3>Warm service</h3><p>Our servers treat your guests the way you would, with patience and respect.</p></div>
  </div>
</div></section>
{CTA}
'''

def svc(id_, key, eyebrow, title, text, points, rev=False, menu=None):
    pts = "".join(f"<li>{p}</li>" for p in points)
    m = f'<p class="script" style="font-size:1.15rem">{menu}</p>' if menu else ""
    return f'''<section class="section{" band" if rev else ""}" id="{id_}"><div class="wrap split{" rev" if rev else ""}">
  <div data-reveal>{media(key, title, pos="50% 62%")}</div>
  <div class="stack" data-reveal="120"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p class="lead">{text}</p><ul class="checks">{pts}</ul>{m}<div><a class="btn btn-primary" href="contact.html">Ask for a quote {ICON["arrow"]}</a></div></div>
</div></section>'''

SERVICES = page_hero("Our services", "Catering for every kind of celebration",
    "Choose a set menu or build your own. We handle cooking, serving, setup and cleanup for events from 10 guests to 1,000+ plates.", "Services") + f'''
<section class="section"><div class="wrap">
  <div class="occasions" data-reveal>
    <span>Weddings</span><span>Receptions</span><span>Engagements</span><span>Baptisms</span><span>First Holy Communion</span><span>Birthdays</span><span>House-warming</span><span>Onam &amp; festival sadya</span><span>Church &amp; temple feasts</span><span>Corporate lunches</span><span>Conferences</span><span>Funeral &amp; remembrance meals</span>
  </div>
</div></section>
''' + svc("weddings","buffet-wide","Weddings &amp; receptions","Wedding catering, start to finish",
    "Whether it's a morning sadya at the church hall or a night reception buffet, we plan the food around your ceremony, your venue and your guest list.",
    ["Traditional sadya or Malabar-style biryani lunch","Reception buffets with starters, mains and desserts","Welcome drinks and live counters","Serving team in uniform for every row and counter"],
    menu="Guest favourites: chicken dum biriyani, beef peralan, duck mappas, duck roast, nool porotta, appam, pork fry") \
+ f'''<section class="section" id="sadya"><div class="wrap">
  <div class="leaf" data-reveal>
    <div class="stack"><span class="eyebrow">Kerala Sadya</span><h2>Sadya menus on banana leaf</h2><p>Choose a classic sadya, a festival sadya with extra curries, or a grand sadya with three payasams. We bring the leaves, the servers and the rhythm of a proper sadya service.</p><div><a class="btn btn-gold" href="contact.html">Book a sadya {ICON["arrow"]}</a></div></div>
    <ul class="dishes"><li>Classic sadya</li><li>Onam sadya</li><li>Wedding sadya</li><li>Avial</li><li>Olan</li><li>Kaalan</li><li>Erissery</li><li>Pulissery</li><li>Inji puli</li><li>Pal payasam</li><li>Ada pradhaman</li><li>Parippu pradhaman</li><li>Boli</li></ul>
  </div>
</div></section>''' \
+ svc("celebrations","d-umali","Family celebrations","Birthdays, baptisms and family days",
    "Smaller gatherings need the same care. We cook for home functions and hall events, and can serve at your house too.",
    ["Baptism, first communion and engagement menus","Birthday buffets with kids' favourites","House-warming lunches, veg or non-veg","Evening snacks, tea and dessert tables"], rev=True) \
+ svc("corporate","clay-pots","Corporate events","Office lunches and conferences",
    "Reliable, on-time food for your team and guests, delivered packed or served as a buffet.",
    ["Daily or one-time office lunches","Conference and seminar catering with tea breaks","Annual day and staff celebration buffets","GST invoices for companies"]) \
+ svc("outdoor","outdoor","Outdoor &amp; live counters","Live counters and outdoor catering",
    "Bring the kitchen to your guests. Live counters add theatre and keep food hot and fresh.",
    ["Live dosa, appam and porotta counters","Chicken tikka, rumali roti and grill stations","Juice, mocktail and ice-cream counters","Lit counters and full setup for outdoor and garden venues"], rev=True) \
+ svc("desserts","d-falooda","Dessert stations","A dessert table guests remember",
    "Our dessert tables are styled and stocked to match your event, with labelled counters and a mix of Kerala, Arabic and continental sweets.",
    ["Umm Ali, short falooda and hazelnut sundae","Walnut brownies, fruit tarts and pastries","Panna cotta, puddings and sugar-free options","Fruit carving and themed decor on the counter"],
    menu="From our last dessert table: sugar-free rose sago pudding") \
+ f'''<section class="section"><div class="wrap">
  <div class="head center"><span class="eyebrow">Included with every booking</span><h2>Everything the food side needs</h2></div>
  <div class="grid g4">
    <div class="feature" data-reveal><div class="icon">{ICON["menu"]}</div><h3>Menu planning</h3><p>Help choosing dishes and quantities for your guest count.</p></div>
    <div class="feature" data-reveal="80"><div class="icon">{ICON["tray"]}</div><h3>Counters &amp; crockery</h3><p>Chafing dishes, plates, glasses and table setup.</p></div>
    <div class="feature" data-reveal="160"><div class="icon">{ICON["people"]}</div><h3>Service staff</h3><p>Uniformed servers sized to your event.</p></div>
    <div class="feature" data-reveal="240"><div class="icon">{ICON["spark"]}</div><h3>Cleanup</h3><p>We clear counters and the dining area after service.</p></div>
  </div>
</div></section>
{CTA}
'''

GAL_ITEMS = [
    ("buffet-wide","buffets","Buffet line with lit arches","Buffets","wide"),
    ("counter-fruit","counters","Fruit carving centre counter","Counters","port"),
    ("d-falooda","desserts","Short falooda &amp; chocolate pastry","Desserts","tall"),
    ("hall-buffet","buffets","Wedding hall buffet","Buffets","port"),
    ("d-sago","desserts","Sugar-free rose sago pudding","Desserts","tall"),
    ("outdoor","outdoor","Outdoor buffet counter","Outdoor","port"),
    ("buffet-labels","buffets","Duck mappas, beef peralan, nool porotta","Buffets","tall"),
    ("d-umali","desserts","Umm Ali &amp; chocolate tarts","Desserts","port"),
    ("counter-blue","counters","Centre counter at night","Counters","tall"),
    ("gold-chef","buffets","Our team at the buffet line","Buffets","port"),
    ("d-brownie","desserts","Walnut brownie &amp; fruit tarts","Desserts","tall"),
    ("clay-pots","buffets","Gold counter with clay pots","Buffets","tall"),
    ("d-sundae","desserts","Hazelnut sundae &amp; pista panna cotta","Desserts","port"),
    ("counter-chef","counters","Centre counter with our chef","Counters","tall"),
    ("d-pannacotta","desserts","Panna cotta &amp; chocolate domes","Desserts","tall"),
    ("buffet-night","buffets","Evening reception buffet","Buffets","port"),
    ("d-pudding","desserts","Saffron pudding, éclairs &amp; cups","Desserts","tall"),
    ("gold-chafers","buffets","Gold chafing dishes","Buffets","tall"),
]
gal = "".join(
    f'<figure data-cat="{cat}" data-reveal="{(i%3)*80}">{media(k, t.replace("&amp;","and"), shape, pos="50% 60%")}<figcaption><b>{t}</b><span>{c}</span></figcaption></figure>'
    for i,(k,cat,t,c,shape) in enumerate(GAL_ITEMS))

GALLERY = page_hero("Gallery", "Food, tables and the moments around them",
    "Real photos from A-one events: buffet lines, centre counters and dessert tables. Tap any photo to view it larger.", "Gallery") + f'''
<section class="section"><div class="wrap">
  <div class="filters" role="group" aria-label="Filter gallery">
    <button aria-pressed="true" data-filter="all">All</button><button aria-pressed="false" data-filter="buffets">Buffets</button><button aria-pressed="false" data-filter="desserts">Desserts</button><button aria-pressed="false" data-filter="counters">Centre counters</button><button aria-pressed="false" data-filter="outdoor">Outdoor</button>
  </div>
  <div class="masonry">{gal}</div>
</div></section>
<div class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-close" aria-label="Close">×</button><button class="lb-prev" aria-label="Previous">‹</button><button class="lb-next" aria-label="Next">›</button>
  <div><img src="" alt=""><p></p></div>
</div>
{CTA}
'''

CONTACT = page_hero("Contact", "Let's plan the food for your day",
    "Share a few details and we'll reply with menu ideas and a quote. For quick questions, just call or WhatsApp.", "Contact") + f'''
<section class="section"><div class="wrap contact-grid">
  <div class="stack" data-reveal>
    <span class="eyebrow">Reach us</span>
    <h2>We'd love to hear about your event</h2>
    <p class="lead">Bookings fill up fast in wedding season, so reach out as soon as you have a date.</p>
    <div class="info">
      <div class="info-item"><div class="icon">{ICON["phone"]}</div><div><b>Call us</b><span class="phones">{phone_links("")}</span></div></div>
      <div class="info-item"><div class="icon">{ICON["wa"]}</div><div><b>Chat on WhatsApp</b><a href="https://wa.me/{PHONE_RAW}" target="_blank" rel="noopener">{PHONE} · tap to open chat</a></div></div>
      <div class="info-item"><div class="icon">{ICON["ig"]}</div><div><b>Follow us on Instagram</b><a href="{IG_URL}" target="_blank" rel="noopener">{IG_HANDLE}</a></div></div>
      <div class="info-item"><div class="icon">{ICON["pin"]}</div><div><b>Based in</b><span>Kothamangalam, Ernakulam, Kerala</span></div></div>
      <div class="info-item"><div class="icon">{ICON["clock"]}</div><div><b>Enquiries</b><span>Every day, 8 am – 9 pm</span></div></div>
    </div>
    <div class="map-card"><b style="font-family:var(--f-display);font-weight:400;font-size:1.3rem;color:#fff">Catering across Kerala</b><span>Our kitchen is in Kothamangalam, and we travel to venues across Kerala. Tell us where your event is.</span><a href="https://maps.google.com/?q=Kothamangalam,Kerala" target="_blank" rel="noopener">Open in Google Maps →</a></div>
  </div>
  <form class="form" id="enquiry" novalidate data-reveal="120">
    <h3>Event enquiry</h3>
    <div class="row">
      <div class="field"><label for="name">Your name *</label><input id="name" name="name" autocomplete="name" placeholder="Full name"><span class="err"></span></div>
      <div class="field"><label for="phone">Mobile number *</label><input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="10-digit number"><span class="err"></span></div>
    </div>
    <div class="row">
      <div class="field"><label for="event">Type of event *</label><select id="event" name="event"><option value="">Select…</option><option>Wedding</option><option>Reception</option><option>Engagement</option><option>Baptism / First Communion</option><option>Birthday</option><option>House-warming</option><option>Sadya / Festival</option><option>Corporate event</option><option>Other</option></select><span class="err"></span></div>
      <div class="field"><label for="date">Event date</label><input id="date" name="date" type="date"><span class="err"></span></div>
    </div>
    <div class="row">
      <div class="field"><label for="guests">Number of guests</label><input id="guests" name="guests" type="number" min="10" placeholder="e.g. 250"><span class="err"></span></div>
      <div class="field"><label for="venue">Venue / location</label><input id="venue" name="venue" placeholder="Hall or place"><span class="err"></span></div>
    </div>
    <div class="field"><label for="message">Menu ideas or questions</label><textarea id="message" name="message" placeholder="Veg / non-veg, sadya or buffet, dishes you'd like…"></textarea><span class="err"></span></div>
    <button class="btn btn-primary" type="submit">Prepare my enquiry {ICON["arrow"]}</button>
    <p class="form-note">Your enquiry is sent to us on WhatsApp, so you'll get a reply on your phone.</p>
    <div class="form-done" id="form-done" hidden>Your enquiry is ready. <a href="#" target="_blank" rel="noopener">Send it on WhatsApp →</a></div>
  </form>
</div></section>
'''

PAGES = [
  ("index.html","A-one Caterers &amp; Events","Wedding, sadya and event catering across Kerala since 1999, from 10 guests to 1,000+ plates. Based in Kothamangalam.","index.html",HOME),
  ("about.html","About · A-one Caterers","Our story: a family kitchen cooking for Kerala's big days since 1999.","about.html",ABOUT),
  ("services.html","Services · A-one Caterers","Wedding catering, Kerala sadya, family celebrations, corporate events and live counters.","services.html",SERVICES),
  ("gallery.html","Gallery · A-one Caterers","Photos of A-one Caterers food, table setups and events.","gallery.html",GALLERY),
  ("contact.html","Contact · A-one Caterers","Get a catering quote from A-one Caterers. Call +91 95445 41075, +91 99953 27413 or +91 70126 90063, or chat on WhatsApp.","contact.html",CONTACT),
]

def body(active, main):
    return f'{header(active)}\n<main class="page-in">{main}</main>\n{FOOTER}\n<script src="assets/js/main.js"></script>'

def build():
    for out, full_index in (("dist", True), ("artifact", False)):
        d = os.path.join(ROOT, out)
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(os.path.join(SRC, "assets"), os.path.join(d, "assets"))
        for fname, title, desc, active, main in PAGES:
            head = HEAD.format(title=title, desc=desc)
            if out == "artifact" and fname == "index.html":
                html = head + "\n" + body(active, main)
            else:
                html = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{head}\n</head>\n<body>\n{body(active, main)}\n</body>\n</html>\n'
            open(os.path.join(d, fname), "w").write(html)
    print("built")

build()
