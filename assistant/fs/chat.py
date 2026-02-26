import hex

# Gather state and inputs.
model_name = hex.get_state("model_name")
prompt = hex.get_input("prompt")
filestore_name = hex.get_state("filestore")
cmd = "list"

# Invoke "list" on the filestore.
result = hex.run(filestore_name, cmd, inputs={"path": "."})

# Get the list of files and print it.
files = result.get("names", [])
print(f"AI: I see these files: {', '.join(files)}")
