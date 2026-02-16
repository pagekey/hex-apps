import hex
import subprocess

container_name = hex.get_state("container_name")

result = subprocess.run(f"docker ps --filter name={container_name} -q")

if result.returncode == 0:
    if len(result.stdout.strip()) > 0:
        print("Running.")
    else:
        print("Not running.")
else:
    print("Failed to run Docker command.")
