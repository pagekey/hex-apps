import hex
import subprocess

container_name = hex.get_state("container_name")
port_map = hex.get_state("port_map")
image = hex.get_state("image")

cmd = f"podman run -d --name {container_name} -p {port_map} {image}"

subprocess.check_call(cmd.split())
