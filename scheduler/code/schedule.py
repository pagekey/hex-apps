import json

import hex
import subprocess
import shutil

# 1. Inputs
job_name = hex.get_input("job_name")
target_item = hex.get_input("item")
target_method = hex.get_input("method")
target_inputs_raw = hex.get_input("inputs")
target_inputs = {}

if target_inputs_raw:
    try:
        # Handle cases where it might already be a dict (for future SDK updates)
        # or parse the JSON string from the CLI
        target_inputs = (
            json.loads(target_inputs_raw)
            if isinstance(target_inputs_raw, str)
            else target_inputs_raw
        )
    except json.JSONDecodeError:
        print(f"Warning: Could not parse inputs as JSON: {target_inputs_raw}")
        target_inputs = {}

# Time fields
m, h, dom, mon, dow = [
    hex.get_input(k) or "*" for k in ["minute", "hour", "day", "month", "weekday"]
]

# 2. Find the Hex binary (ensure absolute path for Cron)
hex_path = shutil.which("hex") or "/usr/local/bin/hex"

# 3. Construct the hex command string
input_args = []
for k, v in target_inputs.items():
    input_args.append(f"-i {k}='{v}'")

full_command = (
    f"{hex_path} run {target_item} {target_method} {' '.join(input_args)}".strip()
)

# 4. Construct the Cron Line with Metadata
cron_entry = f"{m} {h} {dom} {mon} {dow} {full_command} # HEX_JOB:{job_name}"

# 5. Idempotent Update (as before)
try:
    current_cron = subprocess.check_output(["crontab", "-l"], text=True)
except subprocess.CalledProcessError:
    current_cron = ""

lines = current_cron.strip().split("\n")
new_lines = []
updated = False

for line in lines:
    if f"# HEX_JOB:{job_name}" in line:
        new_lines.append(cron_entry)
        updated = True
    elif line.strip():
        new_lines.append(line)

if not updated:
    new_lines.append(cron_entry)

# 6. Write back
subprocess.run(
    ["crontab", "-"], input="\n".join(new_lines) + "\n", text=True, check=True
)

print(f"Scheduled {job_name}: {target_item}.{target_method}")
