// Password gate for the imoves playground (Cloudflare Pages Function, runs before every request).
//
// The browser asks for a username and password (HTTP Basic auth). Only a salted SHA-256 hash of the
// password is stored here, because this repository is public. To change the password, run
//   python3 playground/set-password.py "new-password"
// which rewrites SALT and HASH below, then push the playground branch.
//
// If the Pages project has an environment variable PLAYGROUND_PASSWORD, that is accepted instead
// (so the password can also be changed in the Cloudflare dashboard without a commit).

const USER = 'imoves';
const SALT = 'bc161a36039730007c9a4c4a8b159f3f';
const HASH = '554004400cc6800a3620ab33c2f99ba556e8ac84dde16d40dd464f187ec22199';
const REALM = 'imoves playground';

async function sha256hex(text) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, '0')).join('');
}

// Compare without leaking how many characters matched.
function same(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

async function allowed(request, env) {
  const header = request.headers.get('Authorization') || '';
  if (!header.startsWith('Basic ')) return false;
  let decoded;
  try { decoded = atob(header.slice(6)); } catch { return false; }
  const i = decoded.indexOf(':');
  if (i < 0) return false;
  const user = decoded.slice(0, i), pass = decoded.slice(i + 1);
  if (!same(user.toLowerCase(), USER)) return false;
  if (env && env.PLAYGROUND_PASSWORD && same(pass, env.PLAYGROUND_PASSWORD)) return true;
  return same(await sha256hex(SALT + pass), HASH);
}

export async function onRequest({ request, env, next }) {
  if (!(await allowed(request, env))) {
    return new Response('This is a private imoves playground. Please sign in.', {
      status: 401,
      headers: {
        'WWW-Authenticate': `Basic realm="${REALM}", charset="UTF-8"`,
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Robots-Tag': 'noindex, nofollow',
      },
    });
  }
  const res = await next();
  const out = new Response(res.body, res);
  out.headers.set('X-Robots-Tag', 'noindex, nofollow');
  out.headers.set('Cache-Control', 'private, no-store');
  return out;
}
