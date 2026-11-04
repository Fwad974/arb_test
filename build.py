#!/usr/bin/env python3
"""Static site generator for Elevate Arabia. Python 3.9+, standard library only.

    python3 build.py           build into ./dist and check every internal link
    python3 build.py --serve   build, then serve ./dist at http://localhost:8000

Environment (optional, set in .github/workflows/pages.yml for deploys):
    SITE_URL    absolute site URL, e.g. https://www.elevatearabia.com
                adds canonical/og:url tags and a sitemap.xml
    INDEXABLE   "true" to allow search engines. Default is noindex so a
                preview deploy never competes with the live site in search.
"""
import json
import os
import re
import shutil
import sys
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

import content as C

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
SITE_URL = os.environ.get('SITE_URL', '').strip().rstrip('/')
INDEXABLE = os.environ.get('INDEXABLE', '').strip().lower() in ('1', 'true', 'yes')
YEAR = date.today().year


# --------------------------------------------------------------------------- helpers

def e(text):
    return escape(str(text), quote=True)


def hl(text):
    """Escape a headline and render [bracketed] text in the second tone."""
    return re.sub(r'\[(.+?)\]', r'<span class="tone">\1</span>', e(text))


ICONS = {
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'external': '<path d="M7 17 17 7M9 7h8v8"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
}


