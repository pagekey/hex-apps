import hex
import requests

# Gather inputs
code = hex.get_input("code")
redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

client_id = hex.get_state("client_id")
client_secret = hex.get_state("client_secret")

# PKCE: retrieve stored verifier
code_verifier = hex.get_state("code_verifier")

resp = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        # PKCE
        "code_verifier": code_verifier,
    },
)

if resp.status_code != 200:
    raise Exception(f"Token exchange failed: {resp.text}")

data = resp.json()

hex.set_output("access_token", data.get("access_token"))
hex.set_state("access_token", data.get("access_token"))
hex.set_output("refresh_token", data.get("refresh_token"))
hex.set_state("refresh_token", data.get("refresh_token"))
hex.set_output("expires_in", data.get("expires_in"))
hex.set_output("token_type", data.get("token_type"))
