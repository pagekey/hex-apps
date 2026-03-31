import hex
import requests

# Gather inputs
code = hex.get_input("code")
state = hex.get_input("oauth_state")
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

# Load client credentials from state
client_id = hex.get_state("client_id")
client_secret = hex.get_state("client_secret")  # optional if you have one

# Exchange the authorization code for tokens
resp = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    },
)

if resp.status_code != 200:
    raise Exception(f"Token exchange failed: {resp.text}")

data = resp.json()

# Output tokens
hex.set_output("access_token", data.get("access_token"))
hex.set_output("refresh_token", data.get("refresh_token"))
hex.set_output("expires_in", data.get("expires_in"))
hex.set_output("token_type", data.get("token_type"))

# Persist refresh token for later use
hex.set_output("refresh_token", data.get("refresh_token"))
