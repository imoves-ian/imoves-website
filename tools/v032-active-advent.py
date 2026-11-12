#!/usr/bin/env python3
"""v0.32: Active Advent page improvements and Active Advent on the homepage, as agreed with Ian on
12 November 2026 after reviewing suggested versions on the playground.

    python3 tools/v032-active-advent.py

Run once. It reads both pages as they were at v0.31 (commit 1b6ff7d) and writes active-advent/index.html
and index.html. The calendar doors come from tools/advent_doors.py.

Active Advent page (/active-advent):
  1  banner picture restored (its style rule pointed at the old banner ID) with a purple wash
  2  the normal site header in place of the logo-only one
  3  dates line in the banner
  4  wording: sentence case, Davies Sports, "prize:", 30 November, self-worth, one button wording
  5  the sentence introducing the videos moved above them
  6  Active Advent logo in the header in place of the monthly imoves logo: a brand exception
     confirmed by Ian, this page only
  7  the Google review as a card
  8  a 15-door advent calendar
  9  How it works in three steps; existing accounts and past free trials just log in
  10 the two "what you get" sections and the strip between them merged into one
  11 section headings on the Swipe brush, step numbers on the Circle brush
Homepage:
  2  an Active Advent section after the banner, with a small calendar and a countdown
  3  Active Advent at the top of the "What we offer" drop-down (homepage only) and the phone menu
  4  "Not ready for a demo? Try imoves free this Christmas with Active Advent" under the first demo bar
  The homepage Active Advent items hide themselves after Friday 18 December (UK time) and should be
  taken out of the page in January (issues log 18).
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from advent_doors import *  # noqa: F401,F403  DAYS, DEFS, DOOR_CSS, door_list, SIGNUP, LOGIN, ...

V031 = '1b6ff7d'


def at_v031(path):
    return subprocess.run(['git', '-C', ROOT, 'show', f'{V031}:{path}'], check=True, capture_output=True).stdout.decode('utf-8')


def suball(old, new, s, n=None):
    c = s.count(old)
    assert c and (n is None or c == n), f'{c} found: {old[:70]!r}'
    return s.replace(old, new)


# ==================================================================== the Active Advent page
t = at_v031('active-advent/index.html')
home = at_v031('index.html')

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
new_logo = ('<picture data-suggest="6" style="display:block"><source srcset="../images/300x0/0x0-0x0/logos/active-advent-logo.webp" type="image/webp">'
            '<img alt="Active Advent" src="../images/300x0/0x0-0x0/logos/active-advent-logo.png" width="289" height="112" '
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


# ---------------------------------------------------------------- 8 to 11. calendar, how it works, what you get, brush headings
doors = door_list('../video/thumbs')
calendar = f'''<section class="aa-sec aa-cal" data-suggest="8" aria-labelledby="aa-cal-h">
<div class="aa-wrap">
<h2 class="aa-title" id="aa-cal-h"><span>Your Christmas classroom countdown</span></h2>
<p class="aa-lead">15 doors, one for every school day from 30 November to 18 December. Behind each one is a new festive Active Blast for your class. Tap a door to peek.</p>
{DEFS}<ol class="aa-doors">{''.join(doors)}</ol>
</div></section>'''

steps = [
    ('Sign up for free', 'Create your free imoves account in a minute, using the button below.', '#702F8A'),
    ('Open a door each morning', 'From Monday 30 November, a new door unlocks every school day, right up to Friday 18 December.', '#E03C31'),
    ('Move for 3–5 minutes', 'Press play and follow along. No planning, no equipment, just Christmas fun.', '#0085CA'),
]
how = f'''<section class="aa-sec aa-how" data-suggest="9" aria-labelledby="aa-how-h">
<div class="aa-wrap">
<h2 class="aa-title" id="aa-how-h"><span>How it works</span></h2>
<ol class="aa-steps">{''.join(f'<li><span class="aa-circle" style="--c:{c}">{i}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p, c) in enumerate(steps, 1))}</ol>
<div class="aa-ctas"><a class="aa-btn" href="{SIGNUP}" target="_blank">Join Active Advent 2026 – it's free</a>
<p class="aa-have">Already have an imoves account, or had a free trial? <a href="{LOGIN}">Log in</a> – there's nothing else to do.</p></div>
</div></section>'''

cards = [
    ('15 festive Active Blasts', 'A new fun-filled activity every school day, with follow-along videos for primary classrooms.', '#E03C31', '#F7CECC'),
    ('Your own advent calendar', 'Build the excitement as your class opens a colourful new door each day, and revisit favourites whenever you like.', '#702F8A', '#DBCBE2'),
    ('Certificates and a poster', 'Download certificates for your Active Superstars and a poster for your classroom wall.', '#0085CA', '#BFE1F2'),
    ('Davies Sports prizes', 'Top user prizes every week from our sponsor <a href="https://www.daviessports.co.uk/imoves">Davies Sports</a>, including two disco lights with speakers.', '#05A445', '#B0D9B2'),
]
get = f'''<section class="aa-sec aa-get" data-suggest="10" aria-labelledby="aa-get-h">
<div class="aa-wrap">
<h2 class="aa-title" id="aa-get-h"><span>What you get</span></h2>
<p class="aa-lead">It's educational, mental-health boosting and gets your children active every day.</p>
<div class="aa-get-grid">
<div class="aa-pics">
<picture class="aa-pic1"><source srcset="../images/800x450/0x0-0x0/active-advent/copy-of-landing-page-images-active-advent-2.webp" type="image/webp"><img src="../images/800x450/0x0-0x0/active-advent/copy-of-landing-page-images-active-advent-2.jpg" alt="An Active Blast playing on a classroom screen, with snowmen and a Christmas tree" width="800" height="533" loading="lazy"></picture>
<picture class="aa-pic2"><source srcset="../images/800x450/0x0-0x0/active-advent/copy-of-landing-page-images-active-advent-1.webp" type="image/webp"><img src="../images/800x450/0x0-0x0/active-advent/copy-of-landing-page-images-active-advent-1.jpg" alt="The Active Advent calendar, certificate and Davies Sports disco light prize" width="800" height="533" loading="lazy"></picture>
</div>
<ul class="aa-cards">{''.join(f'<li style="--c:{c};--t:{tt}"><h3>{h}</h3><p>{p}</p></li>' for h, p, c, tt in cards)}</ul>
</div></div></section>'''

a0 = t.find('<div class="bg-white text-black pt-40 pb-20 md:py-50" data-block="image-and-usp">')
a1 = t.find('<div class="my-30 md:my-50 lg:my-75" data-block="videos-block">')
assert 0 < a0 < a1, 'usp blocks not found'
t = t[:a0] + calendar + how + get + t[a1:]

# 11. headings over a brush swipe (brand guideline: titles sit over brush shapes)
t = suball('<h3 class="text-3xl md:text-4xl font-semibold text-purple leading-snug px-20 mb-30"> A little taste of Christmas magic!</h3>',
           '<h2 class="aa-title" data-suggest="11"><span>A little taste of Christmas magic!</span></h2>', t)
t = suball('<h3 class="text-3xl md:text-4xl font-semibold text-purple leading-snug px-20 mb-20"> Happy teachers using imoves say...</h3>',
           '<h2 class="aa-title"><span>Happy teachers using imoves say…</span></h2>', t)

AA_CSS = '''<style>
.aa-sec{padding:64px 0}
.aa-wrap{max-width:1140px;margin:0 auto;padding:0 20px}
.aa-cal{background:#fff}
.aa-how{background:#F3ECF6}
.aa-get{background:#fff}
.aa-title{text-align:center;margin:0 0 14px;line-height:1.2}
.aa-title > span:first-child{position:relative;display:inline-block;padding:10px 34px;color:#702F8A;font-weight:700;font-size:clamp(1.7rem,3.6vw,2.6rem);z-index:0}
.aa-title > span:first-child::before{content:"";position:absolute;inset:-6px -4px;z-index:-1;background:var(--sw,#FDE3CB);
  -webkit-mask:url(../images/brush/swipe-2.svg) center/100% 100% no-repeat;mask:url(../images/brush/swipe-2.svg) center/100% 100% no-repeat}
.aa-how .aa-title > span:first-child::before{--sw:#FDD4DD;background:#FDD4DD}
.aa-lead{text-align:center;max-width:760px;margin:0 auto 34px;font-size:1.15rem;color:#24152b}
''' + DOOR_CSS + '''
/* how it works */
.aa-steps{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px;text-align:center}
.aa-steps h3{color:#702F8A;font-weight:700;font-size:1.4rem;margin:14px 0 6px}
.aa-steps p{margin:0;font-size:1.05rem}
.aa-steps a,.aa-have a,.aa-cards a{color:#702F8A;font-weight:700;text-decoration:underline}
.aa-circle{display:inline-grid;place-items:center;width:92px;height:92px;color:#fff;font-weight:700;font-size:2.6rem;position:relative;z-index:0}
.aa-circle::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--c);-webkit-mask:url(../images/brush/circle.svg) center/contain no-repeat;mask:url(../images/brush/circle.svg) center/contain no-repeat}
.aa-ctas{text-align:center;margin-top:36px}
.aa-btn{display:inline-block;background:#E03C31;color:#fff!important;font-weight:700;font-size:1.25rem;border-radius:999px;padding:12px 34px;text-decoration:none;transition:background .15s,transform .15s}
.aa-btn:hover{background:#c8352b;transform:translateY(-2px)}
.aa-have{margin:14px 0 0;font-size:1rem}
@media (max-width:760px){.aa-steps{grid-template-columns:1fr;gap:22px}}
/* what you get */
.aa-get-grid{display:grid;grid-template-columns:1fr 1.1fr;gap:40px;align-items:center}
.aa-pics{position:relative;padding-bottom:18%}
.aa-pics img{border-radius:16px;box-shadow:0 12px 30px rgba(36,21,43,.18)}
.aa-pic1{display:block;width:82%}
.aa-pic2{display:block;width:62%;position:absolute;right:0;bottom:0;transform:rotate(3deg)}
.aa-pic2 img{border:6px solid #fff}
.aa-cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:16px}
.aa-cards li{background:var(--t);border-radius:16px;padding:18px 18px 16px;border-top:6px solid var(--c)}
.aa-cards h3{margin:0 0 6px;font-weight:700;font-size:1.2rem;color:#24152b}
.aa-cards p{margin:0;font-size:1rem;line-height:1.5}
@media (max-width:880px){.aa-get-grid{grid-template-columns:1fr}.aa-pics{max-width:560px;margin:0 auto 10px;width:100%}}
@media (max-width:520px){.aa-cards{grid-template-columns:1fr}}
/* existing blocks that now use the brush titles */
[data-block="videos-block"] .aa-title,[data-block="images-block"] .aa-title{margin-bottom:10px}
</style>
<script>
document.addEventListener('click',function(e){var b=e.target.closest('.aa-door button');if(!b)return;
  b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');});
</script>'''
t = suball('</head>', AA_CSS + '</head>', t)

# banner: the existing-account line under the button
t = suball(" Join Active Advent 2026 – it's free </a></div></div></div>",
           " Join Active Advent 2026 – it's free </a></div>"
           f'<p data-suggest="9" class="px-30 text-white mt-20" style="font-size:1.05rem">Already have an imoves account, or had a free trial? '
           f'<a href="{LOGIN}" style="color:#fff;font-weight:700;text-decoration:underline">Just log in</a>.</p></div></div>', t)


t = re.sub(r' data-suggest="\d+"', '', t)
open(os.path.join(ROOT, 'active-advent', 'index.html'), 'w', encoding='utf-8').write(t)
print('wrote active-advent/index.html')

# ==================================================================== the homepage
t = home
ADVENT_PAGE = './active-advent'
STAR = ('<svg viewBox="0 0 64 64" width="22" height="22" aria-hidden="true" style="flex:none"><use href="#aa-star"/></svg>')

# ---------------------------------------------------------------- 2. Active Advent feature section after the banner
mini = ''.join(door_list('./video/thumbs'))
feature = f'''{DEFS}<section class="hp-advent" data-advent data-suggest="2" aria-labelledby="hp-advent-h">
<div class="hp-advent-in">
<div class="hp-advent-txt">
<picture><source srcset="./images/300x0/0x0-0x0/logos/active-advent-logo.webp" type="image/webp"><img class="hp-advent-logo" src="./images/300x0/0x0-0x0/logos/active-advent-logo.png" alt="Active Advent" width="289" height="112"></picture>
<h2 id="hp-advent-h">Free for every primary school this Christmas</h2>
<p>15 school days, 15 festive surprises. Every school day from Monday 30 November to Friday 18 December, a new door opens on a fun, follow-along Active Blast for your class. Just 3–5 minutes a day, with no planning and no equipment.</p>
<p class="hp-chip" data-countdown>Starts Monday 30 November</p>
<div class="hp-advent-btns"><a class="aa-btn" href="{SIGNUP}" target="_blank">Join Active Advent – it's free</a>
<a class="hp-more" href="{ADVENT_PAGE}">Find out more</a></div>
<p class="hp-have">Already have an imoves account, or had a free trial? <a href="{LOGIN}">Just log in</a>.</p>
</div>
<div class="hp-advent-cal"><ol class="aa-doors hp-mini">{mini}</ol></div>
</div></section>'''
fv = t.find('<div class="my-30 md:my-50 lg:my-75" data-block="text-and-video">')
assert fv > 0
t = t[:fv] + feature + t[fv:]

# ---------------------------------------------------------------- 3. Active Advent in the menu
# The desktop menu is already full (on the live site it fits on one line only from 1280px wide),
# so Active Advent goes at the top of the "What we offer" drop-down rather than as a new item.
first = '<div class="dropdown-inner p-10 rounded-xl shadow-xl bg-gray-100"><a class="block text-purple hover:underline px-3 text-sm font-bold mb-4" href="./active-school">Active School</a>'
assert t.count(first) == 1, 'What we offer drop-down not found'
t = t.replace(first, first.replace('<a class="block', f'<a data-advent data-suggest="3" class="hp-dd" href="{ADVENT_PAGE}">{STAR.replace("22", "18")}<span>Active Advent<em>Free this Christmas</em></span></a><a class="block', 1), 1)
t = t.replace('<span class="inner relative flex items-center"> What we offer<span', '<span class="inner relative flex items-center"> What we offer<span class="hp-dot" data-advent aria-hidden="true"></span><span', 1)
# the phone menu (slide-out)
pm = re.search(r'<li><a class="block hover:bg-darken-light tr-all px-20 py-10" href="\./pricing">', t)
assert pm, 'phone menu pricing link not found'
t = t[:pm.start()] + (f'<li data-advent><a class="block hover:bg-darken-light tr-all px-20 py-10 font-bold" style="color:#E03C31" href="{ADVENT_PAGE}">'
                      'Active Advent – free this Christmas</a></li>') + t[pm.start():]

# ---------------------------------------------------------------- 4. the free route next to "Book a Demo"
demo = (' Book a Demo </a></div></div><div class="my-30 md:my-50 lg:my-75" data-block="videos-block">')
t = suball(demo, ' Book a Demo </a>'
           f'<p class="hp-or" data-advent data-suggest="4">Not ready for a demo? <a href="{ADVENT_PAGE}">Try imoves free this Christmas with Active Advent</a>, '
           '15 festive Active Blasts for your class from 30 November.</p>'
           '</div></div><div class="my-30 md:my-50 lg:my-75" data-block="videos-block">', t, 1)

# ---------------------------------------------------------------- styles and the countdown
CSS = '''<style>
''' + DOOR_CSS + '''
.aa-btn{display:inline-block;background:#E03C31;color:#fff!important;font-weight:700;font-size:1.15rem;border-radius:999px;padding:11px 30px;text-decoration:none;transition:background .15s,transform .15s}
.aa-btn:hover{background:#c8352b;transform:translateY(-2px)}
/* 2 feature */
.hp-advent{background:#fff;padding:56px 20px}
.hp-advent-in{max-width:1160px;margin:0 auto;display:grid;grid-template-columns:1fr 1.05fr;gap:44px;align-items:center}
.hp-advent-logo{width:260px;height:auto;margin:0 0 10px}
.hp-advent h2{color:#702F8A;font-weight:700;font-size:clamp(1.6rem,3vw,2.3rem);line-height:1.2;margin:0 0 12px}
.hp-advent p{font-size:1.1rem;margin:0 0 14px}
.hp-chip{display:inline-block;background:#FDE3CB;color:#24152b;font-weight:700;border-radius:999px;padding:4px 16px}
.hp-advent-btns{display:flex;flex-wrap:wrap;align-items:center;gap:12px 22px;margin:6px 0 12px}
.hp-more,.hp-have a,.hp-or a{color:#702F8A;font-weight:700;text-decoration:underline}
.hp-have{font-size:1rem!important;margin:0!important}
.hp-mini{gap:8px;padding:10px}
.hp-mini .aa-date,.hp-mini .aa-opens{display:none}
.hp-mini .aa-num{font-size:clamp(1rem,1.8vw,1.4rem)}
.hp-mini .aa-badge{width:40%;margin:1px 0 3px}
.hp-mini .aa-front,.hp-mini .aa-inside,.hp-mini .aa-door button{border-radius:10px}
@media (max-width:900px){.hp-advent-in{grid-template-columns:1fr;gap:26px}.hp-advent-txt{text-align:center}.hp-advent-logo{margin:0 auto 10px}.hp-advent-btns{justify-content:center}}
/* 3 menu */
.hp-dd{display:flex!important;align-items:center;gap:8px;background:#F7CECC;color:#702F8A;border-radius:10px;padding:7px 10px;margin:0 0 8px;font-size:.875rem;font-weight:700;text-decoration:none;white-space:nowrap;line-height:1.2}
.hp-dd svg{display:block}
.hp-dd em{display:block;font-style:normal;font-weight:600;font-size:.75rem;color:#24152b}
.hp-dd:hover{background:#F09E98}
.hp-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#E03C31;box-shadow:0 0 0 2px #fff;margin:0 2px 0 6px}
/* 4 demo bar */
.hp-or{margin:22px auto 0;max-width:640px;font-size:1.05rem;background:#fff;color:#24152b;border-radius:14px;padding:12px 18px}
</style>'''
JS = '''<script>
/* Active Advent countdown and self-removal (UK dates). Doors: school days 30 Nov to 18 Dec 2026. */
(function(){
  var DOORS=['2026-11-30','2026-12-01','2026-12-02','2026-12-03','2026-12-04','2026-12-07','2026-12-08','2026-12-09','2026-12-10','2026-12-11','2026-12-14','2026-12-15','2026-12-16','2026-12-17','2026-12-18'];
  var today=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/London'}).format(new Date());   // YYYY-MM-DD
  var txt;
  if(today>DOORS[14]){document.querySelectorAll('[data-advent]').forEach(function(el){el.remove();});return;}
  if(today<DOORS[0]){
    var days=Math.round((Date.parse(DOORS[0])-Date.parse(today))/864e5);
    txt=days===1?'Starts tomorrow!':'Starts Monday 30 November – '+days+' days to go';
  } else {
    var i=DOORS.indexOf(today);
    if(i>=0) txt='Door '+(i+1)+' opens today!';
    else { var next=DOORS.findIndex(function(d){return d>today;}); txt='Door '+(next+1)+' opens on Monday'; }
  }
  document.querySelectorAll('[data-countdown]').forEach(function(el){el.textContent=txt;});
})();
document.addEventListener('click',function(e){var b=e.target.closest('.aa-door button');if(!b)return;
  b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');});
</script>'''
t = suball('</head>', CSS + '</head>', t, 1)
t = suball('</body>', JS + '</body>', t, 1)


t = re.sub(r' data-suggest="\d+"', '', t)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(t)
print('wrote index.html')