def icon(name, cls='icon'):
    return (f'<svg class="{cls}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def link_arrow(href, label, external=False):
    attrs = ' target="_blank" rel="noopener"' if external else ''
    sr = '<span class="visually-hidden"> (opens in a new tab)</span>' if external else ''
    return f'<a class="link-arrow" href="{e(href)}"{attrs}>{e(label)}{sr}{icon("external" if external else "arrow")}</a>'


def button(href, label, variant=''):
    cls = 'button' + (f' button--{variant}' if variant else '')
    return f'<a class="{cls}" href="{e(href)}">{e(label)}</a>'


def num(i):
    return f'{i:02d}'


def image_size(rel):
    """Pixel size of a WebP or PNG under assets/images, for width/height attributes."""
    b = (ROOT / 'assets' / 'images' / rel).read_bytes()[:32]
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return int.from_bytes(b[16:20], 'big'), int.from_bytes(b[20:24], 'big')
    kind = b[12:16]
    if kind == b'VP8X':
        return 1 + int.from_bytes(b[24:27], 'little'), 1 + int.from_bytes(b[27:30], 'little')
    if kind == b'VP8L':
        bits = int.from_bytes(b[21:25], 'little')
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b'VP8 ':
        return int.from_bytes(b[26:28], 'little') & 0x3FFF, int.from_bytes(b[28:30], 'little') & 0x3FFF
    raise ValueError(f'unsupported image {rel}')


def img(rel, alt, height=None, cls='', lazy=True):
    w, h = image_size(rel)
    if height:
        w, h = round(w * height / h), height
    attrs = f' class="{cls}"' if cls else ''
    attrs += ' loading="lazy" decoding="async"' if lazy else ''
    return f'<img src="assets/images/{rel}" alt="{e(alt)}" width="{w}" height="{h}"{attrs}>'


def logos(items, area=4200, max_w=150, cls=''):
    """Logo row. Sizes are balanced by area so tall and wide marks carry similar weight."""
    out = []
    for slug, name in items:
        w, h = image_size(f'clients/{slug}.webp')
        ratio = w / h
        dh = max(26, min(60, round((area / ratio) ** 0.5)))
        dw = round(dh * ratio)
        if dw > max_w:
            dw, dh = max_w, round(max_w / ratio)
        out.append(f'<li><img src="assets/images/clients/{slug}.webp" alt="{e(name)}" width="{dw}" height="{dh}" '
                   f'loading="lazy" decoding="async"></li>')
    return f'<ul class="logos {cls}">' + ''.join(out) + '</ul>'


BRAND = 'brand/elevate-wordmark.webp'            # original beige wordmark, for dark backgrounds
BRAND_DARK = 'brand/elevate-wordmark-dark.webp'  # navy variant for light backgrounds (beige on white is 2.4:1)

# Old Wix addresses -> new pages. GitHub Pages serves /home-1 from home-1.html,
# so a small redirect page keeps old links and search results working.
REDIRECTS = {
    'home-1': 'services.html', 'blank': 'ventures.html', 'blank-1': 'life-sciences.html',
    'blank-2': 'capital.html', 'blank-3': 'advisory.html', 'blank-4': 'market-entry.html',
    'blank-5': 'sectors.html', 'terms-and-coniditions': 'terms.html', 'privacy-policy': 'privacy.html',
}


def section(eyebrow, heading, body, intro='', id=None, footer=''):
    """Two-column editorial section: heading on the left, content on the right."""
    id_attr = f' id="{id}"' if id else ''
    intro_html = f'<p class="section-intro">{e(intro)}</p>' if intro else ''
    footer_html = f'<div class="section-foot">{footer}</div>' if footer else ''
    return f'''
<section class="section"{id_attr}>
  <div class="wrap split">
    <div class="split__head">
      <p class="eyebrow">{e(eyebrow)}</p>
      <h2>{hl(heading)}</h2>
      {intro_html}
    </div>
    <div class="split__body">
      {body}
      {footer_html}
    </div>
  </div>
</section>'''


def section_wide(eyebrow, heading, body, intro='', id=None):
    """Full-width section: heading block above, content across the whole width."""
    id_attr = f' id="{id}"' if id else ''
    intro_html = f'<p class="section-intro">{e(intro)}</p>' if intro else ''
    return f'''
<section class="section"{id_attr}>
  <div class="wrap">
    <div class="wide__head">
      <p class="eyebrow">{e(eyebrow)}</p>
      <h2>{hl(heading)}</h2>
      {intro_html}
    </div>
    {body}
  </div>
</section>'''


def page_hero(eyebrow, title, lead, actions='', crumbs=None, extra=''):
    crumbs_html = ''
    if crumbs:
        items = ''.join(f'<li><a href="{e(h)}">{e(t)}</a></li>' for t, h in crumbs[:-1])
        items += f'<li><span aria-current="page">{e(crumbs[-1][0])}</span></li>'
        crumbs_html = f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{items}</ol></nav>'
    actions_html = f'<div class="actions">{actions}</div>' if actions else ''
    return f'''
<section class="hero">
  <div class="wrap">
    {crumbs_html}
    <p class="eyebrow">{e(eyebrow)}</p>
    <h1>{hl(title)}</h1>
    <p class="lead">{e(lead)}</p>
    {actions_html}
    {extra}
  </div>
</section>'''


def rows(items):
    """Hairline list. item = dict(title, desc, href=None, num=None, meta=None, extra=None)."""
    out = []
    for it in items:
        num_html = f'<span class="row__num">{e(it["num"])}</span>' if it.get('num') else ''
        kicker = f'<span class="row__kicker">{e(it["meta"])}</span>' if it.get('meta') else ''
        extra = it.get('extra', '')
        inner = (f'{num_html}<span class="row__main">{kicker}<span class="row__title">{e(it["title"])}</span>'
                 f'<span class="row__desc">{e(it["desc"])}</span>{extra}</span>')
        if it.get('href'):
            out.append(f'<li class="row"><a class="row__link" href="{e(it["href"])}">{inner}'
                       f'{icon("arrow", "icon row__arrow")}</a></li>')
        else:
            id_attr = f' id="{it["id"]}"' if it.get('id') else ''
            out.append(f'<li class="row"{id_attr}><div class="row__link row__link--static">{inner}</div></li>')
    cls = 'rows' + (' rows--numbered' if any(i.get('num') for i in items) else '')
    return f'<ul class="{cls}">' + ''.join(out) + '</ul>'


def plain_list(items, numbered=False):
    tag = 'ol' if numbered else 'ul'
    cls = 'list list--numbered' if numbered else 'list'
    return f'<{tag} class="{cls}">' + ''.join(f'<li>{e(x)}</li>' for x in items) + f'</{tag}>'


def faq(pairs):
    return '<div class="faq">' + ''.join(
        f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in pairs) + '</div>'


def cta(title, body, label, href='contact.html'):
    return f'''
<section class="cta">
  <div class="wrap cta__inner">
    <div>
      <h2>{hl(title)}</h2>
      <p>{e(body)}</p>
    </div>
    {button(href, label)}
  </div>
</section>'''


# --------------------------------------------------------------------------- service areas

def service_areas():
    """The eight public service areas, in the live site's order."""
    areas = []
    for s in C.SERVICES:
        if s.get('areas'):
            for a in s['areas']:
                areas.append(dict(label=a['label'], short=a['short'], href=f'{s["slug"]}.html#{a["id"]}',
                                  tag=s['label'], items=a['items']))
        else:
            areas.append(dict(label=s['label'], short=s['short'], href=f'{s["slug"]}.html',
                              tag=s['tag'], items=s['needs']))
    return areas


AREAS = service_areas()
SERVICE_SLUGS = {s['slug'] for s in C.SERVICES}


# --------------------------------------------------------------------------- layout

NAV = [('Services', 'services.html', 'services'), ('Sectors', 'sectors.html', 'sectors'),
       ('About', 'about.html', 'about')]


def section_of(slug):
    if slug in SERVICE_SLUGS or slug == 'services':
        return 'services'
    if slug in ('sectors', 'life-sciences'):
        return 'sectors'
    return slug


def layout(slug, title, description, body):
    current = section_of(slug)
    filename = 'index.html' if slug == 'index' else f'{slug}.html'
    full_title = f'{C.SITE["name"]}: {title}' if slug == 'index' else f'{title} | {C.SITE["name"]}'

    def nav_link(label, href, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{label}</a>'

    nav = ''.join(nav_link(*n) for n in NAV)
    contact_cur = ' aria-current="page"' if current == 'contact' else ''

    head_extra = []
    base = ''
    if slug == '404' and SITE_URL:
        # GitHub Pages serves 404.html at any missing path, including nested ones,
        # so pin relative URLs to the site root.
        base = f'<base href="{e(SITE_URL)}/">\n'
    if SITE_URL:
        url = f'{SITE_URL}/' if slug == 'index' else f'{SITE_URL}/{filename}'
        head_extra += [f'<link rel="canonical" href="{e(url)}">', f'<meta property="og:url" content="{e(url)}">']
    if SITE_URL:
        head_extra += [f'<meta property="og:image" content="{e(SITE_URL)}/assets/images/og-image.png">',
                       '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                       '<meta name="twitter:card" content="summary_large_image">']
    if not INDEXABLE or slug == '404':
        head_extra.append('<meta name="robots" content="noindex">')
    if slug == 'index':
        head_extra.append(organization_jsonld())

    service_links = ''.join(f'<li><a href="{a["href"]}">{e(a["label"])}</a></li>' for a in AREAS)
    emails = ''.join(f'<li><a href="mailto:{m}">{m}</a></li>' for m in C.SITE['emails'])
    phones = ''.join(f'<li><a href="tel:{t}">{e(p)}</a></li>' for p, t in C.SITE['phones'])
    social = ''
    if C.SITE['social']:
        social = ('<div><h2 class="footer-title">Follow</h2><ul>' + ''.join(
            f'<li>{link_arrow(u, n, external=True)}</li>' for n, u in C.SITE['social']) + '</ul></div>')

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(C.SITE["name"])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
{chr(10).join(head_extra)}
<link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/ibm-plex-sans-latin-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/ibm-plex-sans-latin-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/styles.css">
<script>document.documentElement.classList.add('js')</script>
<script src="assets/js/app.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html">{img(BRAND_DARK, 'Elevate Arabia home', height=26, lazy=False)}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu">{icon("menu", "icon icon--menu")}{icon("close", "icon icon--close")}</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      {nav}
      <a class="button button--sm" href="contact.html"{contact_cur}>Contact</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html">{img(BRAND, 'Elevate Arabia home', height=28)}</a>
        <p class="footer-tagline">{e(C.SITE["tagline"])}</p>
      </div>
      <div>
        <h2 class="footer-title">Services</h2>
        <ul>{service_links}</ul>
      </div>
      <div>
        <h2 class="footer-title">Company</h2>
        <ul><li><a href="about.html">About</a></li><li><a href="sectors.html">Sectors</a></li><li><a href="contact.html">Contact</a></li></ul>
      </div>
      <div>
        <h2 class="footer-title">Contact</h2>
        <ul>{emails}{phones}</ul>
        <p class="footer-address">{"<br>".join(e(x) for x in C.SITE["address"])}</p>
        <p class="footer-map">{link_arrow(C.SITE["maps"], "Open in Google Maps", external=True)}</p>
      </div>
      {social}
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} {e(C.SITE["name"])}</span>
      <span><a href="privacy.html">Privacy Policy</a><a href="terms.html">Terms &amp; Conditions</a></span>
    </div>
  </div>
</footer>
</body>
</html>
'''


def organization_jsonld():
    """Company details for search engines (name, address, phones, email, logo)."""
    street, city = ', '.join(C.SITE['address'][:2]), C.SITE['address'][2].split(',')[0]
    data = {
        '@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': C.SITE['name'],
        'description': C.SITE['tagline'], 'email': C.SITE['enquiry_email'],
        'telephone': [t for _, t in C.SITE['phones']],
        'address': {'@type': 'PostalAddress', 'streetAddress': street, 'addressLocality': city, 'addressCountry': 'SA'},
        'areaServed': 'Saudi Arabia',
    }
    if SITE_URL:
        data.update(url=f'{SITE_URL}/', logo=f'{SITE_URL}/assets/images/apple-touch-icon.png',
                    image=f'{SITE_URL}/assets/images/og-image.png')
    if C.SITE['social']:
        data['sameAs'] = [u for _, u in C.SITE['social']]
    text = json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')
    return f'<script type="application/ld+json">\n{text}\n</script>'


PAGES = {}


def page(slug, title, description, body):
    PAGES['index.html' if slug == 'index' else f'{slug}.html'] = layout(slug, title, description, body)


# --------------------------------------------------------------------------- pages

def build_home():
    stats = '<dl class="stats">' + ''.join(
        f'<div class="stat"><dt>{e(v)}</dt><dd>{e(l)}</dd></div>' for v, l in C.STATS) + '</dl>'
    hero = page_hero(
        'Strategy · Capital · Market entry',
        'Building companies, capital pathways [and market‑ready ventures.]',
        'Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale their '
        'operations in Saudi Arabia through integrated advisory, capital readiness, venture support and '
        'market-entry execution.',
        actions=button('contact.html', 'Discuss a project') + link_arrow('services.html', 'Explore services'),
        extra=stats)

    services = section(
        'Services', 'Built around the challenges [you need to solve.]',
        rows([dict(num=num(i + 1), title=a['label'], desc=a['short'], href=a['href']) for i, a in enumerate(AREAS)]),
        intro='Rather than separate disciplines, we join business direction, financial structure and '
              'implementation into one connected approach.',
        footer='<div class="actions actions--tight">' + button('contact.html', 'Discuss a project')
               + link_arrow('services.html', 'All services') + '</div>')

    steps = '<ol class="steps">' + ''.join(
        f'<li class="step"><span class="step__num">{num(i + 1)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
        for i, (t, d) in enumerate(C.STEPS)) + '</ol>'
    approach = section('How we work', 'From complexity [to clarity.]', steps,
                       intro='Every engagement is different, but the work generally moves from understanding '
                             'the problem to building the right structure and supporting execution.')

    who = section(
        'Who we are', 'One integrated perspective. [Multiple disciplines.]',
        f'''<p class="body-lg">We work with established firms, entrepreneurs and investors, combining commercial
        planning, financial discipline, governance and sector understanding, with a focus on execution rather
        than advice in isolation.</p>
        <div class="panel">
          <p class="eyebrow">International partner</p>
          <p class="panel__title">Hirayama Holdings</p>
          <p>Our Japan-based strategic partner brings manufacturing improvement and Gemba Kaizen expertise.</p>
          {link_arrow('about.html#partnership', 'Our partnership')}
        </div>''',
        footer=link_arrow('about.html', 'About Elevate Arabia'))

    network = section_wide(
        'Clients', 'Network & [partners.]', logos(C.CLIENTS_NETWORK, cls='logos--grid'),
        intro='Clients and partners across life sciences, technology, sustainability and finance.', id='clients')

    sectors = section(
        'Sectors', 'Sector familiarity. [Business discipline.]',
        rows([dict(num=num(i + 1), title=s['label'], desc=s['desc'], href=f'sectors.html#{s["slug"]}')
              for i, s in enumerate(C.SECTORS)]),
        intro='We apply advisory and business-building capabilities across innovation, advanced industry '
              'and Saudi growth sectors.',
        footer=link_arrow('sectors.html', 'All sectors'))

    body = hero + services + approach + who + network + sectors + cta(
        'Let’s build what comes next.',
        'Talk to the team about your business, investment or Saudi market opportunity.', 'Discuss a project')
    page('index', 'Strategy, capital and Saudi market entry',
         'Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale '
         'their operations in Saudi Arabia.', body)


def build_services():
    hero = page_hero(
        'Services', 'Business support, [connected end to end.]',
        'Strategy, commercial planning, financial discipline, governance, investment preparation and Saudi '
        'market execution, organized so you can find the right expertise quickly.')
    listing = section(
        'Service areas', 'Eight service areas.',
        rows([dict(num=num(i + 1), title=a['label'], desc=a['short'], href=a['href'], meta=a['tag'],
                   extra='<span class="row__tags">' + ''.join(f'<span>{e(x)}</span>' for x in a['items'][:3]) + '</span>')
              for i, a in enumerate(AREAS)]),
        intro='Explore each area, or talk to us about a combination.')
    journey = section(
        'Approach', 'Not eight separate silos. [One business journey.]',
        '<p class="body-lg">A client may begin with strategy, then need financial structure, governance, '
        'investor readiness and market entry. We bring these together so each step builds on the last.</p>'
        '<p class="journey"><span>Strategy</span><span>Structure</span><span>Capital</span><span>Execution</span></p>')
    page('services', 'Services',
         'Advisory, ventures, capital, Saudi market entry, automotive industrial consultancy and construction '
         'technology from Elevate Arabia.',
         hero + listing + journey + cta('Need a combination of capabilities?',
                                        'Describe the business challenge and we can help determine a suitable '
                                        'starting point.', 'Discuss a project'))


def build_detail(item, is_sector=False):
    slug = item['slug']
    parent = ('Sectors', 'sectors.html') if is_sector else ('Services', 'services.html')
    hero = page_hero(
        item['tag'], item['title'], item['intro'],
        actions=button(f'contact.html?interest={slug}', 'Discuss this service' if not is_sector else 'Discuss your project')
        + link_arrow('#support', 'Where we can help'),
        crumbs=[('Home', 'index.html'), parent, (item['label'], '')])

    overview = section('Overview', 'Designed for [practical progress.]', f'<p class="body-lg">{e(item["overview"])}</p>')

    if item.get('areas'):
        support_body = '<div class="areas">' + ''.join(
            f'<div class="area" id="{a["id"]}"><span class="area__num">{num(i + 1)}</span><h3>{e(a["label"])}</h3>'
            f'<p>{e(a["short"])}</p>{plain_list(a["items"])}</div>'
            for i, a in enumerate(item['areas'])) + '</div>'
    else:
        support_body = plain_list(item['needs'])
    support = section('What we support', 'Where we can help.', support_body, id='support')

    outcomes = section(
        'Challenges & outcomes', 'What needs to [work better?]',
        f'''<div class="cols">
          <div><h3>Common challenges</h3><p class="small">Typical issues we help resolve.</p>{plain_list(item["challenges"], numbered=True)}</div>
          <div><h3>Typical outputs</h3><p class="small">Every engagement is scoped to your situation.</p>{plain_list(item["deliverables"], numbered=True)}</div>
        </div>''')

    questions = section('Questions', 'Good to know.', faq(item['faq']))

    related_items = [s for s in C.SERVICES if s['slug'] != slug][:3]
    related = section('Related', 'Related services.',
                      rows([dict(title=s['label'], desc=s['short'], href=f'{s["slug"]}.html') for s in related_items]))

    body = hero + overview + support + outcomes + questions + related + cta(
        'Have a specific challenge in mind?',
        'Share your objectives and the team can discuss the relevant workstreams.',
        'Enquire about this service' if not is_sector else 'Discuss your project',
        href=f'contact.html?interest={slug}')
    page(slug, item['label'], item['intro'], body)


def build_sectors():
    hero = page_hero(
        'Sectors', 'Sector expertise, [commercial perspective.]',
        'Different sectors face different market realities. The foundations of sound planning, finance, '
        'governance and execution remain essential in each.')

    items = []
    for i, s in enumerate(C.SECTORS):
        extra = (f'<span class="row__more">{link_arrow(s["link"], s["link_label"])}</span>' if s['link'] else '')
        items.append(dict(id=s['slug'], num=num(i + 1), title=s['label'], desc=s['desc'], meta=s['category'], extra=extra))
    listing = section('Focus sectors', 'Where we work.', rows(items),
                      intro='Seven focus sectors across innovation, industry, capital and consumer markets.')
    why = section(
        'Why it matters', 'Different sectors. [Shared disciplines.]',
        '<p class="body-lg">Sector familiarity supports better commercial assumptions and investment '
        'preparation. We combine this context with business modelling, capital readiness and Saudi market '
        'execution.</p>',
        footer=link_arrow('life-sciences.html', 'Life sciences in detail'))
    page('sectors', 'Sectors',
         'Sectors served by Elevate Arabia, from life sciences and advanced industry to education, '
         'agriculture, media and national development.',
         hero + listing + why + cta('Working in a specialized sector?',
                                    'Tell us about the sector, geography and stage of your project.',
                                    'Discuss your sector'))


def build_about():
    hero = page_hero(
        'About', 'A strategic growth and [integrated advisory firm.]',
        'Elevate Arabia supports businesses, ventures and investors through connected strategy, finance, '
        'governance, coordination and execution support.')
    who = section(
        'Who we are', 'Clarity, control [and confidence.]',
        '<p class="body-lg">We are commercially focused, integrated across disciplines and oriented toward '
        'execution. We work with established companies and with new ventures pursuing growth in Saudi Arabia.</p>'
        '<blockquote class="statement"><p>From concept and capital preparation to commercialization and '
        'operations, a stronger business starts with the right structure.</p></blockquote>')
    values = section(
        'Values', 'How we work.',
        '<ul class="grid-values">' + ''.join(
            f'<li><span class="area__num">{num(i + 1)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
            for i, (t, d) in enumerate(C.VALUES)) + '</ul>')
    partner = section(
        'International partnership', 'A shared focus on [improvement.]',
        '<p class="body-lg">Japan-based Hirayama Holdings is our strategic international partner, with a focus on '
        'Gemba Kaizen, manufacturing performance and continuous improvement.</p>'
        f'<figure class="photo">{img(C.PARTNER["photo"], C.PARTNER["photo_alt"])}'
        f'<figcaption>{e(C.PARTNER["photo_alt"])}.</figcaption></figure>'
        '<div class="panel"><p class="eyebrow">International partner</p>'
        f'<p class="panel__title">{e(C.PARTNER["name"])}</p>'
        '<p>Tokyo, Japan. Manufacturing capability, continuous improvement and industrial consulting.</p>'
        f'{link_arrow(C.PARTNER["url"], "Visit Hirayama Holdings", external=True)}</div>'
        + (f'<h3 class="group-title group-title--logos">{e(C.PARTNER_CLIENTS_LABEL)}</h3>'
           + logos(C.CLIENTS_GLOBAL, cls='logos--grid logos--compact') if C.SHOW_PARTNER_CLIENTS else ''),
        id='partnership')

    def avatar(name, photo):
        if photo:
            return img(f'team/{photo}.webp', '', height=56, cls='avatar')
        initials = ''.join(w[0] for w in name.split()[:2])
        return f'<span class="avatar avatar--initials" aria-hidden="true">{e(initials)}</span>'

    def people(arr):
        return '<ul class="people">' + ''.join(
            f'<li>{avatar(n, ph)}<span><span class="people__name">{e(n)}</span>'
            f'<span class="people__role">{e(r)}</span></span></li>'
            for n, r, ph in arr) + '</ul>'

    team = section(
        'Team', 'Experience behind [the work.]',
        f'<h3 class="group-title">Saudi Arabia <span>{len(C.TEAM_SAUDI)}</span></h3>{people(C.TEAM_SAUDI)}'
        f'<h3 class="group-title">International <span>{len(C.TEAM_INTERNATIONAL)}</span></h3>{people(C.TEAM_INTERNATIONAL)}',
        intro='Our team in Saudi Arabia, supported by international specialists in manufacturing and '
              'continuous improvement.', id='team')
    page('about', 'About',
         'Elevate Arabia is a strategic growth and integrated advisory firm in Jeddah, working with businesses, '
         'founders and investors.',
         hero + who + values + partner + team + cta('Work with Elevate Arabia.',
                                                    'Discuss a business challenge, potential engagement or '
                                                    'partnership opportunity.', 'Contact the team'))


def build_contact():
    hero = page_hero(
        'Contact', 'Let’s discuss [your next move.]',
        'Whether you are entering Saudi Arabia, building a venture or preparing for investment, start with a '
        'clear conversation.')

    options = [(s['slug'], s.get('option', s['label'])) for s in C.SERVICES]
    options += [('life-sciences', C.LIFE_SCIENCES['label']), ('other', 'Something else')]
    opts = ''.join(f'<option value="{v}">{e(l)}</option>' for v, l in options)

    def field(fid, label, control, required=False, hint=''):
        req = ' <span class="req" aria-hidden="true">*</span>' if required else ''
        hint_html = f'<p class="field-hint" id="{fid}-hint">{e(hint)}</p>' if hint else ''
        return (f'<div class="field"><label for="{fid}">{e(label)}{req}</label>{hint_html}{control}'
                f'<p class="field-error" id="{fid}-error"></p></div>')

    def described(fid, hint=False):
        ids = ([f'{fid}-hint'] if hint else []) + [f'{fid}-error']
        return f'aria-describedby="{" ".join(ids)}"'

    form = f'''
<form class="form" id="enquiry-form" novalidate data-to="{e(C.SITE["enquiry_email"])}">
  <p class="small">Fields marked <span class="req" aria-hidden="true">*</span><span class="visually-hidden">with an asterisk</span> are required.</p>
  <div class="form-row">
    {field('f-name', 'Full name', f'<input id="f-name" name="name" autocomplete="name" required {described("f-name")} data-required="Please enter your name.">', True)}
    {field('f-email', 'Email', f'<input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required {described("f-email")} data-required="Please enter your email address.">', True)}
  </div>
  <div class="form-row">
    {field('f-company', 'Company', '<input id="f-company" name="company" autocomplete="organization">')}
    {field('f-phone', 'Phone', '<input id="f-phone" name="phone" type="tel" autocomplete="tel">')}
  </div>
  {field('f-interest', 'How can we help?', f'<select id="f-interest" name="interest" required {described("f-interest")} data-required="Please choose a service."><option value="">Choose a service</option>{opts}</select>', True)}
  {field('f-message', 'Project details', f'<textarea id="f-message" name="message" rows="6" minlength="20" required {described("f-message", True)} data-required="Please tell us a little about your project."></textarea>', True, hint='Your objectives, current stage and the support you need.')}
  <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
  <button class="button" type="submit">Prepare email</button>
  <p class="small">This opens a pre-filled email in your mail app so you can review it before sending. Nothing is stored on this website. See our <a href="privacy.html">Privacy Policy</a>.</p>
</form>'''

    details = '<dl class="contact-list">' + ''.join(
        f'<div><dt>Email</dt><dd><a href="mailto:{m}">{m}</a></dd></div>' for m in C.SITE['emails']) + ''.join(
        f'<div><dt>Phone</dt><dd><a href="tel:{t}">{e(p)}</a></dd></div>' for p, t in C.SITE['phones']) + (
        f'<div><dt>Office</dt><dd>{", ".join(e(x) for x in C.SITE["address"])}'
        f'<span class="dd-link">{link_arrow(C.SITE["maps"], "Open in Google Maps", external=True)}</span></dd></div>') + (
        f'<div><dt>Social</dt><dd class="dd-links">' + ''.join(link_arrow(u, n, external=True) for n, u in C.SITE['social'])
        + '</dd></div>' if C.SITE['social'] else '') + '</dl>'

    body = hero + f'''
<section class="section">
  <div class="wrap split">
    <div class="split__head">
      <p class="eyebrow">Direct contact</p>
      <h2>{hl('Tell us what [you’re building.]')}</h2>
      {details}
    </div>
    <div class="split__body">
      <h2 class="visually-hidden">Enquiry form</h2>
      {form}
    </div>
  </div>
</section>'''
    page('contact', 'Contact',
         'Contact Elevate Arabia in Jeddah about advisory, ventures, capital readiness or Saudi market entry.', body)


def build_legal():
    updated = f'<p class="legal-date">Last updated: {e(C.LEGAL_UPDATED)}</p>'
    t = C.TERMS
    terms = (page_hero('Legal', 'Terms & Conditions', 'The terms that apply to using this website.')
             + section('Legal disclaimer', 'Disclaimer.', updated + ''.join(f'<p>{e(x)}</p>' for x in t['disclaimer']),
                       id='disclaimer')
             + section('Terms of use', 'Terms of use.',
                       f'<p>{e(t["intro"])}</p><ol class="legal-clauses">' + ''.join(
                           f'<li><h3>{e(h)}</h3><p>{e(x)}</p></li>' for h, x in t['clauses']) + '</ol>', id='terms'))
    page('terms', 'Terms & Conditions', 'The terms that apply to using the Elevate Arabia website.', terms)

    pr = C.PRIVACY
    contact = f'<p>Questions or requests about your personal data: <a href="mailto:{pr["contact"]}">{pr["contact"]}</a>.</p>'
    privacy = (page_hero('Legal', 'Privacy Policy', 'How we handle personal data, and how to contact us about it.')
               + section('Privacy', 'Your personal data.',
                         updated + ''.join(f'<p>{e(x)}</p>' for x in pr['paragraphs']) + contact + f'<p>{e(pr["changes"])}</p>'))
    page('privacy', 'Privacy Policy', 'How Elevate Arabia handles personal data, and how to contact us about it.', privacy)


def redirect_page(new):
    target = f'{SITE_URL}/{new}' if SITE_URL else new
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Page moved | {e(C.SITE["name"])}</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{e(target)}">
<meta http-equiv="refresh" content="0; url={e(new)}">
<script>location.replace({json.dumps(new)} + location.hash)</script>
</head>
<body>
<h1>This page has moved</h1>
<p><a href="{e(new)}">Continue to the new page</a>.</p>
</body>
</html>
'''


def build_404():
    body = page_hero('Error 404', 'Page not found.',
                     'The page you are looking for does not exist or has moved.',
                     actions=button('index.html', 'Back to home') + link_arrow('contact.html', 'Contact us'))
    page('404', 'Page not found', 'The page you are looking for does not exist or has moved.', body)


# --------------------------------------------------------------------------- checks

class _Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.h1 = [], [], 0
        self.empty_headings, self._heading, self._heading_text = 0, None, ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self._heading, self._heading_text = tag, ''
        if tag == 'img' and self._heading:
            self._heading_text += a.get('alt') or ''
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'h1':
            self.h1 += 1
        for k in ('href', 'src'):
            if a.get(k):
                self.links.append(a[k])

    def handle_data(self, data):
        if self._heading:
            self._heading_text += data

    def handle_endtag(self, tag):
        if tag == self._heading:
            if not self._heading_text.strip():
                self.empty_headings += 1
            self._heading = None


INVISIBLE = re.compile('[\u200b\u200c\u200d\u2060\ufeff]')


def check(out):
    parsed = {}
    for p in out.glob('*.html'):
        c = _Collector()
        text = p.read_text(encoding='utf-8')
        c.feed(text)
        c.invisible = len(INVISIBLE.findall(text))
        parsed[p.name] = c
    errors = []
    for name, c in parsed.items():
        if c.h1 != 1:
            errors.append(f'{name}: expected one <h1>, found {c.h1}')
        if c.empty_headings:
            errors.append(f'{name}: {c.empty_headings} empty heading(s)')
        if c.invisible:
            errors.append(f'{name}: {c.invisible} invisible character(s)')
        dupes = {i for i in c.ids if c.ids.count(i) > 1}
        if dupes:
            errors.append(f'{name}: duplicate ids {sorted(dupes)}')
        for link in c.links:
            u = urlsplit(link)
            if u.scheme or link.startswith('//'):
                continue  # external, mailto:, tel:
            target = u.path or name
            if not (out / target).exists():
                errors.append(f'{name}: broken link "{link}"')
            elif u.fragment and target.endswith('.html') and u.fragment not in parsed[target].ids:
                errors.append(f'{name}: missing anchor "{link}"')
    return errors


# --------------------------------------------------------------------------- main

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'assets', OUT / 'assets')

    build_home()
    build_services()
    for s in C.SERVICES:
        build_detail(s)
    build_detail(C.LIFE_SCIENCES, is_sector=True)
    build_sectors()
    build_about()
    build_contact()
    build_legal()
    build_404()

    for name, html in PAGES.items():
        (OUT / name).write_text(html, encoding='utf-8')
    for old, new in REDIRECTS.items():
        assert f'{old}.html' not in PAGES, old
        (OUT / f'{old}.html').write_text(redirect_page(new), encoding='utf-8')

    robots = 'User-agent: *\n' + ('Allow: /\n' if INDEXABLE else 'Disallow: /\n')
    if SITE_URL:
        urls = [f'{SITE_URL}/' if n == 'index.html' else f'{SITE_URL}/{n}' for n in sorted(PAGES) if n != '404.html']
        (OUT / 'sitemap.xml').write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + ''.join(f'  <url><loc>{e(u)}</loc></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')
        if INDEXABLE:
            robots += f'Sitemap: {SITE_URL}/sitemap.xml\n'
    (OUT / 'robots.txt').write_text(robots, encoding='utf-8')

    errors = check(OUT)
    if errors:
        print('Build checks failed:', *errors, sep='\n  ', file=sys.stderr)
        sys.exit(1)
    print(f'Built {len(PAGES)} pages into {OUT.relative_to(ROOT)}/ '
          f'({"indexable" if INDEXABLE else "noindex"}{", " + SITE_URL if SITE_URL else ""}). Links OK.')

    if '--serve' in sys.argv:
        import functools
        import http.server
        port = int(os.environ.get('PORT', 8000))
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        print(f'Serving http://localhost:{port}  (Ctrl+C to stop)')
        http.server.ThreadingHTTPServer(('', port), handler).serve_forever()


if __name__ == '__main__':
    main()
