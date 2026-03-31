import hex

# Ask for source folder
source = hex.run(
    "cli-user-input", "get_string", {"prompt": "Enter Google Drive source folder"}
)["value"]
hex.set_state("source", "backup-source")
hex.create_item("backup-source", "google-drive", {"base_path": source})

# Ask for backup destination
destination = hex.run(
    "cli-user-input", "get_string", {"prompt": "Enter backup destination"}
)["value"]
hex.set_state("destination", "backup-destination")
hex.create_item("backup-destination", "local-files", {"base_path": destination})


# Save state (so test/schedule can use it)
hex.set_output("source", source)
hex.set_output("destination", destination)

print(f"✅ Backup setup complete: {source} -> {destination}")
