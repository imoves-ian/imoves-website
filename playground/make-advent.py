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


# ---------------------------------------------------------------- 8 to 11. calendar, how it works, what you get, brush headings
SIGNUP = 'https://platform.imoves.com/sign-up?nid=106'
LOGIN = 'https://platform.imoves.com/login'
DAYS = [('Mon', 30, 'Nov'), ('Tue', 1, 'Dec'), ('Wed', 2, 'Dec'), ('Thu', 3, 'Dec'), ('Fri', 4, 'Dec'),
        ('Mon', 7, 'Dec'), ('Tue', 8, 'Dec'), ('Wed', 9, 'Dec'), ('Thu', 10, 'Dec'), ('Fri', 11, 'Dec'),
        ('Mon', 14, 'Dec'), ('Tue', 15, 'Dec'), ('Wed', 16, 'Dec'), ('Thu', 17, 'Dec'), ('Fri', 18, 'Dec')]
# brand colour pairs (100% door, 25% tint for the opened inside)
COLS = [('#E03C31', '#F7CECC'), ('#702F8A', '#DBCBE2'), ('#0085CA', '#BFE1F2'), ('#05A445', '#B0D9B2')]
# a Christmas decoration on every door, chosen so it shows up on that door colour
DECO = {'#E03C31': 'wreath', '#702F8A': 'star', '#0085CA': 'snowflake', '#05A445': 'bauble'}
PEEK = {0: '9337dervz2', 7: 'z2rwkhuq6a', 14: 'pgd1i938wz'}   # door index -> video thumbnail
LONG = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday'}
MONTH = {'Nov': 'November', 'Dec': 'December'}

