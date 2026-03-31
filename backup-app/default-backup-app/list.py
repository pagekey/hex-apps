import hex

# Use stored names or defaults
item_source = hex.get_state("item_source") or "backup-source"
access_token = hex.get_state("access_token")

# Run list on the source (Google Drive)
# Note: we pass access_token from state
files = hex.run(item_source, "list", {"access_token": access_token, "path": ".", "query": ""})

# Set output
hex.set_output("filenames", files.get("files"))

print(f"✅ Listing from {item_source}:")
print(files.get("files"))
