#!/usr/bin/env python3
"""Change the playground password.

    python3 playground/set-password.py "new-password"

Writes a new random salt and the salted SHA-256 hash into playground/functions/_middleware.js.
The password itself is never stored in the repository (it is public). Push the playground branch
afterwards for the change to take effect.
"""
import hashlib, os, re, secrets, sys

if len(sys.argv) != 2 or len(sys.argv[1]) < 12:
    sys.exit('usage: set-password.py "new-password"  (at least 12 characters)')
pw = sys.argv[1]
salt = secrets.token_hex(16)
digest = hashlib.sha256((salt + pw).encode()).hexdigest()
f = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'functions', '_middleware.js')
src = open(f, encoding='utf-8').read()
src = re.sub(r"const SALT = '[0-9a-f]*';", f"const SALT = '{salt}';", src)
src = re.sub(r"const HASH = '[0-9a-f]*';", f"const HASH = '{digest}';", src)
open(f, 'w', encoding='utf-8').write(src)
print('password updated in', f)
