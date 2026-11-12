// Password gate for the imoves playground (Cloudflare Pages Function, runs before every request).
//
// Visitors without a valid sign-in see an imoves sign-in page and type the password into a normal
// form, which works in every browser (the Claude desktop app's built-in browser does not show the
// pop-up box that HTTP Basic sign-in uses). A correct password sets a cookie for 30 days.
// HTTP Basic sign-in (username "imoves") is still accepted, for scripts and older bookmarks.
//
// Only a salted SHA-256 hash of the password is stored here, because this repository is public.
// To change the password, run
//   python3 playground/set-password.py "new-password"
// which rewrites SALT and HASH below, then push the playground branch. Changing the password also
// signs everyone out, because the cookie is derived from the hash.
//
// If the Pages project has an environment variable PLAYGROUND_PASSWORD, that is accepted instead.

const USER = 'imoves';
const SALT = 'bc161a36039730007c9a4c4a8b159f3f';
const HASH = '554004400cc6800a3620ab33c2f99ba556e8ac84dde16d40dd464f187ec22199';
const COOKIE = 'imoves_playground';
const MAX_AGE = 60 * 60 * 24 * 30;
const LOGIN_PATH = '/__signin';
const PUBLIC_PREFIX = '/login/';          // logo and fonts for the sign-in page itself

async function sha256hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function same(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

async function passwordOk(pass, env) {
  if (typeof pass !== 'string' || !pass) return false;
  if (env && env.PLAYGROUND_PASSWORD && same(pass, env.PLAYGROUND_PASSWORD)) return true;
  return same(await sha256hex(SALT + pass), HASH);
}

async function cookieValue(env) {
  return sha256hex('cookie|' + SALT + '|' + HASH + '|' + ((env && env.PLAYGROUND_PASSWORD) || ''));
}

function readCookie(request, name) {
  const all = request.headers.get('Cookie') || '';
  for (const part of all.split(';')) {
    const i = part.indexOf('=');
    if (i > 0 && part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return '';
}

async function signedIn(request, env) {
  const c = readCookie(request, COOKIE);
  if (c && same(c, await cookieValue(env))) return true;
  const header = request.headers.get('Authorization') || '';
  if (!header.startsWith('Basic ')) return false;
  let decoded;
  try { decoded = atob(header.slice(6)); } catch { return false; }
  const i = decoded.indexOf(':');
  if (i < 0) return false;
  return same(decoded.slice(0, i).toLowerCase(), USER) && passwordOk(decoded.slice(i + 1), env);
}

// Only send people back to a page on this site.
function safeNext(v) {
  return typeof v === 'string' && v.startsWith('/') && !v.startsWith('//') ? v : '/';
}

function esc(s) {
  return s.replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function page(next, wrong) {
  return `<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Sign in | imoves playground</title>
<style>
@font-face{font-family:"Baloo Primary";src:url(/login/BalooPrimary-Regular.ttf) format("truetype");font-weight:400}
@font-face{font-family:"Baloo Primary";src:url(/login/BalooPrimary-SemiBold.ttf) format("truetype");font-weight:600}
@font-face{font-family:"Baloo Primary";src:url(/login/BalooPrimary-Bold.ttf) format("truetype");font-weight:700}
*{box-sizing:border-box}
body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;background:#702F8A;color:#24152b;font:400 16px/1.5 "Baloo Primary",ui-rounded,system-ui,sans-serif}
main{width:100%;max-width:400px;text-align:center}
.logo{width:220px;height:auto;margin:0 auto 28px;display:block}
.card{background:#fff;border-radius:20px;padding:28px 26px;text-align:left;box-shadow:0 14px 40px rgba(36,21,43,.25)}
h1{margin:0 0 4px;color:#702F8A;font-size:26px;font-weight:700;line-height:1.2}
p{margin:0 0 20px}
label{display:block;font-weight:600;margin-bottom:6px}
input{width:100%;font:inherit;font-size:18px;padding:12px 14px;border:2px solid #B997C5;border-radius:12px;color:#24152b}
input:focus{outline:none;border-color:#702F8A;box-shadow:0 0 0 4px #DBCBE2}
button{margin-top:16px;width:100%;font:inherit;font-weight:700;font-size:18px;padding:12px;border:0;border-radius:999px;background:#E03C31;color:#fff;cursor:pointer}
button:hover{background:#c8352b}
.err{background:#F7CECC;color:#24152b;border-radius:10px;padding:10px 12px;margin:0 0 16px;font-weight:600}
.note{color:#fff;margin-top:18px;font-size:14px}
</style></head>
<body><main>
<img class="logo" src="/login/logo-strapline-white.svg" alt="imoves – Active every day" width="275" height="139">
<div class="card">
<h1>Playground sign-in</h1>
<p>This is a private imoves playground for trying out ideas. It is not the live website.</p>
${wrong ? '<div class="err" role="alert">That password is not right. Please try again.</div>' : ''}
<form method="post" action="${LOGIN_PATH}">
<input type="hidden" name="next" value="${esc(next)}">
<label for="pw">Password</label>
<input id="pw" name="password" type="password" autocomplete="current-password" required autofocus>
<button type="submit">Sign in</button>
</form>
</div>
<p class="note">You stay signed in on this browser for 30 days.</p>
</main></body></html>`;
}

function html(body, status, extra = {}) {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex, nofollow', ...extra },
  });
}

export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);

  if (url.pathname.startsWith(PUBLIC_PREFIX)) return next();

  if (url.pathname === LOGIN_PATH) {
    if (request.method !== 'POST') return Response.redirect(new URL('/', url), 303);
    let form;
    try { form = await request.formData(); } catch { form = new FormData(); }
    const to = safeNext(form.get('next'));
    if (!(await passwordOk(form.get('password'), env))) return html(page(to, true), 401);
    return new Response(null, {
      status: 303,
      headers: {
        Location: to,
        'Set-Cookie': `${COOKIE}=${await cookieValue(env)}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
        'Cache-Control': 'no-store',
      },
    });
  }

  if (!(await signedIn(request, env))) {
    return html(page(url.pathname + url.search, false), 401);
  }

  const res = await next();
  const out = new Response(res.body, res);
  out.headers.set('X-Robots-Tag', 'noindex, nofollow');
  out.headers.set('Cache-Control', 'private, no-store');
  return out;
}
