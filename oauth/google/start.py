import hex
import secrets
import urllib.parse

# Gather inputs
client_id = hex.get_state("client_id")
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
scope = url = "https://www.googleapis.com/auth/drive.readonly"

# Generate a random state token (CSRF protection)
state = secrets.token_urlsafe(32)

# Persist state for later validation in finish
# hex.set_output("oauth_state", state)

# Build the Google OAuth authorization URL
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": "code",  # always "code" for auth code flow
    "scope": scope,
    "access_type": "offline",  # ensures we get a refresh token
    "prompt": "consent",  # forces consent to get refresh token
    "state": state,
}

url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

# Output the URL and state
hex.set_output("url", url)
hex.set_output("state", state)
