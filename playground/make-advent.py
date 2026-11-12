#!/usr/bin/env python3
"""Build the suggested Active Advent page for the playground.

    python3 playground/make-advent.py

Takes the real page (active-advent/index.html, as on imoves.com) and applies the suggested changes,
each marked with data-suggest="N" so the review panel can jump to it. Writes
playground/site/active-advent/index.html. Images and video thumbnails load from imoves.com; the
site's CSS, fonts and scripts are copied into playground/site/default and playground/site/video so
they work on the playground's own address. Google Tag Manager is removed so reviewing the page does
not count as visits in the live analytics.

Nothing here changes the live page. If Ian approves any of the suggestions, they are made on main
as a normal numbered version.
"""
import os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'playground', 'site', 'active-advent')
SITE = os.path.join(ROOT, 'playground', 'site')

import subprocess
def from_main(path):
    """The page as it is on main (= live once main and production match), not this branch's old copy."""
    return subprocess.run(['git', '-C', ROOT, 'show', f'origin/main:{path}'], check=True,
                          capture_output=True).stdout.decode('utf-8')
t = from_main('active-advent/index.html')
home = from_main('index.html')


def sub1(old, new, s, count=1):
    n = s.count(old)
    assert n >= count, f'expected {count} of {old[:70]!r}, found {n}'
    return s.replace(old, new) if count == 'all' else s.replace(old, new, count)


def suball(old, new, s):
    assert old in s, f'not found: {old[:70]!r}'
    return s.replace(old, new)


# ---------------------------------------------------------------- 0. playground plumbing
# drop Google Tag Manager (head script and the noscript iframe)
t = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', t, flags=re.S)
t = re.sub(r'<script>\(function\(w,d,s,l,i\).*?</script>', '', t, flags=re.S)
t = re.sub(r'<noscript><iframe[^>]*googletagmanager[^>]*></iframe></noscript>', '', t)
assert 'googletagmanager' not in t, 'GTM still present'
t = suball('<head>', '<head><meta name="robots" content="noindex, nofollow">', t)

# ---------------------------------------------------------------- 1. banner picture restored
# The 5 November copy gave the banner a new ID (6aecc75b426d5) but kept the old style rule
# (6ae397095bc86), so the snowy-trees picture never shows and the dark grey fallback does.
t = suball('[data-home-banner="6ae397095bc86"] {',
           '[data-home-banner="6aecc75b426d5"] {', t)
t = suball("background-image: url('../images/1920x0/0x0-0x0/active-advent/aa-banner-with-ds-star-1920-x-1080-px-1-1.png')",
           "background-image: url('../images/1920x0/0x0-0x0/active-advent/aa-banner-with-ds-star-1920-x-1080-px-1-1.png');"
           "background-image: image-set(url('../images/1920x0/0x0-0x0/active-advent/aa-banner-with-ds-star-1920-x-1080-px-1-1.webp') type('image/webp'),"
           "url('../images/1920x0/0x0-0x0/active-advent/aa-banner-with-ds-star-1920-x-1080-px-1-1.png') type('image/png'));"
           "background-position:center 62%", t)
# 40% black wash -> brand purple wash, strongest behind the words, so the trees and stars show
t = suball('<div class="home-banner relative bg-cover bg-center bg-gray-800 py-40" data-block="home-banner" data-home-banner="6aecc75b426d5">'
           '<div class="absolute z-20 top-0 left-0 w-full h-full bg-black opacity-40"></div>',
           '<div class="home-banner relative bg-cover bg-center bg-purple py-40" data-block="home-banner" data-home-banner="6aecc75b426d5" data-suggest="1" style="padding-bottom:130px;text-shadow:0 2px 10px rgba(79,31,99,.45)">'
           '<div class="absolute z-20 top-0 left-0 w-full h-full" style="background:linear-gradient(180deg,rgba(112,47,138,.90) 0%,rgba(112,47,138,.66) 58%,rgba(112,47,138,0) 100%)"></div>', t)
t = suball('<h2 class="px-30 text-white opacity-80 text-xl md:text-2xl lg:text-3xl mt-20">',
           '<h2 class="px-30 text-white text-xl md:text-2xl lg:text-3xl mt-20">', t)

