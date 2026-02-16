import hex
import subprocess

container_name = hex.get_state("container_name")

subprocess.check_call(f"docker stop {container_name}")
subprocess.check_call(f"docker rm {container_name}")
