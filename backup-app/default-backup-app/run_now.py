from pathlib import Path

import hex
from datetime import datetime

# 1. Load state
item_source = hex.get_state("item_source") or "backup-source"
item_destination = hex.get_state("item_destination") or "backup-destination"

access_token = hex.get_state("access_token")

print("🚀 Starting backup run...")

# 2. Create timestamped folder name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_folder = f"backup_{timestamp}"

print(f"📁 Creating backup folder: {backup_folder}")

# 3. List files from source
print("📡 Fetching files from source...")

res = hex.run(item_source, "list")

files = res.get("names", [])

if not files:
    print("⚠️ No files found in source.")
    exit(0)

print(f"Found {len(files)} files. Beginning download...")

# 4. Download + write each file
for f in files:
    print(f"⬇️ Downloading: {f}")

    # Download file content from source
    file_res = hex.run(item_source, "read", {"filename": f})

    content = file_res.get("content")

    if content is None:
        print(f"❌ Failed to read {f}, skipping.")
        continue

    dest_path = f"{backup_folder}/{f}"

    print(f"💾 Writing to: {dest_path}")

    # Write to destination
    hex.run(item_destination, "write", {"filename": dest_path, "content": content})

backup_dir = (
    Path(hex.run(item_destination, "get_base_path").get("base_path")) / backup_folder
)

print(f"✅ Backup complete! Saved to {backup_dir.absolute()}")
