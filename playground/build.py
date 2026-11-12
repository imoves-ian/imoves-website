#!/usr/bin/env python3
"""Build the packages-and-prices block of the playground page.

    python3 playground/build.py

Reads the products, prices and feature rows from the data block of tools/versiond-compare.py (the
same data that generates the comparison table on the live homepage and /pricing), so the playground
can never show a different price. Rewrites the part of playground/site/index.html between
<!--GEN:packages--> and <!--/GEN:packages-->. Do not hand-edit that part.
"""
import html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'tools', 'versiond-compare.py')
PAGE = os.path.join(HERE, 'site', 'index.html')

# Run only the data block of the generator (it rewrites the live pages if run whole).
code = open(SRC, encoding='utf-8').read()
start = code.index('PLATFORM = ')
end = code.index('# product pages')
data = {}
exec(code[start:end], data)
PLATFORM, PRODUCTS, GROUPS = data['PLATFORM'], data['PRODUCTS'], data['GROUPS']

# Short descriptions, taken from each product page's meta description.
BLURB = {
    'blasts':   '250+ ready-to-use movement breaks to help children get active, refocus or calm down.',
    'learning': 'Ready-to-use movement activities for Maths, English, Science and the wider curriculum.',
    'dance':    'Progressive dance lessons for EYFS to KS2, with original music and video demonstrations.',
    'pe':       'Progressive PE planning, lessons, assessment and child-facing demonstrations.',
    'school':   'PE, active learning, movement breaks, wellbeing and staff support – the lot.',
}
TIERS = [('i', 'Infant school', 'EYFS and KS1'), ('j', 'Junior school', 'KS2'), ('p', 'Primary school', 'EYFS, KS1 and KS2')]
DEFAULT = 'p'
esc = html.escape

every = GROUPS[0]
specific = GROUPS[1:]

out = []
out.append('<div class="tier-bar reveal"><div class="tiers" role="group" aria-label="School type">')
for t, name, ks in TIERS:
    out.append(f'<button type="button" data-tier="{t}" aria-pressed="{str(t == DEFAULT).lower()}">{esc(name)}<small>{esc(ks)}</small></button>')
out.append('</div></div>')
labels = ' '.join(f'data-l{t}="{esc(name)} ({esc(ks)})"' for t, name, ks in TIERS)
default_label = next(f'{n} ({k})' for t, n, k in TIERS if t == DEFAULT)
out.append(f'<p class="tier-note">Showing prices for a <span data-tier-label {labels}>{esc(default_label)}</span>. Per school per year, plus VAT.</p>')

out.append('<div class="pkg-grid">')
for k, name, bg, colour, pid, prices in PRODUCTS:
    p = dict(zip('ijp', prices))
    feats = [label for _, rows in specific for label, who in rows if k in who]
    featured = k == 'school'
    out.append(f'<article class="pkg reveal{" featured" if featured else ""}" style="--bg:{bg};--c:{colour}" '
               + ' '.join(f'data-p{t}="{v}"' for t, v in p.items()) + '>')
    if featured: out.append('<span class="badge">Everything included</span>')
    out.append(f'<h3>{esc(name)}</h3><p class="blurb">{esc(BLURB[k])}</p>')
    out.append(f'<div class="price"><span data-price>£{p[DEFAULT]}</span> <small>/ year</small></div><div class="per">plus VAT · 28-day free trial</div>')
    out.append('<ul>' + ''.join(f'<li>{esc(f)}</li>' for f in feats) + '</ul>')
    out.append(f'<a class="btn" href="{PLATFORM}{pid}">Get {esc(name)}</a></article>')
out.append('</div>')

out.append('<p class="every reveal"><strong>Every package includes:</strong> '
           + ', '.join(esc(l[0].lower() + l[1:]) if not l.startswith('Online') else esc(l) for l, _ in every[1]) + '.</p>')
out.append('<p class="discount reveal">Get <strong>30% discount</strong> if your school is small. '
           'Message <a href="mailto:kirsty@imoves.com">kirsty@imoves.com</a> for your unique discount code.</p>')

# full comparison matrix, folded away
out.append('<details class="compare reveal"><summary>Compare every feature</summary><div class="table-scroll"><table class="matrix">')
out.append('<thead><tr><th scope="col">Feature</th>' + ''.join(f'<th scope="col" style="--c:{c}">{esc(n)}</th>' for k, n, bg, c, pid, pr in PRODUCTS) + '</tr></thead><tbody>')
for gname, rows in GROUPS:
    out.append(f'<tr class="grp"><td colspan="{len(PRODUCTS) + 1}">{esc(gname)}</td></tr>')
    for label, who in rows:
        out.append(f'<tr><td>{esc(label)}</td>' + ''.join(
            '<td class="y" aria-label="Included">✓</td>' if k in who else '<td class="n" aria-label="Not included">–</td>'
            for k, *_ in PRODUCTS) + '</tr>')
out.append(f'<tr class="grp"><td colspan="{len(PRODUCTS) + 1}">Price per year, plus VAT</td></tr>')
for i, (t, name, ks) in enumerate(TIERS):
    out.append(f'<tr class="pr"><td>{esc(name)}<small>{esc(ks)}</small></td>' + ''.join(f'<td>£{pr[i]}</td>' for *_, pr in PRODUCTS) + '</tr>')
out.append('</tbody></table></div></details>')

block = '<!--GEN:packages-->\n' + '\n'.join(out) + '\n<!--/GEN:packages-->'
page = open(PAGE, encoding='utf-8').read()
page, n = re.subn(r'<!--GEN:packages-->.*?<!--/GEN:packages-->', lambda m: block, page, flags=re.S)
assert n == 1, 'GEN markers not found'
open(PAGE, 'w', encoding='utf-8').write(page)
print(f'packages block rebuilt: {len(PRODUCTS)} products from {os.path.relpath(SRC, HERE)}')
