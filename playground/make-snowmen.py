#!/usr/bin/env python3
"""Option for Ian: dancing snowmen in the space under the Active Advent banner text.

    python3 playground/make-snowmen.py

Takes the Active Advent page as it is on main (v0.33, with the smaller gap), gives the banner back
some height at the bottom and fills it with a row of dancing snowmen, gingerbread people and a penguin (simple flat drawings in
brand colours, gently bouncing and waving; still for anyone who has asked their device to reduce
motion). Writes playground/site/active-advent-snowmen/index.html, so it can be compared with
the v0.33 page on the development view. Images load from imoves.com; GTM is removed.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from advent_doors import review_panel  # noqa: E402

t = subprocess.run(['git', '-C', ROOT, 'show', 'origin/main:active-advent/index.html'], check=True, capture_output=True).stdout.decode()


def suball(old, new, s):
    assert s.count(old) == 1, f'{s.count(old)} found: {old[:70]!r}'
    return s.replace(old, new)


t = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', t, flags=re.S)
t = re.sub(r'<script>\(function\(w,d,s,l,i\).*?</script>', '', t, flags=re.S)
t = re.sub(r'<noscript><iframe[^>]*googletagmanager[^>]*></iframe></noscript>', '', t)
assert 'googletagmanager' not in t
t = suball('<head>', '<head><meta name="robots" content="noindex, nofollow">', t)

# room for the snowmen at the bottom of the banner
t = suball('data-home-banner="6aecc75b426d5" style="padding-bottom:36px;',
           'data-home-banner="6aecc75b426d5" data-suggest="1" style="padding-bottom:clamp(120px,14vw,200px);', t)

# five snowmen: scarf colour, hat colour, hat band
LOOKS = [('#E03C31', '#702F8A', '#05A445'), ('#0085CA', '#E03C31', '#FBC697'), ('#05A445', '#0085CA', '#E03C31'),
         ('#F65275', '#702F8A', '#F68D2E'), ('#702F8A', '#05A445', '#E03C31')]


def snowman(i, scarf, hat, band):
    return f'''<svg class="sm sm{i}" viewBox="0 0 100 140" aria-hidden="true">
<ellipse cx="50" cy="136" rx="30" ry="4" fill="#9663A8" opacity=".35"/>
<g class="sm-body">
 <g class="sm-arm sm-arm-l"><path d="M30 68 L8 48 M14 54 l-8 -2 M14 54 l-2 -8" stroke="#702F8A" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>
 <g class="sm-arm sm-arm-r"><path d="M70 68 L92 48 M86 54 l8 -2 M86 54 l2 -8" stroke="#702F8A" stroke-width="3.5" stroke-linecap="round" fill="none"/></g>
 <circle cx="50" cy="106" r="29" fill="#fff" stroke="#BFE1F2" stroke-width="3"/>
 <path d="M30 118 a29 29 0 0 0 40 0" fill="none" stroke="#BFE1F2" stroke-width="4" stroke-linecap="round"/>
 <circle cx="50" cy="68" r="21" fill="#fff" stroke="#BFE1F2" stroke-width="3"/>
 <circle cx="50" cy="61" r="2.6" fill="#24152b"/><circle cx="50" cy="70" r="2.6" fill="#24152b"/><circle cx="50" cy="79" r="2.6" fill="#24152b"/>
 <circle cx="50" cy="34" r="16" fill="#fff" stroke="#BFE1F2" stroke-width="3"/>
 <circle cx="44.5" cy="31" r="2.3" fill="#24152b"/><circle cx="55.5" cy="31" r="2.3" fill="#24152b"/>
 <path d="M50 35 L64 38 L50 40 Z" fill="#F68D2E"/>
 <path d="M43 42 q7 5 14 0" stroke="#24152b" stroke-width="2" fill="none" stroke-linecap="round"/>
 <path d="M33 48 q17 8 34 0 l1 6 q-18 8 -36 0 z" fill="{scarf}"/>
 <path d="M58 52 l6 18 l-7 1 l-4 -17 z" fill="{scarf}"/>
 <rect x="38" y="6" width="24" height="15" rx="2" fill="{hat}"/>
 <rect x="38" y="16" width="24" height="4" fill="{band}"/>
 <rect x="31" y="19" width="38" height="5" rx="2.5" fill="{hat}"/>
</g></svg>'''


def gingerbread(i):
    return f"""<svg class="sm sm{i}" viewBox="0 0 100 140" aria-hidden="true">
