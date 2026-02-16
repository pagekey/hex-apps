import hex
import subprocess

container_name = hex.get_state("container_name")

subprocess.check_call(f"podman stop {container_name}")
subprocess.check_call(f"podman rm {container_name}")
