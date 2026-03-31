import hex
from pathlib import Path

# 1. Gather context from Hex
base_path = hex.get_state("base_path")
filename = hex.get_input("filename")
content = hex.get_input("content")

# 2. Perform the logic
full_path = Path(base_path) / filename

try:
    # Ensure directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, "w") as f:
        f.write(content)

    print(f"Successfully saved to {full_path}")
    # No specific outputs required by contract, but we could set one for logs
    hex.set_output("saved_path", str(full_path))

except Exception as e:
    print(f"Error saving file: {e}")
    exit(1)
