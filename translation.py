"""Shared by the translated content files (content_ar.py, content_zh.py, content_ja.py).

Each of those files supplies text only, in private tables (_SERVICES, _LIFE_SCIENCES,
_SERVICE_AREAS, _SECTORS, _ROLES) plus VALUES, STEPS, STATS, PARTNER, LEGAL_UPDATED, TERMS, PRIVACY,
SITE and UI. complete() fills in everything else from content.py (slugs, links,
photos, numbers, logos) and fails loudly if a translation is missing or has a
different number of items from the English, so the languages can't drift apart.

Two exceptions, both explicit in the translation file:
- LOCAL_KEYS / AREA_LOCAL_KEYS: a translation may give a page its own text where the English
  page borrows it from its service area (the Industrial page's own lead, approach and outcomes;
  a Services page summary that differs from the home page's). The build falls back to the
  shared text wherever a translation does not.
- _OWN_LENGTH: a set of (table, id, key) naming lists whose length the translation sets itself,
  because the site owner rewrote them with a different number of items. Every other list must
  have exactly as many items as the English one.
"""
import copy

import content as en

TEXT_KEYS = ('label', 'option', 'short', 'tag', 'title', 'intro', 'overview', 'overview_more', 'needs',
             'challenges_title', 'challenges', 'why', 'examples', 'deliverables', 'faq')
AREA_KEYS = ('label', 'home', 'approach_title', 'approach', 'support', 'outcomes')
LOCAL_KEYS = ('intro', 'approach', 'outcomes')   # a service page's own text, used instead of its area's
AREA_LOCAL_KEYS = ('summary',)                   # the Services page summary, used instead of 'home'


def _check_length(where, key, ours, theirs, own):
    if not isinstance(ours, list) or not ours:
        raise ValueError(f'{where}: "{key}" must be a non-empty list')
    if key not in own and len(ours) != len(theirs):
        raise ValueError(f'{where}: "{key}" has {len(ours)} items, English has {len(theirs)}')


def _item(item, tr, where, own=()):
    out = copy.deepcopy(item)
    for key in TEXT_KEYS:
        if key in item:
            if key not in tr:
                raise KeyError(f'{where}: missing "{key}"')
            if isinstance(item[key], list):
                _check_length(where, key, tr[key], item[key], own)
            out[key] = tr[key]
    for key in LOCAL_KEYS:
        if key in tr and key not in item:
            out[key] = tr[key]
    if item.get('areas'):
        out['areas'] = []
        for area in item['areas']:
            t = tr['areas'][area['id']]
            if len(t['items']) != len(area['items']):
                raise ValueError(f'{where}: area {area["id"]} item count differs from English')
            out['areas'].append(dict(area, **t))
    return out


def _area(area, tr, where, own=()):
    out = copy.deepcopy(area)
    for key in AREA_KEYS:
        if key in area:
            if key not in tr:
                raise KeyError(f'{where}: missing "{key}"')
            if isinstance(area[key], list):
                _check_length(where, key, tr[key], area[key], own)
            out[key] = tr[key]
    for key in AREA_LOCAL_KEYS:
        if key in tr:
            out[key] = tr[key]
    return out


def complete(ns):
    """Fill a translated content module's namespace in place. Call at the end of the module."""
    code = ns['LANG']['code']
    own = set(ns.get('_OWN_LENGTH', ()))
    tables = {'_SERVICES': {s['slug'] for s in en.SERVICES}, '_LIFE_SCIENCES': {'life-sciences'},
              '_SERVICE_AREAS': {a['id'] for a in en.SERVICE_AREAS}}
    for table, ident, key in own:
        if ident not in tables.get(table, ()):
            raise KeyError(f'{code}: _OWN_LENGTH names an unknown list {(table, ident, key)}')

    def own_keys(table, ident):
        return {k for t, i, k in own if t == table and i == ident}
    ns['SERVICES'] = [_item(s, ns['_SERVICES'][s['slug']], f'{code} service {s["slug"]}', own_keys('_SERVICES', s['slug']))
                      for s in en.SERVICES]
    ns['LIFE_SCIENCES'] = _item(en.LIFE_SCIENCES, ns['_LIFE_SCIENCES'], f'{code} life-sciences',
                                own_keys('_LIFE_SCIENCES', 'life-sciences'))
    ns['SERVICE_AREAS'] = [_area(a, ns['_SERVICE_AREAS'][a['id']], f'{code} service area {a["id"]}', own_keys('_SERVICE_AREAS', a['id']))
                           for a in en.SERVICE_AREAS]
    ns['SECTORS'] = [dict(s, **ns['_SECTORS'][s['slug']]) for s in en.SECTORS]
    for sector in ns['SECTORS']:
        if sector['link'] and 'link_label' not in ns['_SECTORS'][sector['slug']]:
            raise KeyError(f'{code}: missing link_label for sector {sector["slug"]}')
    roles = ns['_ROLES']
    ns['TEAM_SAUDI'] = [(n, roles[n], photo) for n, _role, photo in en.TEAM_SAUDI]
    ns['TEAM_INTERNATIONAL'] = [(n, roles[n], photo) for n, _role, photo in en.TEAM_INTERNATIONAL]
    for name in ('SHOW_PARTNER_CLIENTS', 'CLIENTS_NETWORK', 'CLIENTS_GLOBAL'):
        ns.setdefault(name, getattr(en, name))

    for name, ours, theirs in [('VALUES', ns['VALUES'], en.VALUES), ('STEPS', ns['STEPS'], en.STEPS),
                               ('STATS', ns['STATS'], en.STATS),
                               ('TERMS.clauses', ns['TERMS']['clauses'], en.TERMS['clauses']),
                               ('TERMS.disclaimer', ns['TERMS']['disclaimer'], en.TERMS['disclaimer']),
                               ('PRIVACY.paragraphs', ns['PRIVACY']['paragraphs'], en.PRIVACY['paragraphs'])]:
        if len(ours) != len(theirs):
            raise ValueError(f'{code}: {name} has {len(ours)} items, English has {len(theirs)}')
    missing, extra = set(en.UI) - set(ns['UI']), set(ns['UI']) - set(en.UI)
    if missing or extra:
        raise KeyError(f'{code}: UI keys missing {sorted(missing)} / extra {sorted(extra)}')
    for key, value in en.UI.items():
        if isinstance(value, list) and len(ns['UI'][key]) != len(value):
            raise ValueError(f'{code}: UI "{key}" has {len(ns["UI"][key])} items, English has {len(value)}')
