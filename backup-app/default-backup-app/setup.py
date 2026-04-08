from pathlib import Path

import hex

# 1. Resolve item names from state or use defaults
item_user_input = hex.get_state("item_user_input") or "cli-user-input"
item_source = hex.get_state("item_source") or "backup-source"
item_destination = hex.get_state("item_destination") or "backup-destination"

# Update state so we remember these
hex.set_state("item_user_input", item_user_input)
hex.set_state("item_source", item_source)
hex.set_state("item_destination", item_destination)

# 2. Ensure items exist
if not hex.get_item(item_user_input):
    hex.create_item(item_user_input, "cli-user-input", emoji="⌨️")

if not hex.get_item(item_source):
    source_path = hex.run(
        item_user_input, "get_string", {"prompt": "Enter Google Drive source folder: "}
    )["value"]
    hex.create_item(item_source, "google-drive", {"base_path": source_path}, emoji="📂")
    hex.run(item_source, "setup", inputs={"base_path": source_path})

if not hex.get_item(item_destination):
    dest_path = hex.run(
        item_user_input, "get_string", {"prompt": "Enter local backup destination: "}
    )["value"]
    dest_path = str(Path.home() / dest_path)
    hex.create_item(
        item_destination, "local-files", {"base_path": dest_path}, emoji="📂"
    )

print("✅ Backup setup complete! Access token saved.")
print("Next, run 'test' to verify it works.")
