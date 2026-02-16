from pathlib import Path
import hex
import subprocess

container_name = hex.get_state("container_name")
port_map = hex.get_state("port_map")
image = hex.get_state("image")
path = Path(hex.get_state("path")).absolute()

cmd = f"podman run -d -v {path}:/srv --name {container_name} -p {port_map} {image} caddy file-server --root /srv --listen :80 --browse"

subprocess.check_call(cmd.split())
