import os

import hex

# Resolve helper items
item_user_input = "cli-user-input"
item_auth = "google-auth"

# Ensure helper items exist
if not hex.get_item(item_user_input):
    hex.create_item(item_user_input, "cli-user-input", emoji="⌨️")

if not hex.get_item(item_auth):
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

    hex.create_item(
        item_auth,
        "google-auth",
        {"client_id": client_id, "client_secret": client_secret},
        emoji="🛠️",
    )

# --- OAuth flow ---
auth_res = hex.run(item_auth, "generate_url")
auth_url = auth_res.get("url")

print(f"Authorize here:\n{auth_url}")

code = hex.run(
    item_user_input, "get_string", {"prompt": "Paste the authorization code: "}
)["value"]

token_res = hex.run(item_auth, "generate_token", {"code": code})

access_token = token_res.get("access_token")
refresh_token = token_res.get("refresh_token")

# Store in THIS ITEM (google-drive)
hex.set_state("access_token", access_token)
hex.set_state("refresh_token", refresh_token)

# Ask for base path
base_path = hex.run(
    item_user_input,
    "get_string",
    {"prompt": "Enter Google Drive folder (name or ID): "},
)["value"]

hex.set_state("base_path", base_path)

print("✅ Google Drive setup complete!")
