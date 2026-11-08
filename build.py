#!/usr/bin/env python3
"""Static site generator for Elevate Arabia. Python 3.9+, standard library only.

    python3 build.py           build into ./dist and check every internal link
    python3 build.py --serve   build, then serve ./dist at http://localhost:8000

Builds the English site at / and the Arabic site at /ar/ from the same templates.
Copy lives in content.py (English) and content_ar.py (Arabic).

Environment (optional, set in .github/workflows/pages.yml for deploys):
    SITE_URL    absolute site URL, e.g. https://www.elevatearabia.com
                adds canonical, hreflang and og:url tags and a sitemap.xml
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
from urllib.parse import quote, urlsplit

import content as EN
import content_ar as AR
import content_ja as JA
import content_zh as ZH

LANGS = [EN, AR, ZH, JA]   # the first is the default language, served at the site root
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
SITE_URL = os.environ.get('SITE_URL', '').strip().rstrip('/')
INDEXABLE = os.environ.get('INDEXABLE', '').strip().lower() in ('1', 'true', 'yes')
YEAR = date.today().year


def load_site_env(path):
    """Contact-channel settings from site.env. A non-empty environment variable with the same
    name (e.g. a GitHub Actions repository variable) overrides the file."""
    values, placeholders = {}, set()
    if path.exists():
        for raw in path.read_text(encoding='utf-8').splitlines():
            line = raw.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, _, rest = line.partition('=')
            key = key.strip()
            parts = re.split(r'\s+#', rest, maxsplit=1)
            values[key] = parts[0].strip().strip('"\'')
            if len(parts) > 1 and 'placeholder' in parts[1].lower():
                placeholders.add(key)
    for key in ('WHATSAPP_NUMBER', 'WECHAT_ID', 'WECHAT_QR', 'LINE_ID'):
        override = os.environ.get(key, '').strip()
        if override:
            values[key] = override
            placeholders.discard(key)
        values.setdefault(key, '')
    return values, placeholders


SITE_ENV, ENV_PLACEHOLDERS = load_site_env(ROOT / 'site.env')

# The language being built. set_language() switches these.
C = EN          # content module for this language
PREFIX = ''     # path from a page to the site root: '' for /, '../' for /ar/
AREAS = []
SERVICE_SLUGS = set()


def set_language(mod):
    global C, PREFIX, AREAS, SERVICE_SLUGS
    C = mod
    PREFIX = '../' * mod.LANG['path'].count('/')
    AREAS = service_areas()
    SERVICE_SLUGS = {s['slug'] for s in C.SERVICES}


def t(key, **values):
    """Interface text in the current language. {placeholders} are filled only when values are given."""
    text = C.UI[key]
    return text.format(**values) if values else text


# --------------------------------------------------------------------------- helpers

def e(text):
    return escape(str(text), quote=True)


def hl(text):
    """Escape a headline and render [bracketed] text in the second tone."""
    return re.sub(r'\[(.+?)\]', r'<span class="tone">\1</span>', e(text))


def asset(path):
    return f'{PREFIX}assets/{path}'


ICONS = {
    'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'external': '<path d="M7 17 17 7M9 7h8v8"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3Z"/>',
}


def icon(name, cls='icon'):
    return (f'<svg class="{cls} icon--{name}" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


BRAND_ICONS = {name: re.search(r'<path d="([^"]+)"', (ROOT / 'assets' / 'icons' / f'{name}.svg').read_text()).group(1)
               for name in ('whatsapp', 'wechat', 'line')}


def brand_icon(name):
    return (f'<svg class="icon icon--brand" aria-hidden="true" viewBox="0 0 24 24" fill="currentColor">'
            f'<path d="{BRAND_ICONS[name]}"/></svg>')


def channels():
    """Messaging apps configured in site.env, validated, in display order."""
    out = []
    digits = re.sub(r'\D', '', SITE_ENV['WHATSAPP_NUMBER'])
    if digits:
        if not 8 <= len(digits) <= 15:
            raise ValueError('site.env: WHATSAPP_NUMBER must be a full international number, e.g. +966533337712')
        shown = next((label for label, number in C.SITE['phones'] if re.sub(r'\D', '', number) == digits), '+' + digits)
        out.append(dict(key='whatsapp', name=t('whatsapp'), action=t('whatsapp_action'), value=shown,
                        href=f'https://wa.me/{digits}?text={quote(t("whatsapp_text"))}'))
    wechat = SITE_ENV['WECHAT_ID']
    if wechat:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{5,19}', wechat):
            raise ValueError('site.env: WECHAT_ID must be 6-20 letters, digits, _ or -, starting with a letter')
        qr = SITE_ENV['WECHAT_QR']
        if qr and not (ROOT / 'assets' / 'images' / 'contact' / qr).exists():
            raise ValueError(f'site.env: WECHAT_QR file assets/images/contact/{qr} not found')
        out.append(dict(key='wechat', name=t('wechat'), value=wechat, qr=qr, href='contact.html#wechat'))
    line = SITE_ENV['LINE_ID']
    if line:
        if line.startswith('https://line.me/'):
            href, shown = line, line
        else:
            handle = line.lstrip('@')
            if not re.fullmatch(r'[A-Za-z0-9._-]{3,20}', handle):
                raise ValueError('site.env: LINE_ID must be an Official Account ID such as @elevatearabia')
            href, shown = f'https://line.me/R/ti/p/%40{handle}', '@' + handle
        out.append(dict(key='line', name=t('line'), action=t('line_action'), value=shown, href=href))
    return out


def link_arrow(href, label, external=False, brand=None):
    attrs = ' target="_blank" rel="noopener"' if external else ''
    sr = f'<span class="visually-hidden">{e(t("new_tab"))}</span>' if external else ''
    lead = brand_icon(brand) if brand else ''
    return (f'<a class="link-arrow" href="{e(href)}"{attrs}>{lead}{e(label)}{sr}'
            f'{icon("external" if external else "arrow")}</a>')


def button(href, label):
    return f'<a class="button" href="{e(href)}">{e(label)}</a>'


def mailto(address):
    return f'<a href="mailto:{e(address)}" dir="ltr">{e(address)}</a>'


def tel(label, number):
    return f'<a href="tel:{e(number)}" dir="ltr">{e(label)}</a>'


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
    return f'<img src="{asset("images/" + rel)}" alt="{e(alt)}" width="{w}" height="{h}"{attrs}>'


def logos(items, cls=''):
    """Logo grid. Files are monochrome ink on one 360x160 canvas (scripts/prepare_logos.py).
    Each item is (slug, name) or (slug, name, website); a website makes the logo a link."""
    out = []
    for slug, name, *rest in items:
        if image_size(f'clients/{slug}.webp') != (360, 160):
            raise ValueError(f'clients/{slug}.webp is not 360x160; prepare it with scripts/prepare_logos.py')
        logo = (f'<img src="{asset(f"images/clients/{slug}.webp")}" alt="{e(name)}" width="180" height="80" '
                f'loading="lazy" decoding="async">')
        if rest and rest[0]:
            if not rest[0].startswith('https://'):
                raise ValueError(f'{slug}: logo link must start with https://')
            logo = (f'<a href="{e(rest[0])}" target="_blank" rel="noopener">{logo}'
                    f'<span class="visually-hidden">{e(t("new_tab"))}</span></a>')
        out.append(f'<li>{logo}</li>')
    return f'<ul class="logos {cls}">' + ''.join(out) + '</ul>'


# The wordmark is one SVG master file, traced from the original artwork. The header inlines it,
# so the letters follow the theme colour (navy on white, beige in dark mode) and the red bar can
# draw itself in and lift on hover (see .logo in styles.css). The footer, which is always dark,
# shows a beige copy as an image; main() writes that copy into dist/.
LOGO_SVG = (ROOT / 'assets' / 'images' / 'brand' / 'elevate-wordmark.svg').read_text(encoding='utf-8')
LOGO_VIEWBOX = re.search(r'viewBox="([^"]+)"', LOGO_SVG).group(1)
LOGO_RATIO = (lambda v: v[2] / v[3])([float(x) for x in LOGO_VIEWBOX.split()])
LOGO_BEIGE = '#b4a298'                               # the original beige, for dark backgrounds
LOGO_LIGHT = 'brand/elevate-wordmark-light.svg'      # generated beige copy, for the footer


def _logo_part(pattern):
    found = re.search(pattern, LOGO_SVG)
    if not found:
        raise ValueError(f'elevate-wordmark.svg: missing {pattern}')
    return found.group(1)


_letters = _logo_part(r'<path id="logo-letters"[^>]*?\sd="([^"]+)"')
_kanji = _logo_part(r'<path id="logo-kanji"[^>]*?\sd="([^"]+)"')
_bar = _logo_part(r'(<line [^>]+/>)').replace('<line ', '<line class="logo__line" ', 1)
# The light that runs up the red bar: the same line, white, narrower, and drawn as one short dash
# (styles.css moves the dash). One copy plays on page load, the other on hover.
_ends = ' '.join(k + '="' + _logo_part(r'<line[^>]*\s' + k + r'="([-0-9.]+)"') + '"' for k in ('x1', 'y1', 'x2', 'y2'))
_glint_width = round(float(_logo_part(r'<line [^>]*stroke-width="([0-9.]+)"')) * 0.5, 1)
_glints = ''.join(f'<line class="logo__glint logo__glint--{when}" {_ends} stroke="#fff" stroke-width="{_glint_width}" '
                  f'stroke-linecap="round" pathLength="1"/>' for when in ('load', 'hover'))
if 'color="#0f2137"' not in LOGO_SVG:
    raise ValueError('elevate-wordmark.svg: the root <svg> needs color="#0f2137" (the footer copy swaps it)')
LOGO_INLINE = (f'<svg class="logo" viewBox="{LOGO_VIEWBOX}" aria-hidden="true" focusable="false">'
               f'<path fill="currentColor" d="{_letters}"/><g class="logo__bar">{_bar}{_glints}'
               f'<path class="logo__kanji" fill="#fff" d="{_kanji}"/></g></svg>')

# Runs before first paint. Marks JS as available, and plays the logo's intro only when the
# visitor arrives from another site or types the address, not on every page inside the site.
# Reading the referrer stores nothing on the visitor's device.
HEAD_SCRIPT = ("(function(d){d.classList.add('js');try{var r=document.referrer;"
               "if(!r||new URL(r).host!==location.host)d.classList.add('logo-intro')}catch(x){}})"
               "(document.documentElement)")


# Old Wix addresses -> new pages. GitHub Pages serves /home-1 from home-1.html,
# so a small redirect page keeps old links and search results working.
REDIRECTS = {
    'home-1': 'services.html', 'blank': 'ventures.html', 'blank-1': 'life-sciences.html',
    'blank-2': 'capital.html', 'blank-3': 'advisory.html', 'blank-4': 'market-entry.html',
    'blank-5': 'sectors.html', 'terms-and-coniditions': 'terms.html', 'privacy-policy': 'privacy.html',
}


def section(eyebrow, heading, body, intro='', id=None, footer=''):
    """Two-column editorial section: heading on the start side, content on the end side."""
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


def page_hero(eyebrow, title, lead, actions='', crumbs=None, extra='', cls=''):
    """Page header. On wide screens (see .hero in styles.css) the intro and actions sit
    beside the headline instead of below it, so the first screen uses its full width."""
    crumbs_html = ''
    if crumbs:
        items = ''.join(f'<li><a href="{e(h)}">{e(x)}</a></li>' for x, h in crumbs[:-1])
        items += f'<li><span aria-current="page">{e(crumbs[-1][0])}</span></li>'
        crumbs_html = f'<nav class="breadcrumb" aria-label="{e(t("breadcrumb_label"))}"><ol>{items}</ol></nav>'
    actions_html = f'<div class="actions">{actions}</div>' if actions else ''
    return f'''
<section class="hero{' ' + cls if cls else ''}">
  <div class="wrap">
    {crumbs_html}
    <div class="hero__main">
      <p class="eyebrow">{e(eyebrow)}</p>
      <h1>{hl(title)}</h1>
    </div>
    <div class="hero__side">
      <p class="lead">{e(lead)}</p>
      {actions_html}
    </div>
    {extra}
  </div>
</section>'''


def rows(items, compact=False):
    """Hairline list. item = dict(title, desc, href=None, num=None, meta=None, extra=None).
    compact=True shows titles only, in two columns from tablet width up."""
    out = []
    for it in items:
        num_html = f'<span class="row__num">{e(it["num"])}</span>' if it.get('num') else ''
        kicker = f'<span class="row__kicker">{e(it["meta"])}</span>' if it.get('meta') else ''
        extra = it.get('extra', '')
        desc = '' if compact else f'<span class="row__desc">{e(it["desc"])}</span>'
        inner = (f'{num_html}<span class="row__main">{kicker}<span class="row__title">{e(it["title"])}</span>'
                 f'{desc}{extra}</span>')
        if it.get('href'):
            out.append(f'<li class="row"><a class="row__link" href="{e(it["href"])}">{inner}'
                       f'{icon("arrow", "icon row__arrow")}</a></li>')
        else:
            id_attr = f' id="{it["id"]}"' if it.get('id') else ''
            out.append(f'<li class="row"{id_attr}><div class="row__link row__link--static">{inner}</div></li>')
    cls = 'rows' + (' rows--numbered' if any(i.get('num') for i in items) else '') + (' rows--compact' if compact else '')
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


# --------------------------------------------------------------------------- layout

def section_of(slug):
    if slug in SERVICE_SLUGS or slug == 'services':
        return 'services'
    if slug in ('sectors', 'life-sciences'):
        return 'sectors'
    return slug


def page_url(mod, filename):
    """Absolute URL of a page in a given language (requires SITE_URL)."""
    path = mod.LANG['path'] + ('' if filename == 'index.html' else filename)
    return f'{SITE_URL}/{path}'


def layout(slug, title, description, body):
    lang = C.LANG
    current = section_of(slug)
    filename = 'index.html' if slug == 'index' else f'{slug}.html'
    full_title = f'{C.SITE["name"]}: {title}' if slug == 'index' else f'{title} | {C.SITE["name"]}'
    has_twin = slug != '404'
    twin = filename if has_twin else 'index.html'

    def lang_links():
        # The same page in every language, each label in its own script.
        items = []
        for m in LANGS:
            current_attr = ' aria-current="true"' if m is C else ''
            items.append(f'<li><a href="{PREFIX}{m.LANG["path"]}{twin}" hreflang="{m.LANG["code"]}" '
                         f'lang="{m.LANG["code"]}"{current_attr}>{e(m.LANG["name"])}</a></li>')
        return ''.join(items)

    def nav_link(label, href, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{e(label)}</a>'

    nav = ''.join(nav_link(t(k), h, key) for k, h, key in [
        ('nav_services', 'services.html', 'services'), ('nav_sectors', 'sectors.html', 'sectors'),
        ('nav_about', 'about.html', 'about')])
    contact_cur = ' aria-current="page"' if current == 'contact' else ''
    lang_menu = (f'<details class="lang-menu"><summary aria-label="{e(t("language"))}: {e(lang["name"])}">'
                 f'{icon("globe")}<span>{e(lang["short"])}</span></summary><ul>{lang_links()}</ul></details>')

    head_extra = [f'<meta property="og:locale" content="{lang["locale"]}">']
    base = ''
    if slug == '404' and SITE_URL:
        # GitHub Pages serves 404.html at any missing path, including nested ones,
        # so pin relative URLs to the site root.
        base = f'<base href="{e(SITE_URL)}/">\n'
    if SITE_URL:
        url = page_url(C, filename)
        head_extra += [f'<link rel="canonical" href="{e(url)}">', f'<meta property="og:url" content="{e(url)}">',
                       f'<meta property="og:image" content="{e(SITE_URL)}/assets/images/og-image.png">',
                       '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
                       '<meta name="twitter:card" content="summary_large_image">']
        if has_twin:
            head_extra += [f'<link rel="alternate" hreflang="{m.LANG["code"]}" href="{e(page_url(m, filename))}">' for m in LANGS]
            head_extra.append(f'<link rel="alternate" hreflang="x-default" href="{e(page_url(EN, filename))}">')
    if not INDEXABLE or slug == '404':
        head_extra.append('<meta name="robots" content="noindex">')
    if slug == 'index' and C is EN:
        head_extra.append(organization_jsonld())
    # Arabic preloads Readex Pro; Chinese and Japanese use the visitor's system fonts
    # (CJK web fonts are several MB), with Plex Sans for any Latin text.
    font = 'readex-pro-arabic' if lang['code'] == 'ar' else 'ibm-plex-sans-latin'
    preloads = ''.join(f'<link rel="preload" href="{asset(f"fonts/{font}-{w}.woff2")}" as="font" type="font/woff2" crossorigin>\n'
                       for w in (400, 600))

    service_links = ''.join(f'<li><a href="{a["href"]}">{e(a["label"])}</a></li>' for a in AREAS)
    emails = ''.join(f'<li>{mailto(m)}</li>' for m in C.SITE['emails'])
    phones = ''.join(f'<li>{tel(p, n)}</li>' for p, n in C.SITE['phones'])
    apps = ''
    if channels():
        items = []
        for ch in channels():
            external = ch['key'] != 'wechat'
            attrs = ' target="_blank" rel="noopener"' if external else ''
            sr = f'<span class="visually-hidden">{e(t("new_tab"))}</span>' if external else ''
            items.append(f'<li><a href="{e(ch["href"])}"{attrs}>{brand_icon(ch["key"])}{e(ch["name"])}{sr}</a></li>')
        apps = f'<p class="footer-apps-title">{e(t("messaging"))}</p><ul class="footer-apps">{"".join(items)}</ul>'
    social = ''
    if C.SITE['social']:
        social = (f'<div><h2 class="footer-title">{e(t("footer_follow"))}</h2><ul>' + ''.join(
            f'<li>{link_arrow(u, n, external=True)}</li>' for n, u in C.SITE['social']) + '</ul></div>')

    return f'''<!doctype html>
<html lang="{lang["code"]}" dir="{lang["dir"]}">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description)}">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b1622" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(C.SITE["name"])}">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(description)}">
{chr(10).join(head_extra)}
<link rel="icon" href="{asset("images/favicon.svg")}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{asset("images/apple-touch-icon.png")}">
{preloads}<link rel="stylesheet" href="{asset("css/styles.css")}">
<script>{HEAD_SCRIPT}</script>
<script src="{asset("js/app.js")}" defer></script>
</head>
<body>
<a class="skip-link" href="#main">{e(t("skip"))}</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="index.html" aria-label="{e(t("home_alt"))}">{LOGO_INLINE}</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{e(t("menu_open"))}" data-label-open="{e(t("menu_open"))}" data-label-close="{e(t("menu_close"))}">{icon("menu", "icon")}{icon("close", "icon")}</button>
    <nav class="site-nav" id="site-nav" aria-label="{e(t("nav_label"))}">
      {nav}
      <a class="button button--sm" href="contact.html"{contact_cur}>{e(t("nav_contact"))}</a>
    </nav>
    {lang_menu}
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html"><img src="{asset("images/" + LOGO_LIGHT)}" alt="{e(t("home_alt"))}" width="{round(28 * LOGO_RATIO)}" height="28" loading="lazy" decoding="async"></a>
        <p class="footer-tagline">{e(C.SITE["tagline"])}</p>
      </div>
      <div>
        <h2 class="footer-title">{e(t("footer_services"))}</h2>
        <ul>{service_links}</ul>
      </div>
      <div>
        <h2 class="footer-title">{e(t("footer_company"))}</h2>
        <ul><li><a href="about.html">{e(t("nav_about"))}</a></li><li><a href="sectors.html">{e(t("nav_sectors"))}</a></li><li><a href="contact.html">{e(t("nav_contact"))}</a></li></ul>
      </div>
      <div>
        <h2 class="footer-title">{e(t("footer_contact"))}</h2>
        <ul>{emails}{phones}</ul>
        {apps}
        <p class="footer-address">{"<br>".join(e(x) for x in C.SITE["address"])}</p>
        <p class="footer-map">{link_arrow(C.SITE["maps"], t("maps"), external=True)}</p>
      </div>
      {social}
    </div>
    <div class="footer-bottom">
      <span>© {YEAR} {e(C.SITE["name"])}</span>
      <span class="footer-legal"><a href="privacy.html">{e(t("privacy"))}</a><a href="terms.html">{e(t("terms"))}</a></span>
      <ul class="footer-langs" aria-label="{e(t("language"))}">{lang_links()}</ul>
    </div>
  </div>
</footer>
</body>
</html>
'''


def organization_jsonld():
    """Company details for search engines (name, address, phones, email, logo)."""
    street, city = ', '.join(EN.SITE['address'][:2]), EN.SITE['address'][2].split(',')[0]
    data = {
        '@context': 'https://schema.org', '@type': 'ProfessionalService', 'name': EN.SITE['name'],
        'description': EN.SITE['tagline'], 'email': EN.SITE['enquiry_email'],
        'telephone': [n for _, n in EN.SITE['phones']],
        'address': {'@type': 'PostalAddress', 'streetAddress': street, 'addressLocality': city, 'addressCountry': 'SA'},
        'areaServed': 'Saudi Arabia', 'availableLanguage': ['en', 'ar'],
    }
    if SITE_URL:
        data.update(url=f'{SITE_URL}/', logo=f'{SITE_URL}/assets/images/apple-touch-icon.png',
                    image=f'{SITE_URL}/assets/images/og-image.png')
    if EN.SITE['social']:
        data['sameAs'] = [u for _, u in EN.SITE['social']]
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
        t('hero_eyebrow'), t('hero_title'), t('hero_lead'),
        actions=button('contact.html', t('cta_discuss')) + link_arrow('services.html', t('explore_services')),
        extra=stats, cls='hero--home')

    services = section(
        t('services_eyebrow'), t('services_heading'),
        rows([dict(num=num(i + 1), title=a['label'], desc=a['short'], href=a['href']) for i, a in enumerate(AREAS)]),
        intro=t('services_intro'),
        footer='<div class="actions actions--tight">' + button('contact.html', t('cta_discuss'))
               + link_arrow('services.html', t('all_services')) + '</div>')

    steps = '<ol class="steps">' + ''.join(
        f'<li class="step"><span class="step__num">{num(i + 1)}</span><h3>{e(x)}</h3><p>{e(d)}</p></li>'
        for i, (x, d) in enumerate(C.STEPS)) + '</ol>'
    approach = section(t('how_eyebrow'), t('how_heading'), steps, intro=t('how_intro'))

    who = section(
        t('who_eyebrow'), t('who_heading'),
        f'''<p class="body-lg">{e(t("who_body"))}</p>
        <div class="panel">
          <p class="eyebrow">{e(t("partner_eyebrow"))}</p>
          <p class="panel__title">{e(t("partner_short_name"))}</p>
          <p>{e(t("partner_short_body"))}</p>
          {link_arrow('about.html#partnership', t('our_partnership'))}
        </div>''',
        footer=link_arrow('about.html', t('about_link')))

    network = section_wide(t('clients_eyebrow'), t('clients_heading'), logos(C.CLIENTS_NETWORK),
                           intro=t('clients_intro'), id='clients')

    sectors = section(
        t('sectors_eyebrow'), t('sectors_heading'),
        rows([dict(num=num(i + 1), title=s['label'], desc=s['desc'], href=f'sectors.html#{s["slug"]}')
              for i, s in enumerate(C.SECTORS)], compact=True),
        intro=t('sectors_intro'), footer=link_arrow('sectors.html', t('all_sectors')))

    body = hero + services + approach + who + network + sectors + cta(
        t('home_cta_title'), t('home_cta_body'), t('cta_discuss'))
    page('index', t('home_title'), t('home_desc'), body)


def build_services():
    hero = page_hero(t('services_eyebrow'), t('services_hero_title'), t('services_hero_lead'))
    listing = section(
        t('areas_eyebrow'), t('areas_heading'),
        rows([dict(num=num(i + 1), title=a['label'], desc=a['short'], href=a['href'], meta=a['tag'],
                   extra='<span class="row__tags">' + ''.join(f'<span>{e(x)}</span>' for x in a['items'][:3]) + '</span>')
              for i, a in enumerate(AREAS)]),
        intro=t('areas_intro'))
    journey = section(
        t('journey_eyebrow'), t('journey_heading'),
        f'<p class="body-lg">{e(t("journey_body"))}</p>'
        '<p class="journey">' + ''.join(f'<span>{e(x)}</span>' for x in t('journey_steps')) + '</p>')
    page('services', t('services_title'), t('services_desc'),
         hero + listing + journey + cta(t('services_cta_title'), t('services_cta_body'), t('cta_discuss')))


def build_detail(item, is_sector=False):
    slug = item['slug']
    parent = (t('nav_sectors'), 'sectors.html') if is_sector else (t('nav_services'), 'services.html')
    hero = page_hero(
        item['tag'], item['title'], item['intro'],
        actions=button(f'contact.html?interest={slug}', t('discuss_project') if is_sector else t('discuss_service'))
        + link_arrow('#support', t('where_help_link')),
        crumbs=[(t('home'), 'index.html'), parent, (item['label'], '')])

    overview = section(t('overview_eyebrow'), t('overview_heading'), f'<p class="body-lg">{e(item["overview"])}</p>')

    if item.get('areas'):
        support_body = '<div class="areas">' + ''.join(
            f'<div class="area" id="{a["id"]}"><span class="area__num">{num(i + 1)}</span><h3>{e(a["label"])}</h3>'
            f'<p>{e(a["short"])}</p>{plain_list(a["items"])}</div>'
            for i, a in enumerate(item['areas'])) + '</div>'
    else:
        support_body = plain_list(item['needs'])
    support = section(t('support_eyebrow'), t('support_heading'), support_body, id='support')

    outcomes = section(
        t('outcomes_eyebrow'), t('outcomes_heading'),
        f'''<div class="cols">
          <div><h3>{e(t("challenges_title"))}</h3><p class="small">{e(t("challenges_sub"))}</p>{plain_list(item["challenges"], numbered=True)}</div>
          <div><h3>{e(t("outputs_title"))}</h3><p class="small">{e(t("outputs_sub"))}</p>{plain_list(item["deliverables"], numbered=True)}</div>
        </div>''')

    questions = section(t('faq_eyebrow'), t('faq_heading'), faq(item['faq']))

    related_items = [s for s in C.SERVICES if s['slug'] != slug][:3]
    related = section(t('related_eyebrow'), t('related_heading'),
                      rows([dict(title=s['label'], desc=s['short'], href=f'{s["slug"]}.html') for s in related_items]))

    body = hero + overview + support + outcomes + questions + related + cta(
        t('detail_cta_title'), t('detail_cta_body'),
        t('discuss_project') if is_sector else t('enquire_service'), href=f'contact.html?interest={slug}')
    page(slug, item['label'], item['intro'], body)


def build_sectors():
    hero = page_hero(t('sectors_eyebrow'), t('sectors_hero_title'), t('sectors_hero_lead'))
    items = []
    for i, s in enumerate(C.SECTORS):
        extra = (f'<span class="row__more">{link_arrow(s["link"], s["link_label"])}</span>' if s['link'] else '')
        items.append(dict(id=s['slug'], num=num(i + 1), title=s['label'], desc=s['desc'], meta=s['category'], extra=extra))
    listing = section(t('focus_eyebrow'), t('focus_heading'), rows(items), intro=t('focus_intro'))
    why = section(t('why_eyebrow'), t('why_heading'), f'<p class="body-lg">{e(t("why_body"))}</p>',
                  footer=link_arrow('life-sciences.html', t('ls_link')))
    page('sectors', t('sectors_title'), t('sectors_desc'),
         hero + listing + why + cta(t('sectors_cta_title'), t('sectors_cta_body'), t('sectors_cta_label')))


def build_about():
    hero = page_hero(t('nav_about'), t('about_hero_title'), t('about_hero_lead'))
    who = section(
        t('who_eyebrow'), t('about_who_heading'),
        f'<p class="body-lg">{e(t("about_who_body"))}</p>'
        f'<blockquote class="statement"><p>{e(t("about_statement"))}</p></blockquote>')
    values = section(
        t('values_eyebrow'), t('values_heading'),
        '<ul class="grid-values">' + ''.join(
            f'<li><span class="area__num">{num(i + 1)}</span><h3>{e(x)}</h3><p>{e(d)}</p></li>'
            for i, (x, d) in enumerate(C.VALUES)) + '</ul>')
    partner = section(
        t('partnership_eyebrow'), t('partnership_heading'),
        f'<p class="body-lg">{e(t("partnership_body"))}</p>'
        f'<figure class="photo">{img(C.PARTNER["photo"], C.PARTNER["photo_alt"])}'
        f'<figcaption>{e(C.PARTNER["photo_alt"])}{e(t("period"))}</figcaption></figure>'
        f'<div class="panel"><p class="eyebrow">{e(t("partner_eyebrow"))}</p>'
        f'<p class="panel__title">{e(C.PARTNER["name"])}</p>'
        f'<p>{e(t("partner_location"))}</p>'
        f'{link_arrow(C.PARTNER["url"], t("visit_partner"), external=True)}</div>'
        + (f'<h3 class="group-title group-title--logos">{e(C.PARTNER_CLIENTS_LABEL)}</h3>'
           + logos(C.CLIENTS_GLOBAL) if C.SHOW_PARTNER_CLIENTS else ''),
        id='partnership')

    def avatar(name, photo):
        if photo:
            return img(f'team/{photo}.webp', '', height=56, cls='avatar')
        initials = ''.join(w[0] for w in name.split()[:2])
        return f'<span class="avatar avatar--initials" aria-hidden="true">{e(initials)}</span>'

    def people(arr):
        # Names stay in Latin script; lang="en" gives screen readers the right pronunciation.
        name_lang = '' if C is EN else ' lang="en"'
        return '<ul class="people">' + ''.join(
            f'<li>{avatar(n, ph)}<span><span class="people__name"{name_lang}>{e(n)}</span>'
            f'<span class="people__role">{e(r)}</span></span></li>'
            for n, r, ph in arr) + '</ul>'

    # Full width, so the 26 people fill rows across the page instead of one long column.
    team = section_wide(
        t('team_eyebrow'), t('team_heading'),
        f'<h3 class="group-title">{e(t("team_saudi"))} <span>{len(C.TEAM_SAUDI)}</span></h3>{people(C.TEAM_SAUDI)}'
        f'<h3 class="group-title">{e(t("team_international"))} <span>{len(C.TEAM_INTERNATIONAL)}</span></h3>{people(C.TEAM_INTERNATIONAL)}',
        intro=t('team_intro'), id='team')
    page('about', t('about_title'), t('about_desc'),
         hero + who + values + partner + team + cta(t('about_cta_title'), t('about_cta_body'), t('about_cta_label')))


def build_contact():
    wa = next((ch for ch in channels() if ch['key'] == 'whatsapp'), None)
    hero = page_hero(t('nav_contact'), t('contact_hero_title'), t('contact_hero_lead'),
                     actions=link_arrow(wa['href'], wa['action'], external=True, brand='whatsapp') if wa else '')

    def channel_row(ch):
        dt = f'<dt>{brand_icon(ch["key"])}{e(ch["name"])}</dt>'
        if ch['key'] == 'wechat':
            qr = (f'<img class="wechat-qr" src="{asset("images/contact/" + ch["qr"])}" alt="{e(t("wechat_qr_alt"))}" '
                  f'width="160" height="160" loading="lazy">' if ch['qr'] else '')
            return (f'<div id="wechat">{dt}<dd><span class="channel-id"><code dir="ltr">{e(ch["value"])}</code>'
                    f'<button class="copy-button" type="button" data-copy="{e(ch["value"])}" data-copied="{e(t("copied"))}" hidden>'
                    f'{e(t("copy"))}</button></span><span class="dd-note">{e(t("wechat_hint"))}</span>{qr}</dd></div>')
        return (f'<div>{dt}<dd>{link_arrow(ch["href"], ch["action"], external=True)}'
                f'<span class="dd-note" dir="ltr">{e(ch["value"])}</span></dd></div>')

    options = [(s['slug'], s.get('option', s['label'])) for s in C.SERVICES]
    options += [('life-sciences', C.LIFE_SCIENCES['label']), ('other', t('f_other'))]
    opts = ''.join(f'<option value="{v}">{e(l)}</option>' for v, l in options)

    def field(fid, label, control, required=False, hint=''):
        req = ' <span class="req" aria-hidden="true">*</span>' if required else ''
        hint_html = f'<p class="field-hint" id="{fid}-hint">{e(hint)}</p>' if hint else ''
        return (f'<div class="field"><label for="{fid}">{e(label)}{req}</label>{hint_html}{control}'
                f'<p class="field-error" id="{fid}-error"></p></div>')

    def described(fid, hint=False):
        ids = ([f'{fid}-hint'] if hint else []) + [f'{fid}-error']
        return f'aria-describedby="{" ".join(ids)}"'

    i18n = dict(required=t('js_required'), email=t('js_email'), min=t('js_min'), fixOne=t('js_fix_one'),
                fixMany=t('js_fix_many'), ok=t('js_ok'), okManual=t('js_ok_manual'), subject=t('js_subject'),
                labels=dict(name=t('js_lbl_name'), email=t('js_lbl_email'), company=t('js_lbl_company'),
                            phone=t('js_lbl_phone'), interest=t('js_lbl_interest')))

    form = f'''
<form class="form" id="enquiry-form" novalidate data-to="{e(C.SITE["enquiry_email"])}" data-i18n="{e(json.dumps(i18n, ensure_ascii=False))}">
  <p class="small">{e(t("required_before"))} <span class="req" aria-hidden="true">*</span><span class="visually-hidden">{e(t("required_sr"))}</span> {e(t("required_after"))}</p>
  <div class="form-row">
    {field('f-name', t('f_name'), f'<input id="f-name" name="name" autocomplete="name" required {described("f-name")} data-required="{e(t("f_name_req"))}">', True)}
    {field('f-email', t('f_email'), f'<input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" dir="ltr" required {described("f-email")} data-required="{e(t("f_email_req"))}">', True)}
  </div>
  <div class="form-row">
    {field('f-company', t('f_company'), '<input id="f-company" name="company" autocomplete="organization">')}
    {field('f-phone', t('f_phone'), '<input id="f-phone" name="phone" type="tel" autocomplete="tel" dir="ltr">')}
  </div>
  {field('f-interest', t('f_interest'), f'<select id="f-interest" name="interest" required {described("f-interest")} data-required="{e(t("f_interest_req"))}"><option value="">{e(t("f_choose"))}</option>{opts}</select>', True)}
  {field('f-message', t('f_message'), f'<textarea id="f-message" name="message" rows="6" minlength="20" required {described("f-message", True)} data-required="{e(t("f_message_req"))}"></textarea>', True, hint=t('f_message_hint'))}
  <div class="form-status" id="form-status" role="status" aria-live="polite"></div>
  <button class="button" type="submit">{e(t("submit"))}</button>
  <p class="small">{e(t("form_note"))} <a href="privacy.html">{e(t("privacy"))}</a>{e(t("form_note_end"))}</p>
</form>'''

    details = '<dl class="contact-list">' + ''.join(
        f'<div><dt>{e(t("email_label"))}</dt><dd>{mailto(m)}</dd></div>' for m in C.SITE['emails']) + ''.join(
        f'<div><dt>{e(t("phone_label"))}</dt><dd>{tel(p, n)}</dd></div>' for p, n in C.SITE['phones']) + ''.join(
        channel_row(ch) for ch in channels()) + (
        f'<div><dt>{e(t("office_label"))}</dt><dd>{e(C.LANG["sep"]).join(e(x) for x in C.SITE["address"])}'
        f'<span class="dd-link">{link_arrow(C.SITE["maps"], t("maps"), external=True)}</span></dd></div>') + (
        f'<div><dt>{e(t("social_label"))}</dt><dd class="dd-links">' + ''.join(link_arrow(u, n, external=True) for n, u in C.SITE['social'])
        + '</dd></div>' if C.SITE['social'] else '') + '</dl>'

    body = hero + f'''
<section class="section">
  <div class="wrap split">
    <div class="split__head">
      <p class="eyebrow">{e(t("direct_eyebrow"))}</p>
      <h2>{hl(t("direct_heading"))}</h2>
      {details}
    </div>
    <div class="split__body">
      <h2 class="visually-hidden">{e(t("form_heading"))}</h2>
      {form}
    </div>
  </div>
</section>'''
    page('contact', t('contact_title'), t('contact_desc'), body)


def build_legal():
    updated = f'<p class="legal-date">{e(t("last_updated", date=C.LEGAL_UPDATED))}</p>'
    terms_text = C.TERMS
    terms = (page_hero(t('legal_eyebrow'), t('terms'), t('terms_lead'))
             + section(t('disclaimer_eyebrow'), t('disclaimer_heading'),
                       updated + ''.join(f'<p>{e(x)}</p>' for x in terms_text['disclaimer']), id='disclaimer')
             + section(t('termsofuse_eyebrow'), t('termsofuse_heading'),
                       f'<p>{e(terms_text["intro"])}</p><ol class="legal-clauses">' + ''.join(
                           f'<li><h3>{e(h)}</h3><p>{e(x)}</p></li>' for h, x in terms_text['clauses']) + '</ol>', id='terms'))
    page('terms', t('terms'), t('terms_desc'), terms)

    pr = C.PRIVACY
    contact = f'<p>{e(t("privacy_contact"))} {mailto(pr["contact"])}{e(t("period"))}</p>'
    privacy = (page_hero(t('legal_eyebrow'), t('privacy'), t('privacy_lead'))
               + section(t('privacy_eyebrow'), t('privacy_heading'),
                         updated + ''.join(f'<p>{e(x)}</p>' for x in pr['paragraphs']) + contact + f'<p>{e(pr["changes"])}</p>'))
    page('privacy', t('privacy'), t('privacy_desc'), privacy)


def build_404():
    """One 404 page at the site root (GitHub Pages serves only that one), with a note in every language."""
    others = '<div class="nf-alts">' + ''.join(
        f'<p class="nf-alt" lang="{m.LANG["code"]}" dir="{m.LANG["dir"]}">{e(m.UI["nf_title"])} {e(m.UI["nf_lead"])} '
        f'<a href="{m.LANG["path"]}index.html">{e(m.UI["nf_home"])}</a></p>' for m in LANGS if m is not EN) + '</div>'
    body = page_hero(t('nf_eyebrow'), t('nf_title'), t('nf_lead'),
                     actions=button('index.html', t('nf_home')) + link_arrow('contact.html', t('nf_contact')),
                     extra=others)
    page('404', t('nf_title').rstrip('.'), t('nf_lead'), body)


def redirect_page(new):
    target = f'{SITE_URL}/{new}' if SITE_URL else new
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Page moved | {e(EN.SITE["name"])}</title>
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


def build_language(mod):
    set_language(mod)
    PAGES.clear()
    build_home()
    build_services()
    for s in C.SERVICES:
        build_detail(s)
    build_detail(C.LIFE_SCIENCES, is_sector=True)
    build_sectors()
    build_about()
    build_contact()
    build_legal()
    if mod is EN:
        build_404()
    out = OUT / mod.LANG['path']
    out.mkdir(parents=True, exist_ok=True)
    for name, html in PAGES.items():
        (out / name).write_text(html, encoding='utf-8')
    return sorted(PAGES)


# --------------------------------------------------------------------------- checks

class _Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.h1 = [], [], 0
        self.empty_headings, self._heading, self._heading_text = 0, None, ''
        self.html_lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.html_lang = a.get('lang')
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
        for candidate in (a.get('srcset') or '').split(','):
            if candidate.strip():
                self.links.append(candidate.split()[0])

    def handle_data(self, data):
        if self._heading:
            self._heading_text += data

    def handle_endtag(self, tag):
        if tag == self._heading:
            if not self._heading_text.strip():
                self.empty_headings += 1
            self._heading = None


INVISIBLE = re.compile('[​‌‍⁠﻿]')


def check(out):
    parsed = {}
    for p in out.rglob('*.html'):
        c = _Collector()
        text = p.read_text(encoding='utf-8')
        c.feed(text)
        c.invisible = len(INVISIBLE.findall(text))
        parsed[p.resolve()] = c
    errors = []
    for path, c in parsed.items():
        name = path.relative_to(out.resolve())
        if c.h1 != 1:
            errors.append(f'{name}: expected one <h1>, found {c.h1}')
        if c.empty_headings:
            errors.append(f'{name}: {c.empty_headings} empty heading(s)')
        if c.invisible:
            errors.append(f'{name}: {c.invisible} invisible character(s)')
        folder = name.parts[0] + '/' if len(name.parts) > 1 else ''
        expected = next((m.LANG['code'] for m in LANGS if m.LANG['path'] == folder), None)
        if expected and name.name not in [f'{old}.html' for old in REDIRECTS] and c.html_lang != expected:
            errors.append(f'{name}: expected lang="{expected}", found "{c.html_lang}"')
        dupes = {i for i in c.ids if c.ids.count(i) > 1}
        if dupes:
            errors.append(f'{name}: duplicate ids {sorted(dupes)}')
        for link in c.links:
            u = urlsplit(link)
            if u.scheme or link.startswith('//'):
                continue  # external, mailto:, tel:
            target = (path.parent / u.path).resolve() if u.path else path
            if not target.exists():
                errors.append(f'{name}: broken link "{link}"')
            elif u.fragment and target.suffix == '.html' and u.fragment not in parsed[target].ids:
                errors.append(f'{name}: missing anchor "{link}"')
    return errors


# --------------------------------------------------------------------------- main

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / 'assets', OUT / 'assets')
    (OUT / 'assets' / 'images' / LOGO_LIGHT).write_text(
        LOGO_SVG.replace('color="#0f2137"', f'color="{LOGO_BEIGE}"', 1), encoding='utf-8')

    built = {mod.LANG['code']: build_language(mod) for mod in LANGS}
    set_language(EN)
    for old, new in REDIRECTS.items():
        assert f'{old}.html' not in built['en'], old
        (OUT / f'{old}.html').write_text(redirect_page(new), encoding='utf-8')

    robots = 'User-agent: *\n' + ('Allow: /\n' if INDEXABLE else 'Disallow: /\n')
    if SITE_URL:
        urls = [page_url(m, n) for m in LANGS for n in built[m.LANG['code']] if n != '404.html']
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
    if ENV_PLACEHOLDERS:
        print(f'Note: site.env still has placeholder values for {", ".join(sorted(ENV_PLACEHOLDERS))}; '
              'replace them before sharing the site.', file=sys.stderr)
    counts = ', '.join(f'{len(v)} {k}' for k, v in built.items())
    print(f'Built {counts} pages into {OUT.relative_to(ROOT)}/ '
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