# ---------------------------------------------------------------- 2. the normal site header
# The page has the "simple" landing-page header: logo only. Swap in the header every other page
# has (menu, Login, Get FREE Access). The page already contains the slide-out phone menu it opens.
k = t.find('<div class="simple-header')
depth = 0
for m in re.finditer(r'<div\b|</div>', t[k:]):
    depth += 1 if m.group(0) == '<div' else -1
    if depth == 0:
        end = k + m.end(); break
hi, hj = home.find('<header'), home.find('</header>') + len('</header>')
header = home[hi:hj]
header = re.sub(r'(href|src)="\./', r'\1="../', header)
header = header.replace('<header class="main-header', '<header data-suggest="2" class="main-header', 1)
t = t[:k] + header + t[end:]
t = re.sub(r'(<body[^>]*class="[^"]*)\bsimple-header\b', r'\1', t)

# ---------------------------------------------------------------- 7. Active Advent logo in the header (this page only)
# A deliberate brand exception, confirmed by Ian on 12 November 2026: on this page the top-left
# header logo is the Active Advent campaign logo instead of the month's imoves logo.
old_logo = '<img alt="11 November White Logo" height="85" src="../images/300x0/0x0-0x0/logos/11-november-white-logo.png" style="width: 150px;" width="300"/>'
new_logo = ('<picture data-suggest="6" style="display:block"><source srcset="/assets/active-advent-logo.webp" type="image/webp">'
            '<img alt="Active Advent" src="/assets/active-advent-logo.png" width="289" height="112" '
            'style="display:block;height:58px;width:auto;margin:-8px 0"></picture>')
t = suball(old_logo, new_logo, t)

# ---------------------------------------------------------------- 3. hero: dates and one clear button
t = suball('Every school day, a new Christmas door unlocks, revealing a surprise Active Blast for your class.</h2>',
           'Every school day, a new Christmas door unlocks, revealing a surprise Active Blast for your class.</h2>'
           '<p data-suggest="3" class="px-30 text-white font-bold text-lg md:text-xl mt-20">'
           'Monday 30 November to Friday 18 December &middot; 3–5 minutes a day &middot; free to join</p>', t)

# ---------------------------------------------------------------- 4. wording: brand sentence case, typos, consistent buttons
W = [
    (' Active Advent 2026 – 15 Days of Christmas Movement Fun!</h1>', ' Active Advent 2026: 15 days of Christmas movement fun!</h1>'),
    (" Join Active Advent 2026 - It's FREE </a>", " Join Active Advent 2026 – it's free </a>"),
    ('join thousands of primary school teachers for a FREE Christmas movement countdown.', 'join thousands of primary school teachers for a free Christmas movement countdown.'),
    ('<strong>TOP USER prizes every week</strong>', '<strong>top user prizes every week</strong>'),
    ('>Davies Sport</a>!', '>Davies Sports</a>!'),
    ('<strong>Win a Davies Sports Prize!: </strong>', '<strong>Win a Davies Sports prize: </strong>'),
    ('<h2>Your Christmas Classroom Countdown Starts Here!</h2>', '<h2>Your Christmas classroom countdown starts here!</h2>'),
    (' A Little Taste of Christmas Magic!</h3>', ' A little taste of Christmas magic!</h3>'),
    ('confidence and self worth,', 'confidence and self-worth,'),
]
for old, new in W:
    t = suball(old, new, t)
t = t.replace(' Get FREE access to Active Advent!</h3>', ' Get free access to Active Advent!</h3>')
t = t.replace('starting from 30th November - plus certificates for the children AND a downloadable poster',
              'starting on 30 November – plus certificates for the children and a downloadable poster')
t = t.replace(' Get FREE Access to Active Advent </a>', ' Join Active Advent 2026 – it\'s free </a>')
# mark the first changed heading so the panel can jump to the wording changes
t = suball('<h1 class="px-30', '<h1 data-suggest="4" class="px-30', t)

# ---------------------------------------------------------------- 5. videos: introduce them first
intro = ('<div class="text-content mt-30 md:mt-50 lg:mt-75 text-center"><p>Here\'s a little taste of the fun waiting for your class! '
         'From festive dances to energising movement breaks, every activity is designed to get children moving and having fun together.</p></div>')
