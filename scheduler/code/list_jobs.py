import subprocess
import re
import hex

try:
    current_cron = subprocess.check_output(["crontab", "-l"], text=True)
except subprocess.CalledProcessError:
    current_cron = ""

jobs = []

# Updated Pattern:
# 1. Match the 5 time fields (.*)
# 2. Match the command until the comment tag (.*?)
# 3. Match the specific # HEX_JOB: tag and the ID (.*)
pattern = r"^(?P<schedule>\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+(?P<command>.*?)\s*# HEX_JOB:(?P<id>.*)$"

for line in current_cron.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue

    match = re.match(pattern, line)
    if match:
        jobs.append(
            {
                "id": match.group("id"),
                "schedule": match.group("schedule"),
                "raw_cmd": match.group("command"),
            }
        )

hex.set_output("jobs", jobs)
print(f"Found {len(jobs)} jobs.")
