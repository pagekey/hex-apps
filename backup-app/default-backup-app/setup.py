import hex

# 1. Resolve item names from state or use defaults
item_auth = hex.get_state("item_auth") or "google-auth"
item_user_input = hex.get_state("item_user_input") or "cli-user-input"
item_source = hex.get_state("item_source") or "backup-source"
item_destination = hex.get_state("item_destination") or "backup-destination"

# Update state so we remember these
hex.set_state("item_auth", item_auth)
hex.set_state("item_user_input", item_user_input)
hex.set_state("item_source", item_source)
hex.set_state("item_destination", item_destination)

# 2. Ensure items exist
if not hex.get_item(item_user_input):
    hex.create_item(item_user_input, "cli-user-input", emoji="⌨️")

if not hex.get_item(item_auth):
    # Ask for credentials if they aren't provided by default
    client_id = hex.run(item_user_input, "get_string", {"prompt": "Enter Google Client ID: "})["value"]
    client_secret = hex.run(item_user_input, "get_string", {"prompt": "Enter Google Client Secret: "})["value"]
    hex.create_item(item_auth, "google-auth", {"client_id": client_id, "client_secret": client_secret}, emoji="🛠️")

if not hex.get_item(item_source):
    source_path = hex.run(item_user_input, "get_string", {"prompt": "Enter Google Drive source folder: "})["value"]
    hex.create_item(item_source, "google-drive", {"base_path": source_path}, emoji="📂")

if not hex.get_item(item_destination):
    dest_path = hex.run(item_user_input, "get_string", {"prompt": "Enter local backup destination: "})["value"]
    hex.create_item(item_destination, "local-files", {"base_path": dest_path}, emoji="📂")

# 3. Auth flow
# generate_url returns the URL and state
auth_res = hex.run(item_auth, "generate_url")
auth_url = auth_res.get("url")

print(f"Please follow this link to authorize: {auth_url}")

code = hex.run(item_user_input, "get_string", {"prompt": "Follow the link and paste the token: "})["value"]

# Use generate_token to get the actual auth token
token_res = hex.run(item_auth, "generate_token", {"code": code})

# 4. Save in the backup manager (the current app item)
access_token = token_res.get("access_token")
refresh_token = token_res.get("refresh_token")
hex.set_state("access_token", access_token)
hex.set_state("refresh_token", refresh_token)

print(f"✅ Backup setup complete! Access token saved.")

# 5. Finally, list the files in the google drive remote
print("\n--- Listing Google Drive Files ---")
files_res = hex.run(item_source, "list", {"access_token": access_token, "path": ".", "query": ""})
print(f"Files found: {files_res.get('files')}")
