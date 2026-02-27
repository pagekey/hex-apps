import hex
import subprocess
import sys

# 1. Inputs
job_name = hex.get_input("job_name")

if not job_name:
    print("Error: job_name is required to unschedule.")
    sys.exit(1)

# 2. Get existing crontab
try:
    current_cron = subprocess.check_output(["crontab", "-l"], text=True)
except subprocess.CalledProcessError:
    # If no crontab exists, there's nothing to unschedule
    print("No crontab found for current user.")
    sys.exit(0)

# 3. Filter out the specific job
lines = current_cron.strip().split("\n")
# We look for the exact HEX_JOB tag we created in schedule.py
new_lines = [line for line in lines if f"# HEX_JOB:{job_name}" not in line]

if len(new_lines) == len(lines):
    print(f"Job '{job_name}' not found in crontab. No changes made.")
    hex.set_output("status", "not_found")
    sys.exit(0)

# 4. Write back
new_cron = "\n".join(new_lines) + "\n"

# If the new crontab is empty, some systems prefer 'crontab -r'
# but piping an empty string to 'crontab -' usually works to clear it.
process = subprocess.run(["crontab", "-"], input=new_cron, text=True)

if process.returncode == 0:
    print(f"Successfully unscheduled job: {job_name}")
    hex.set_output("status", "removed")
else:
    print("Failed to update crontab.")
    sys.exit(1)