t = suball(intro, '', t)
t = suball(' A little taste of Christmas magic!</h3>',
           ' A little taste of Christmas magic!</h3><div data-suggest="5" class="text-content text-center text-lg px-20" style="max-width:820px;margin:0 auto 10px">'
           '<p>Here\'s a little taste of the fun waiting for your class! From festive dances to energising movement breaks, '
           'every activity is designed to get children moving and having fun together.</p></div>', t)

# ---------------------------------------------------------------- 6. reviews: the Google review as a card, like the others
gq = t.find('"Great fun activities for kids of all ages')
blk_start = t.rfind('<div class="row px-20 md:px-30 my-30 md:my-50 lg:my-75" data-block="main-content">', 0, gq)
blk_end = t.find('(Google Review, Miss Peasnall)</p></div></div>', gq) + len('(Google Review, Miss Peasnall)</p></div></div>')
card = ('<div data-suggest="7" class="row px-20" style="margin:10px auto 60px;max-width:820px">'
        '<div style="background:#fff;border-radius:16px;padding:28px 30px;text-align:center;box-shadow:0 8px 24px rgba(112,47,138,.12)">'
        '<div style="color:#F68D2E;font-size:28px;letter-spacing:4px;line-height:1">★★★★★</div>'
        '<p class="text-xl md:text-2xl font-semibold text-purple leading-snug" style="margin:14px 0 10px">'
        '“Great fun activities for kids of all ages to do and learn. My class particularly enjoy learning a new dance and '
        'pretending they’re riding a mountain bike. Definitely recommended.”</p>'
        '<p style="margin:0;color:#3a2a40">Miss Peasnall, Google review</p></div></div>')
t = t[:blk_start] + card + t[blk_end:]

# ---------------------------------------------------------------- all addresses that point at the live site
for attr in ('src', 'href', 'srcset'):
    t = re.sub(rf'{attr}="\.\./(?!default/|video/cf-player)', f'{attr}="https://imoves.com/', t)
t = t.replace("url('../images/", "url('https://imoves.com/images/").replace('url(../images/', 'url(https://imoves.com/images/')
t = t.replace('srcset="../video/thumbs/', 'srcset="https://imoves.com/video/thumbs/')

# ---------------------------------------------------------------- review panel (playground only)
SUGGESTIONS = [
    ('Banner picture back', 'The snowy-trees picture has been missing since the 5 November update: the banner was given a new ID but its picture rule still pointed at the old one, so visitors see plain dark grey. Fixed, with a purple wash in place of the 40% black one so the trees and stars show.', 'Fault on the live page'),
    ('Normal header with menu', 'The page has a logo-only header, so there is no menu, Login or Get FREE Access. This uses the same header as every other page.', 'Design choice'),
    ('Dates in the banner', 'The dates, how long it takes and that it is free, straight away, before anyone scrolls.', 'New line'),
    ('Wording tidy', 'Sentence case, per the brand rules (no all-capitals FREE, TOP USER, AND); "Davies Sport" link corrected to Davies Sports; "Prize!:" to "prize:"; "30th November" to 30 November; self-worth; every button now says the same thing.', 'Wording'),
    ('Introduce the videos first', 'The sentence introducing the three videos sat underneath them. It now comes first.', 'Order'),
    ('Active Advent logo in the header', 'The Active Advent logo (Santa and reindeer) replaces the imoves November logo top-left, on this page only. A brand exception you confirmed; every other page keeps the monthly imoves logo.', 'Brand exception'),
    ('Google review as a card', 'The Google review was a large block of purple text. It now sits in a card with stars, to match the other reviews.', 'Design'),
]
items = ''.join(
    f'<li><button type="button" data-go="{i}"><span class="n">{i}</span><span><strong>{h}</strong>'
    f'<small>{tag}</small><em>{d}</em></span></button></li>'
    for i, (h, d, tag) in enumerate(SUGGESTIONS, 1))
