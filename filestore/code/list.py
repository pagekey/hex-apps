import hex
import os
from pathlib import Path

# 1. Get context
# base_path: from Item state (e.g., /home/user/hex-vault)
# path: from CLI input (e.g., "." or "subfolder")
base_path = Path(hex.get_state("base_path"))
sub_path = hex.get_input("path") or "."

target_dir = (base_path / sub_path).resolve()

# 2. Safety Check: Ensure we aren't escaping the base_path
if not str(target_dir).startswith(str(base_path)):
    print(f"Error: Path {target_dir} is outside of base_path {base_path}")
    exit(1)

try:
    # 3. List files
    names = [f for f in os.listdir(target_dir)]

    # 4. Set output
    hex.set_output("names", names)

    # Human-friendly output for the console
    print(f"Found {len(names)} files in {target_dir}")

except Exception as e:
    print(f"Failed to list directory: {e}")
    exit(1)
