---
tags: [concept, web, authentication]
---

# Cookies, Sessions, and JWTs

## Why cookies are a trust boundary

HTTP is stateless - cookies are the standard mechanism for a server to "remember" something about a client across requests, by handing the client a piece of data that's sent back with every subsequent request. The problem: **a plain cookie is just a value the browser stores and the user can freely edit** (via dev tools → Application/Storage → Cookies, or the `document.cookie` API in the console). If a server trusts a cookie's value directly for an authorization decision - e.g. an `admin=false` flag, or a `time=<value>` field used server-side - without any cryptographic protection, the user can simply edit that value and have the server believe whatever they typed.

## Why this is subtly different from session IDs

A properly designed session system stores the *actual* state (is this user an admin? what's in their cart?) server-side, keyed by an opaque, unguessable session ID that's the only thing handed to the client - the ID itself carries no meaning an attacker could exploit by editing it, since changing it to a different random string just invalidates the session rather than escalating privilege. The vulnerable pattern is specifically when the meaningful data itself (`admin=true/false`) is placed directly in client-controlled storage with nothing to prevent tampering.

## Why Base64-looking cookie values aren't automatically "secure"

A cookie value that "looks encoded" (ending in `%3D`/`=`, or otherwise non-human-readable at a glance) is very often just Base64-encoded plain data, not encrypted (see [[Encoding vs Encryption]]) - decoding it is a one-line operation, and the fact that it's not immediately human-readable provides no actual confidentiality or integrity guarantee.

## JWTs specifically

A JSON Web Token has three Base64url-encoded parts - header, payload, signature - and anyone can decode the header/payload without any key (they're not encrypted, just encoded; tools like jwt.io do this instantly). The **signature** is what's supposed to make a JWT trustworthy: it's a cryptographic proof, computed over the header+payload using a secret key (for HMAC algorithms like HS256) or a private key (for RSA-based algorithms), that the token hasn't been tampered with since the server issued it.

This is exactly why JWTs are only as secure as their signing secret:
- If the signing secret is a weak, guessable passphrase, it can be **cracked offline** the same way a password hash is cracked (see [[Password and Hash Cracking]]) - a tool like `john` with the `HMAC-SHA256` format and a wordlist tries candidate secrets, computing the same signature algorithm the server uses, until one produces a signature matching the captured token.
- Once the secret is recovered, an attacker can **forge a new, validly-signed token with arbitrary claims** (e.g. change `"username": "alice"` to `"username": "admin"`, recompute the signature with the cracked secret) - and the server will accept it, because the signature check passes; the server has no way to know the *content* was attacker-chosen rather than legitimately issued.

## The underlying lesson

Client-controlled state is only trustworthy to the extent it's cryptographically protected *and* that protection relies on a secret strong enough to resist offline cracking - an easily-guessed signing key makes a JWT's cryptographic signature a formality rather than a real guarantee.
