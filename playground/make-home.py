#!/usr/bin/env python3
"""Build the suggested homepage for the playground: the live homepage with Active Advent promoted.

    python3 playground/make-home.py

Takes index.html as it is on main, adds the suggestions (each marked data-suggest="N" for the review
panel) and writes playground/site/homepage/index.html. Images load from imoves.com; the site's CSS,
fonts and scripts come from the playground's own copy (made by make-advent.py). Google Tag Manager
is removed. Nothing here changes imoves.com.

Everything Active Advent on the page carries data-advent and hides itself once Friday 18 December
is over (UK time), so nobody has to remember to take it down on the day; it should still be removed
from the page files in January.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from advent_doors import DEFS, DOOR_CSS, door_list, review_panel, SIGNUP, LOGIN  # noqa: E402

t = subprocess.run(['git', '-C', ROOT, 'show', 'origin/main:index.html'], check=True, capture_output=True).stdout.decode('utf-8')


def suball(old, new, s, n=None):
    c = s.count(old)
    assert c and (n is None or c == n), f'{c} found: {old[:70]!r}'
    return s.replace(old, new)


# ---------------------------------------------------------------- playground plumbing
t = re.sub(r'<!-- Google Tag Manager -->.*?<!-- End Google Tag Manager -->', '', t, flags=re.S)
t = re.sub(r'<script>\(function\(w,d,s,l,i\).*?</script>', '', t, flags=re.S)
t = re.sub(r'<noscript><iframe[^>]*googletagmanager[^>]*></iframe></noscript>', '', t)
assert 'googletagmanager' not in t
t = suball('<head>', '<head><meta name="robots" content="noindex, nofollow">', t)

ADVENT_PAGE = 'https://imoves-playground.pages.dev/active-advent/'   # the suggested page, for review
STAR = ('<svg viewBox="0 0 64 64" width="22" height="22" aria-hidden="true" style="flex:none"><use href="#aa-star"/></svg>')

# ---------------------------------------------------------------- 1. Active Advent strip under the header
strip = f'''<div class="hp-strip" data-advent data-suggest="1">
<div class="hp-strip-in">{STAR}
<p><strong>Active Advent 2026</strong> – 15 days of free Christmas movement for your class. <span class="hp-count" data-countdown>Starts Monday 30 November</span></p>
<a class="hp-strip-link" href="{ADVENT_PAGE}">Find out more</a>
<a class="hp-strip-btn" href="{SIGNUP}" target="_blank">Join free</a>
</div></div>'''
hj = t.find('</header>') + len('</header>')
t = t[:hj] + strip + t[hj:]

# ---------------------------------------------------------------- 2. Active Advent feature section after the banner
mini = ''.join(door_list())
feature = f'''{DEFS}<section class="hp-advent" data-advent data-suggest="2" aria-labelledby="hp-advent-h">
<div class="hp-advent-in">
<div class="hp-advent-txt">
<picture><source srcset="/assets/active-advent-logo.webp" type="image/webp"><img class="hp-advent-logo" src="/assets/active-advent-logo.png" alt="Active Advent" width="289" height="112"></picture>
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
/* 1 strip */
.hp-strip{background:#F7CECC;color:#24152b;border-bottom:3px solid #E03C31;padding-top:calc(2.33vw - 2px)}
.hp-strip-in{max-width:1240px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;justify-content:center}
.hp-strip p{margin:0;font-size:1.02rem;line-height:1.35}
.hp-strip strong{color:#702F8A}
.hp-count{display:inline-block;font-weight:600;color:#702F8A;background:#fff;border-radius:999px;padding:0 10px;margin-left:4px}
.hp-strip-link{color:#702F8A;font-weight:700;text-decoration:underline}
.hp-strip-btn{background:#E03C31;color:#fff!important;font-weight:700;border-radius:999px;padding:5px 18px;text-decoration:none}
.hp-strip-btn:hover{background:#c8352b}
@media (max-width:1100px){.hp-strip-in{gap:8px 14px;padding:9px 14px}.hp-strip p{text-align:center;flex-basis:100%}.hp-strip-in > svg{display:none}}
@media (max-width:640px){.hp-strip p{font-size:.95rem}}
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

SUGGESTIONS = [
    ('Active Advent strip under the header', 'A slim festive strip on every visit: what it is, a live countdown ("18 days to go", then "Door 3 opens today!"), Find out more and Join free.', 'New'),
    ('Active Advent section after the banner', 'The Active Advent logo, a short pitch, the countdown, Join free and Find out more, and a small version of the 15-door calendar from the Active Advent page. Says that existing users and past free trials just log in.', 'New section'),
    ('Active Advent in the menu', 'At the top of the "What we offer" drop-down, with a red dot on "What we offer" to draw the eye, and at the top of the phone menu. The menu itself is full (on the live site it only fits on one line from 1280px wide), so there is no room for a new item. The menu is on every page, so on the live site this would be a site-wide change.', 'Menu'),
    ('A free route next to "Book a Demo"', 'Under the first "See how imoves could work in your school" bar: "Not ready for a demo? Try imoves free this Christmas with Active Advent". Turns the campaign into a way in for schools not ready to talk to sales.', 'New line'),
]
panel = review_panel(SUGGESTIONS, 'https://imoves.com/')
panel = panel.replace('This review panel is for the playground only.', 'This review panel is for the playground only. Everything Active Advent here hides itself automatically after Friday 18 December.', 1)
assert 'hides itself' in panel
t = suball('</body>', panel + '</body>', t, 1)

# ---------------------------------------------------------------- addresses
t = re.sub(r'(href|src|srcset)="\./(?=default/|video/cf-player)', r'\1="../', t)
t = re.sub(r'(href|src|srcset)="\./', r'\1="https://imoves.com/', t)
t = re.sub(r'(href|src|srcset)="\.\./(?!default/|video/cf-player)', r'\1="https://imoves.com/', t)
t = t.replace("url('./", "url('https://imoves.com/").replace('url(./', 'url(https://imoves.com/')
t = re.sub(r'href="https://imoves\.com/"(?=[^>]*class="block hover:opacity-70)', 'href="https://imoves.com/"', t)

out = os.path.join(HERE, 'site', 'homepage', 'index.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(t)
print('wrote', os.path.relpath(out, ROOT))
