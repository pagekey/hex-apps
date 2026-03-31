import hex
import secrets
import urllib.parse
import hashlib
import base64

# Gather inputs
client_id = hex.get_state("client_id")
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
scope = "https://www.googleapis.com/auth/drive.readonly"

# Generate state (same as before)
state = secrets.token_urlsafe(32)

# --- PKCE START ---

# Generate code_verifier (43-128 chars)
code_verifier = secrets.token_urlsafe(64)

# Create code_challenge (SHA256 -> base64url)
digest = hashlib.sha256(code_verifier.encode()).digest()
code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

# Store verifier for later
hex.set_state("code_verifier", code_verifier)
hex.set_state("oauth_state", state)

# --- PKCE END ---

params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",
    "scope": scope,
    "access_type": "offline",
    "prompt": "consent",
    "state": state,
    # PKCE
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}

url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

hex.set_output("url", url)
hex.set_output("state", state)
hex.set_state("state", state)

print(f"Generated URL! Now, visit: {url}")