<ellipse cx="50" cy="136" rx="28" ry="4" fill="#9663A8" opacity=".35"/>
<g class="sm-body">
 <g class="sm-arm sm-arm-l"><path d="M36 62 L12 48" stroke="#F68D2E" stroke-width="15" stroke-linecap="round"/><path d="M18 50 l4 -6 M22 53 l4 -6" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/></g>
 <g class="sm-arm sm-arm-r"><path d="M64 62 L88 48" stroke="#F68D2E" stroke-width="15" stroke-linecap="round"/><path d="M82 50 l-4 -6 M78 53 l-4 -6" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/></g>
 <path d="M40 92 L28 128 M60 92 L72 128" stroke="#F68D2E" stroke-width="16" stroke-linecap="round"/>
 <path d="M24 120 q6 4 10 0 M66 120 q6 4 10 0" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
 <rect x="32" y="52" width="36" height="46" rx="16" fill="#F68D2E"/>
 <circle cx="50" cy="32" r="19" fill="#F68D2E"/>
 <circle cx="43" cy="29" r="2.6" fill="#24152b"/><circle cx="57" cy="29" r="2.6" fill="#24152b"/>
 <path d="M42 38 q8 6 16 0" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round"/>
 <path d="M34 49 q16 7 32 0" stroke="#fff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-dasharray="3 4"/>
 <circle cx="50" cy="62" r="3.2" fill="#E03C31"/><circle cx="50" cy="74" r="3.2" fill="#05A445"/><circle cx="50" cy="86" r="3.2" fill="#0085CA"/>
 <path d="M44 51 l6 4 l6 -4 l-1 8 l-5 -3 l-5 3 z" fill="#E03C31"/>
</g></svg>"""


def penguin(i):
    return f"""<svg class="sm sm{i}" viewBox="0 0 100 140" aria-hidden="true">
<ellipse cx="50" cy="136" rx="28" ry="4" fill="#9663A8" opacity=".35"/>
<g class="sm-body">
 <g class="sm-arm sm-arm-l"><path d="M28 64 q-18 8 -20 26 q12 -4 22 -14 z" fill="#24152b"/></g>
 <g class="sm-arm sm-arm-r"><path d="M72 64 q18 8 20 26 q-12 -4 -22 -14 z" fill="#24152b"/></g>
 <ellipse cx="50" cy="82" rx="26" ry="44" fill="#24152b"/>
 <ellipse cx="50" cy="92" rx="18" ry="32" fill="#fff"/>
 <circle cx="42" cy="46" r="7" fill="#fff"/><circle cx="58" cy="46" r="7" fill="#fff"/>
 <circle cx="43" cy="47" r="3" fill="#24152b"/><circle cx="57" cy="47" r="3" fill="#24152b"/>
 <path d="M44 55 L50 62 L56 55 Z" fill="#F68D2E"/>
 <path d="M34 124 q-6 8 6 8 l8 -4 z M66 124 q6 8 -6 8 l-8 -4 z" fill="#F68D2E"/>
 <path d="M30 60 q20 9 40 0 l1 7 q-21 9 -42 0 z" fill="#0085CA"/>
 <path d="M58 64 l7 16 l-7 2 l-4 -16 z" fill="#0085CA"/>
 <path d="M30 34 q20 -34 40 0 z" fill="#E03C31"/><rect x="28" y="31" width="44" height="7" rx="3.5" fill="#fff"/>
 <circle cx="50" cy="8" r="6" fill="#fff"/>
