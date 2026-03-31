import hex
import os
from pathlib import Path

# 1. Gather context from Hex
base_path = hex.get_state("base_path")
filename = hex.get_input("filename")

# 2. Perform the logic
full_path = Path(base_path) / filename

try:
    if not full_path.exists():
        print(f"Error: File {full_path} does not exist.")
        hex.set_output("content", "")
        exit(0)

    with open(full_path, "r") as f:
        content = f.read()

    # 3. Set output
    hex.set_output("content", content)
    print(f"Successfully read {len(content)} characters from {full_path}")

except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)
