import hex

# Use stored names or defaults
item_source = hex.get_state("item_source") or "backup-source"
access_token = hex.get_state("access_token")

print(f"Scheduled backup run (listing files only for now)...")

# Run list on the source (Google Drive)
files = hex.run(item_source, "list", {"access_token": access_token})

print(f"✅ Scheduled run from {item_source}:")
print(files.get("files"))