</g></svg>"""


# a festive line-up, like the dancing children on the homepage banner
CAST = [snowman(0, *LOOKS[0]), gingerbread(1), snowman(2, *LOOKS[1]), penguin(3), snowman(4, *LOOKS[2]), gingerbread(5), snowman(6, *LOOKS[3])]
row = '<div class="sm-row" aria-hidden="true">' + ''.join(CAST) + '</div>'
# the row sits on the snow at the very bottom of the banner (after the inner text block)
banner_inner_end = t.index('Just log in</a>.</p></div>') + len('Just log in</a>.</p></div>')
t = t[:banner_inner_end] + row + t[banner_inner_end:]

CSS = '''<style>
.home-banner{overflow:hidden}
.sm-row{position:absolute;z-index:25;left:50%;bottom:-6px;transform:translateX(-50%);display:flex;align-items:flex-end;gap:clamp(4px,2vw,34px);width:min(1200px,98%);justify-content:center;pointer-events:none}
.sm{width:clamp(58px,9.5vw,150px);height:auto;overflow:visible}
.sm1,.sm5{width:clamp(50px,8vw,128px)}
.sm3{width:clamp(54px,8.6vw,138px)}
.sm-body{transform-box:fill-box;transform-origin:50% 100%;animation:sm-dance 1.1s ease-in-out infinite alternate}
.sm-arm{transform-box:fill-box;animation:sm-wave .55s ease-in-out infinite alternate}
.sm-arm-l{transform-origin:100% 100%}.sm-arm-r{transform-origin:0% 100%;animation-delay:-.27s}
.sm1 .sm-body{animation-delay:-.3s}.sm2 .sm-body{animation-delay:-.6s;animation-duration:.95s}
.sm3 .sm-body{animation-delay:-.15s;animation-duration:.85s}.sm4 .sm-body{animation-delay:-.75s;animation-duration:1.25s}.sm5 .sm-body{animation-delay:-.45s}.sm6 .sm-body{animation-delay:-.9s;animation-duration:1.05s}
@keyframes sm-dance{0%{transform:translateY(0) rotate(-6deg)}50%{transform:translateY(-10%) rotate(0)}100%{transform:translateY(0) rotate(6deg)}}
@keyframes sm-wave{from{transform:rotate(-14deg)}to{transform:rotate(16deg)}}
@media (prefers-reduced-motion:reduce){.sm-body,.sm-arm{animation:none}}
@media (max-width:640px){.sm-row{gap:0}.sm0,.sm5,.sm6{display:none}}
</style>'''
t = suball('</head>', CSS + '</head>', t)

panel = review_panel([
    ('Dancing festive characters under the banner', 'A festive line-up dancing on the snow at the bottom of the banner, like the children on the homepage: four snowmen, two gingerbread people and a penguin, in brand colours. '
     'On phones four of them dance. They keep still for anyone whose device is set to reduce motion. '
     'The alternative is the smaller gap in v0.33 on the development view.', 'Option'),
], 'https://main.imoves-site.pages.dev/active-advent/')
panel = panel.replace('Compare with <a', 'Compare with v0.33 on <a').replace('>the live page</a>', '>the development view</a>')
t = suball('</body>', panel + '</body>', t)

for attr in ('src', 'href', 'srcset'):
    t = re.sub(rf'{attr}="\.\./(?!default/|video/cf-player)', f'{attr}="https://imoves.com/', t)
t = t.replace("url('../images/", "url('https://imoves.com/images/").replace('url(../images/', 'url(https://imoves.com/images/')

out = os.path.join(HERE, 'site', 'active-advent-snowmen', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(t)
print('wrote', os.path.relpath(out, ROOT))
