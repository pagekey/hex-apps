import hex

# Ask for source folder
source = hex.run("cli-user-input", "get_string", {"prompt": "Enter source folder"})[
    "value"
]
hex.set_state("source", source)

# Ask for backup destination
destination = hex.run(
    "cli-user-input", "get_string", {"prompt": "Enter backup destination"}
)["value"]

# Save state (so test/schedule can use it)
hex.set_output("source", source)
hex.set_output("destination", destination)

print(f"✅ Backup setup complete: {source} -> {destination}")
