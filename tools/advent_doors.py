"""Active Advent calendar pieces, shared by the Active Advent page and the homepage (v0.32): the 15 doors,
their Christmas decorations (simple flat drawings in brand colours) and snow, and the door styles.
Used by tools/v032-active-advent.py. The same code drew the suggested pages on the playground."""
SIGNUP = 'https://platform.imoves.com/sign-up?nid=106'
LOGIN = 'https://platform.imoves.com/login'
DAYS = [('Mon', 30, 'Nov'), ('Tue', 1, 'Dec'), ('Wed', 2, 'Dec'), ('Thu', 3, 'Dec'), ('Fri', 4, 'Dec'),
        ('Mon', 7, 'Dec'), ('Tue', 8, 'Dec'), ('Wed', 9, 'Dec'), ('Thu', 10, 'Dec'), ('Fri', 11, 'Dec'),
        ('Mon', 14, 'Dec'), ('Tue', 15, 'Dec'), ('Wed', 16, 'Dec'), ('Thu', 17, 'Dec'), ('Fri', 18, 'Dec')]
# brand colour pairs (100% door, 25% tint for the opened inside)
COLS = [('#E03C31', '#F7CECC'), ('#702F8A', '#DBCBE2'), ('#0085CA', '#BFE1F2'), ('#05A445', '#B0D9B2')]
# a Christmas decoration on every door, chosen so it shows up on that door colour
DECOS = ['wreath', 'stocking', 'star', 'present', 'holly', 'bauble']
PEEK = {0: '9337dervz2', 7: 'z2rwkhuq6a', 14: 'pgd1i938wz'}   # door index -> video thumbnail
LONG = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday'}
MONTH = {'Nov': 'November', 'Dec': 'December'}


import random as _r
def _snow(seed):
    """A lumpy snow drift for the top of a door, with the odd icicle drip."""
    rnd = _r.Random(seed); x = 0.0; pts = []
    while x < 200:
        w = min(rnd.uniform(14, 24), 200 - x); drip = rnd.random() < 0.18 and 12 < x < 180
        pts.append((x, x + w, rnd.uniform(14, 22), drip, rnd.uniform(25, 30)))
        x += w
    d = f'M0 0 H200 V{pts[-1][2]:.1f}'
    for x0, x1, depth, drip, dl in reversed(pts):
        mid = (x0 + x1) / 2
        if drip:
            d += (f' Q{x1:.1f} {depth + 6:.1f} {mid + 3:.1f} {depth + 2:.1f} L{mid + 3:.1f} {dl - 4:.1f}'
                  f' Q{mid:.1f} {dl + 3:.1f} {mid - 3:.1f} {dl - 4:.1f} L{mid - 3:.1f} {depth + 2:.1f} Q{x0:.1f} {depth + 6:.1f} {x0:.1f} {depth - 3:.1f}')
        else:
            d += f' Q{mid:.1f} {depth + 9:.1f} {x0:.1f} {depth - 3:.1f}'
    return d + ' Z'
_snows = ''.join(
    f'<symbol id="aa-snow{k}" viewBox="0 0 200 40" preserveAspectRatio="none">'
    f'<path d="{_snow(k + 3)}" fill="#BFE1F2" transform="translate(0 3)"/><path d="{_snow(k + 3)}" fill="#fff"/>'
    + ''.join(f'<circle cx="{_r.Random(k * 7 + j).uniform(8, 192):.0f}" cy="{_r.Random(k * 11 + j).uniform(4, 11):.0f}" r="1.4" fill="#BFE1F2"/>' for j in range(5))
    + '</symbol>' for k in range(3))
_wreath = ''.join(f'<ellipse cx="0" cy="-17" rx="7" ry="10.5" transform="rotate({a})" fill="{"#05A445" if k % 2 else "#5FBB72"}"/>'
                  for k, a in enumerate(range(0, 360, 30))) + ''.join(
                  f'<circle cx="0" cy="-17" r="3" transform="rotate({a})" fill="#E03C31"/>' for a in (20, 110, 200, 290))
DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>' + _snows +
 '<symbol id="aa-wreath" viewBox="0 0 64 64"><g transform="translate(32 30)">' + _wreath + '</g>'
 '<path d="M32 46 l-12 -7 v14 z M32 46 l12 -7 v14 z" fill="#E03C31"/><path d="M30 47 l-6 13 h5 l3 -6 l3 6 h5 l-6 -13 z" fill="#E03C31"/>'
 '<circle cx="32" cy="46" r="3.8" fill="#F09E98"/></symbol>'
 '<symbol id="aa-stocking" viewBox="0 0 64 64"><path d="M26 4 q-5 0 -5 5" stroke="#702F8A" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
 '<path d="M22 18 h20 v20 q0 4 4 6 l6 3 q7 4 3 11 q-4 6 -11 2 l-18 -10 q-4 -2 -4 -7 z" fill="#E03C31"/>'
 '<path d="M42 50 q8 2 11 0 q2 5 -2 8 q-4 2 -9 -1 z" fill="#05A445"/><path d="M22 30 h8 v8 q-4 1 -8 -2 z" fill="#05A445"/>'
 '<rect x="19" y="8" width="26" height="11" rx="5.5" fill="#fff" stroke="#B997C5" stroke-width="2"/></symbol>'
 '<symbol id="aa-star" viewBox="0 0 64 64"><path d="M32 4 l8 18 19.5 2 -14.7 13 4.3 19.2 -17.1 -10 -17.1 10 4.3 -19.2 -14.7 -13 19.5 -2 z" fill="#F68D2E" stroke="#E03C31" stroke-width="2" stroke-linejoin="round"/>'
 '<path d="M32 14 l4.6 10.2 11 1.2" stroke="#FBC697" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></symbol>'
 '<symbol id="aa-present" viewBox="0 0 64 64"><rect x="10" y="26" width="44" height="32" rx="3" fill="#702F8A"/><rect x="7" y="19" width="50" height="10" rx="3" fill="#9663A8"/>'
 '<rect x="28" y="19" width="8" height="39" fill="#F65275"/><path d="M32 19 q-14 -14 -18 -5 q-2 6 18 5 z M32 19 q14 -14 18 -5 q2 6 -18 5 z" fill="#F65275"/>'
 '<circle cx="32" cy="18" r="3.5" fill="#FC7E96"/></symbol>'
 '<symbol id="aa-holly" viewBox="0 0 64 64"><path d="M30 34 L6 18 l5 8 -7 4 8 2 -3 7 8 -2 0 8 6 -5 3 7 z" fill="#05A445" stroke="#05A445" stroke-width="2" stroke-linejoin="round"/>'
 '<path d="M34 34 L58 18 l-5 8 7 4 -8 2 3 7 -8 -2 0 8 -6 -5 -3 7 z" fill="#5FBB72" stroke="#5FBB72" stroke-width="2" stroke-linejoin="round"/>'
 '<circle cx="27" cy="38" r="6" fill="#E03C31"/><circle cx="38" cy="38" r="6" fill="#E03C31"/><circle cx="32.5" cy="29" r="6" fill="#E03C31"/>'
 '<circle cx="25" cy="36" r="1.6" fill="#fff"/><circle cx="36" cy="36" r="1.6" fill="#fff"/><circle cx="30.5" cy="27" r="1.6" fill="#fff"/></symbol>'
 '<symbol id="aa-bauble" viewBox="0 0 64 64"><path d="M32 2 v8" stroke="#702F8A" stroke-width="2.5"/><rect x="25" y="9" width="14" height="8" rx="2" fill="#F68D2E"/>'
 '<circle cx="32" cy="38" r="21" fill="#E03C31"/><path d="M13 36 q19 9 38 0" stroke="#FBC697" stroke-width="4.5" fill="none" stroke-linecap="round"/>'
 '<path d="M20 30 a14 14 0 0 1 9 -9" stroke="#fff" stroke-width="3.5" fill="none" stroke-linecap="round" opacity=".9"/></symbol>'
 '</defs></svg>')

