import hex

# Gather state and inputs.
model_name = hex.get_state("model_name")
prompt = hex.get_input("prompt")
filestore_name = hex.get_state("filestore")
cmd = "list"

# Invoke "list" on the filestore.
result = hex.run(filestore_name, cmd, inputs={"path": "."})

# Get the list of files and print it.
files = result.get("files", [])
print(f"AI ({model_name}): I see these files: {', '.join(files)}")