panel = f'''
<style>
[data-suggest]:not(header){{position:relative}}
[data-suggest].sg-hi{{outline:4px solid #F68D2E;outline-offset:4px;border-radius:6px}}
.sg-pin{{position:absolute;z-index:60;top:8px;left:8px;width:30px;height:30px;border-radius:50%;background:#F68D2E;color:#24152b;font:700 15px/30px Baloo,sans-serif;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,.25);pointer-events:none}}
header .sg-pin{{top:auto;bottom:-14px;left:180px}}
#sg{{position:fixed;z-index:9999;right:16px;bottom:16px;width:360px;max-width:calc(100vw - 32px);max-height:min(520px,calc(100vh - 140px));display:flex;flex-direction:column;background:#fff;border-radius:16px;box-shadow:0 12px 40px rgba(36,21,43,.28);font-family:Baloo,sans-serif;color:#24152b;overflow:hidden}}
#sg header,#sg .sg-head{{background:#702F8A;color:#fff;padding:12px 16px;display:flex;align-items:center;gap:10px}}
#sg .sg-head strong{{font-size:17px;flex:1}}
#sg .sg-head button{{background:#fff;color:#702F8A;border:0;border-radius:999px;font:600 13px Baloo,sans-serif;padding:4px 12px;cursor:pointer}}
#sg ol{{list-style:none;margin:0;padding:8px;overflow:auto}}
#sg li button{{display:flex;gap:10px;width:100%;text-align:left;background:none;border:0;border-radius:12px;padding:10px;cursor:pointer;font:inherit;color:inherit}}
#sg li button:hover,#sg li button:focus-visible{{background:#DBCBE2}}
#sg .n{{flex:none;width:26px;height:26px;border-radius:50%;background:#F68D2E;font-weight:700;text-align:center;line-height:26px}}
#sg strong{{display:block;font-size:15px;line-height:1.3}}
#sg small{{display:inline-block;font-size:11px;font-weight:600;color:#702F8A;background:#DBCBE2;border-radius:999px;padding:0 8px;margin:3px 0}}
#sg em{{display:block;font-style:normal;font-size:13px;line-height:1.45;color:#3a2a40}}
#sg .sg-foot{{padding:10px 16px 14px;font-size:13px;border-top:1px solid #DBCBE2}}
#sg .sg-foot a{{color:#702F8A;font-weight:600}}
#sg.min ol,#sg.min .sg-foot{{display:none}}
</style>
<aside id="sg" aria-label="Suggested changes">
  <div class="sg-head"><strong>Suggested changes ({len(SUGGESTIONS)})</strong><button type="button" id="sg-min">Hide</button></div>
  <ol>{items}</ol>
  <div class="sg-foot">Click a change to jump to it. Compare with <a href="https://imoves.com/active-advent/" target="_blank" rel="noopener">the live page</a>. This review panel is for the playground only.</div>
</aside>
<script>
(function(){{
  var els={{}};document.querySelectorAll('[data-suggest]').forEach(function(el){{var n=el.dataset.suggest;els[n]=el;var p=document.createElement('span');p.className='sg-pin';p.textContent=n;el.appendChild(p);}});
  document.querySelectorAll('#sg [data-go]').forEach(function(b){{b.addEventListener('click',function(){{
    var el=els[b.dataset.go];if(!el)return;
    var y=el.getBoundingClientRect().top+scrollY-120;scrollTo({{top:Math.max(0,y),behavior:'smooth'}});
    el.classList.add('sg-hi');setTimeout(function(){{el.classList.remove('sg-hi');}},2200);
  }});}});
  var sg=document.getElementById('sg'),m=document.getElementById('sg-min');
  m.addEventListener('click',function(){{var x=sg.classList.toggle('min');m.textContent=x?'Show':'Hide';}});
  if(innerWidth<700){{sg.classList.add('min');m.textContent='Show';}}
}})();
</script>
'''
t = suball('</body>', panel + '</body>', t)

os.makedirs(OUT_DIR, exist_ok=True)
open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8').write(t)

# site CSS, fonts and scripts so the page renders the same as on imoves.com
files = subprocess.run(['git', '-C', ROOT, 'ls-tree', '-r', '--name-only', 'origin/main', '--', 'default',
                        'video/cf-player.js', 'video/cf-player.css'], check=True, capture_output=True).stdout.decode().split()
for p in files:
    dest = os.path.join(SITE, p); os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'wb').write(subprocess.run(['git', '-C', ROOT, 'show', f'origin/main:{p}'], check=True, capture_output=True).stdout)
print('wrote', os.path.relpath(os.path.join(OUT_DIR, 'index.html'), ROOT))