def door_list(thumbs='../video/thumbs'):
    """The 15 doors as <li> items. thumbs is the address of video/thumbs relative to the page."""
    doors = []
    for i, (d, n, m) in enumerate(DAYS):
        c, tint = COLS[(i + 2 * (i // 5)) % len(COLS)]
        when = f'{LONG[d]} {n} {MONTH[m]}'
        inside = (f'<picture><source srcset="{thumbs}/{PEEK[i]}.webp" type="image/webp">'
                  f'<img src="{thumbs}/{PEEK[i]}.jpg" alt="" loading="lazy" width="1280" height="720"></picture>'
                  if i in PEEK else '<span class="aa-star" aria-hidden="true">★</span>')
        doors.append(
            f'<li class="aa-door{" aa-peek" if i in PEEK else ""}" style="--c:{c};--t:{tint}">'
            f'<button type="button" aria-label="Door {i + 1}: opens {when}" aria-pressed="false">'
            f'<span class="aa-inside">{inside}<span class="aa-opens">Opens {d} {n} {m}</span></span>'
            f'<span class="aa-front"><svg class="aa-snow" aria-hidden="true" viewBox="0 0 200 40" preserveAspectRatio="none"><use href="#aa-snow{i % 3}"/></svg>'
            f'<span class="aa-badge" aria-hidden="true"><svg class="aa-deco" viewBox="0 0 64 64"><use href="#aa-{DECOS[(i + 2 * (i // 5)) % len(DECOS)]}"/></svg></span>'
            f'<span class="aa-num">{i + 1}</span><span class="aa-date">{d} {n} {m}</span></span>'
            f'</button></li>')
    return doors


DOOR_CSS = '''/* calendar */
.aa-doors{list-style:none;margin:0;padding:18px;display:grid;grid-template-columns:repeat(5,1fr);gap:14px;background:#DBCBE2;border-radius:22px;box-shadow:inset 0 0 0 6px #B997C5}
.aa-door button{position:relative;display:block;width:100%;aspect-ratio:5/4;border:0;padding:0;background:var(--t);border-radius:14px;cursor:pointer;perspective:900px;font:inherit;box-shadow:0 4px 10px rgba(36,21,43,.18)}
.aa-front,.aa-inside{position:absolute;inset:0;border-radius:14px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.aa-inside{overflow:hidden;background:var(--t)}
.aa-inside img{width:100%;height:100%;object-fit:cover}
.aa-star{font-size:2.2rem;color:var(--c)}
.aa-opens{position:absolute;left:0;right:0;bottom:0;background:rgba(36,21,43,.78);color:#fff;font-weight:600;font-size:.82rem;padding:3px 4px;text-align:center}
.aa-front{background:var(--c);color:#fff;transform-origin:left center;transition:transform .55s cubic-bezier(.3,.7,.3,1);box-shadow:inset 0 0 0 3px rgba(255,255,255,.35)}
.aa-front::after{content:"";position:absolute;right:10px;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:#FBC697}
.aa-num{font-weight:700;font-size:clamp(1.2rem,2.3vw,1.9rem);line-height:1}
.aa-front{overflow:hidden;padding-top:11%;justify-content:flex-start}
.aa-snow{position:absolute;left:-1px;top:0;width:calc(100% + 2px);height:24%;z-index:2;filter:drop-shadow(0 1px 1px rgba(36,21,43,.15))}
.aa-badge{display:grid;place-items:center;width:33%;aspect-ratio:1;max-width:68px;border-radius:50%;background:#fff;box-shadow:0 0 0 4px rgba(255,255,255,.35),0 4px 10px rgba(36,21,43,.3);margin:4px 0 5px}
.aa-deco{width:76%;height:76%}
.aa-date{font-weight:600;font-size:clamp(.7rem,1.3vw,.95rem);opacity:.95;margin-top:4px}
.aa-door.aa-peek .aa-front{transform:rotateY(-58deg)}
.aa-door button:hover .aa-front{transform:rotateY(-22deg)}
.aa-door.aa-peek button:hover .aa-front{transform:rotateY(-70deg)}
.aa-door button[aria-pressed="true"] .aa-front{transform:rotateY(-105deg)}
@media (prefers-reduced-motion:reduce){.aa-front{transition:none}}
@media (max-width:640px){.aa-doors{gap:8px;padding:10px;border-radius:16px}.aa-front,.aa-inside,.aa-door button{border-radius:10px}.aa-date{display:none}.aa-badge{width:46%;margin:1px 0;box-shadow:0 2px 5px rgba(36,21,43,.3)}.aa-num{font-size:1rem}.aa-front::after{width:5px;height:5px;right:5px}.aa-opens{display:none}.aa-star{font-size:1.4rem}}
'''

