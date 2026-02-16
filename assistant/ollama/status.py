import hex
import subprocess

container_name = hex.get_state("container_name")

result = subprocess.run(f"podman ps --filter name={container_name} -q".split())

if result.returncode == 0:
    if result.stdout and len(result.stdout.strip()) > 0:
        print("Running.")
    else:
        print("Not running.")
else:
    print("Failed to run container command.")
