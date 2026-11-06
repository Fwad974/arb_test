"""Shared by the translated content files (content_ar.py, content_zh.py, content_ja.py).

Each of those files supplies text only, in private tables (_SERVICES, _LIFE_SCIENCES,
_SECTORS, _ROLES) plus VALUES, STEPS, STATS, PARTNER, LEGAL_UPDATED, TERMS, PRIVACY,
SITE and UI. complete() fills in everything else from content.py (slugs, links,
photos, numbers, logos) and fails loudly if a translation is missing or has a
different number of items from the English, so the languages can't drift apart.
"""
import copy

import content as en

TEXT_KEYS = ('label', 'option', 'short', 'tag', 'title', 'intro', 'overview', 'needs', 'challenges', 'deliverables', 'faq')


def _item(item, tr, where):
    out = copy.deepcopy(item)
    for key in TEXT_KEYS:
        if key in item:
            if key not in tr:
                raise KeyError(f'{where}: missing "{key}"')
            if isinstance(item[key], list) and len(item[key]) != len(tr[key]):
                raise ValueError(f'{where}: "{key}" has {len(tr[key])} items, English has {len(item[key])}')
            out[key] = tr[key]
    if item.get('areas'):
        out['areas'] = []
        for area in item['areas']:
            t = tr['areas'][area['id']]
            if len(t['items']) != len(area['items']):
                raise ValueError(f'{where}: area {area["id"]} item count differs from English')
            out['areas'].append(dict(area, **t))
    return out


def complete(ns):
    """Fill a translated content module's namespace in place. Call at the end of the module."""
    code = ns['LANG']['code']
    ns['SERVICES'] = [_item(s, ns['_SERVICES'][s['slug']], f'{code} service {s["slug"]}') for s in en.SERVICES]
    ns['LIFE_SCIENCES'] = _item(en.LIFE_SCIENCES, ns['_LIFE_SCIENCES'], f'{code} life-sciences')
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