doors = []
for i, (d, n, m) in enumerate(DAYS):
    c, tint = COLS[(i + 2 * (i // 5)) % len(COLS)]
    when = f'{LONG[d]} {n} {MONTH[m]}'
    inside = (f'<picture><source srcset="../video/thumbs/{PEEK[i]}.webp" type="image/webp">'
              f'<img src="../video/thumbs/{PEEK[i]}.jpg" alt="" loading="lazy" width="1280" height="720"></picture>'
              if i in PEEK else '<span class="aa-star" aria-hidden="true">★</span>')
    doors.append(
        f'<li class="aa-door{" aa-peek" if i in PEEK else ""}" style="--c:{c};--t:{tint}">'
        f'<button type="button" aria-label="Door {i + 1}: opens {when}" aria-pressed="false">'
        f'<span class="aa-inside">{inside}<span class="aa-opens">Opens {d} {n} {m}</span></span>'
        f'<span class="aa-front"><span class="aa-snow" aria-hidden="true"></span>'
        f'<svg class="aa-deco" aria-hidden="true" viewBox="0 0 64 64"><use href="#aa-{DECO[c]}"/></svg>'
        f'<span class="aa-num">{i + 1}</span><span class="aa-date">{d} {n} {m}</span></span>'
        f'</button></li>')

calendar = f'''<section class="aa-sec aa-cal" data-suggest="8" aria-labelledby="aa-cal-h">
<div class="aa-wrap">
<h2 class="aa-title" id="aa-cal-h"><span>Your Christmas classroom countdown</span></h2>
<p class="aa-lead">15 doors, one for every school day from 30 November to 18 December. Behind each one is a new festive Active Blast for your class. Tap a door to peek.</p>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="aa-wreath" viewBox="0 0 64 64">
  <g transform="translate(32 30)"><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(0)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(30)" fill="#05A445"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(60)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(90)" fill="#05A445"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(120)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(150)" fill="#05A445"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(180)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(210)" fill="#05A445"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(240)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(270)" fill="#05A445"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(300)" fill="#5FBB72"/><ellipse cx="0" cy="-19" rx="6.5" ry="10" transform="rotate(330)" fill="#05A445"/><circle cx="0" cy="-19" r="2.6" transform="rotate(15)" fill="#E03C31" stroke="#fff" stroke-width="1"/><circle cx="0" cy="-19" r="2.6" transform="rotate(105)" fill="#E03C31" stroke="#fff" stroke-width="1"/><circle cx="0" cy="-19" r="2.6" transform="rotate(195)" fill="#E03C31" stroke="#fff" stroke-width="1"/><circle cx="0" cy="-19" r="2.6" transform="rotate(285)" fill="#E03C31" stroke="#fff" stroke-width="1"/></g>
  <path d="M32 46 l-11 -7 v14 z M32 46 l11 -7 v14 z" fill="#fff"/>
  <path d="M30 47 l-6 13 h5 l3 -6 l3 6 h5 l-6 -13 z" fill="#fff"/>
  <circle cx="32" cy="46" r="3.6" fill="#FDE3CB"/>
</symbol>
<symbol id="aa-star" viewBox="0 0 64 64">
  <path d="M32 5 l7.6 17.2 18.7 1.8 -14.1 12.4 4.1 18.4 -16.3 -9.6 -16.3 9.6 4.1 -18.4 -14.1 -12.4 18.7 -1.8 z" fill="#FBC697" stroke="#F68D2E" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="50" cy="10" r="2.5" fill="#fff"/><circle cx="12" cy="52" r="2" fill="#fff"/><circle cx="55" cy="47" r="1.6" fill="#fff"/>
</symbol>
<symbol id="aa-snowflake" viewBox="0 0 64 64">
  <g stroke="#fff" stroke-width="4" stroke-linecap="round" fill="none" transform="translate(32 32)"><g transform="rotate(0)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g><g transform="rotate(60)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g><g transform="rotate(120)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g><g transform="rotate(180)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g><g transform="rotate(240)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g><g transform="rotate(300)"><path d="M0 0 V-24"/><path d="M0 -14 l-7 -7 M0 -14 l7 -7"/></g></g>
  <circle cx="32" cy="32" r="4" fill="#BFE1F2"/>
</symbol>
<symbol id="aa-bauble" viewBox="0 0 64 64">
  <path d="M32 2 v8" stroke="#fff" stroke-width="2.5"/>
  <rect x="25" y="9" width="14" height="8" rx="2" fill="#FBC697" stroke="#F68D2E" stroke-width="2"/>
  <circle cx="32" cy="38" r="21" fill="#E03C31" stroke="#fff" stroke-width="2.5"/>
  <path d="M13 36 q19 9 38 0" stroke="#FDE3CB" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M20 30 a14 14 0 0 1 9 -9" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".85"/>
</symbol>
</defs></svg><ol class="aa-doors">{''.join(doors)}</ol>
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
  -webkit-mask:url(/assets/brush/swipe-2.svg) center/100% 100% no-repeat;mask:url(/assets/brush/swipe-2.svg) center/100% 100% no-repeat}
.aa-how .aa-title > span:first-child::before{--sw:#FDD4DD;background:#FDD4DD}
.aa-lead{text-align:center;max-width:760px;margin:0 auto 34px;font-size:1.15rem;color:#24152b}
/* calendar */
.aa-doors{list-style:none;margin:0;padding:18px;display:grid;grid-template-columns:repeat(5,1fr);gap:14px;background:#DBCBE2;border-radius:22px;box-shadow:inset 0 0 0 6px #B997C5}
.aa-door button{position:relative;display:block;width:100%;aspect-ratio:4/3;border:0;padding:0;background:var(--t);border-radius:14px;cursor:pointer;perspective:900px;font:inherit;box-shadow:0 4px 10px rgba(36,21,43,.18)}
.aa-front,.aa-inside{position:absolute;inset:0;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.aa-inside{overflow:hidden;background:var(--t)}
.aa-inside img{width:100%;height:100%;object-fit:cover}
.aa-star{font-size:2.2rem;color:var(--c)}
.aa-opens{position:absolute;left:0;right:0;bottom:0;background:rgba(36,21,43,.78);color:#fff;font-weight:600;font-size:.82rem;padding:3px 4px;text-align:center}
.aa-front{background:var(--c);color:#fff;transform-origin:left center;transition:transform .55s cubic-bezier(.3,.7,.3,1);box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}
.aa-front::after{content:"";position:absolute;right:10px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:#FBC697}
.aa-num{font-weight:700;font-size:clamp(1.4rem,2.8vw,2.2rem);line-height:1}
.aa-front{overflow:hidden;padding-top:8%}
.aa-snow{position:absolute;left:0;right:0;top:0;height:20%;background:#fff;
  -webkit-mask:radial-gradient(circle at 10% 0,#000 62%,transparent 64%) 0 0/20% 100% repeat-x,linear-gradient(#000,#000) 0 0/100% 45% no-repeat;
  mask:radial-gradient(circle at 10% 0,#000 62%,transparent 64%) 0 0/20% 100% repeat-x,linear-gradient(#000,#000) 0 0/100% 45% no-repeat}
.aa-deco{width:34%;height:auto;max-width:64px;margin-bottom:4px;filter:drop-shadow(0 2px 2px rgba(36,21,43,.25))}
.aa-date{font-weight:600;font-size:clamp(.7rem,1.3vw,.95rem);opacity:.95;margin-top:4px}
.aa-door.aa-peek .aa-front{transform:rotateY(-58deg)}
.aa-door button:hover .aa-front{transform:rotateY(-22deg)}
.aa-door.aa-peek button:hover .aa-front{transform:rotateY(-70deg)}
.aa-door button[aria-pressed="true"] .aa-front{transform:rotateY(-105deg)}
@media (prefers-reduced-motion:reduce){.aa-front{transition:none}}
@media (max-width:640px){.aa-doors{gap:8px;padding:10px;border-radius:16px}.aa-front,.aa-inside,.aa-door button{border-radius:10px}.aa-date{display:none}.aa-deco{width:44%;margin-bottom:2px}.aa-num{font-size:1.15rem}.aa-front::after{width:5px;height:5px;right:5px}.aa-opens{display:none}.aa-star{font-size:1.4rem}}
/* how it works */
.aa-steps{list-style:none;margin:10px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:28px;text-align:center}
.aa-steps h3{color:#702F8A;font-weight:700;font-size:1.4rem;margin:14px 0 6px}
.aa-steps p{margin:0;font-size:1.05rem}
.aa-steps a,.aa-have a,.aa-cards a{color:#702F8A;font-weight:700;text-decoration:underline}
.aa-circle{display:inline-grid;place-items:center;width:92px;height:92px;color:#fff;font-weight:700;font-size:2.6rem;position:relative;z-index:0}
.aa-circle::before{content:"";position:absolute;inset:0;z-index:-1;background:var(--c);-webkit-mask:url(/assets/brush/circle.svg) center/contain no-repeat;mask:url(/assets/brush/circle.svg) center/contain no-repeat}
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
    ('An advent calendar you can see', '15 doors, one per school day, with dates, snow along the top and a Christmas decoration on each (wreath, star, snowflake or bauble). Three are peeking open to show what is behind them; tap any door to open it.', 'New section'),
    ('How it works in three steps', 'Sign up, open a door, move for 3–5 minutes. Says clearly that anyone with an account or a past free trial just logs in (also under the banner button).', 'New section'),
    ('One "What you get" section', 'The two near-identical sections and the purple strip between them become one section: four cards and the two pictures. The page is about a third shorter.', 'Merged'),
    ('Headings on brush swipes', 'Section headings sit on the supplied Swipe brush in a soft brand tint, as the brand guidelines show; step numbers sit on the Circle brush.', 'Brand'),
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
