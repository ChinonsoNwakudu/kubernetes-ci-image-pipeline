import yaml
import subprocess
import hashlib
from datetime import datetime

REGISTRY = "registry.example.com/kubespray-ci"

with open("config/images.yml") as f:
    config = yaml.safe_load(f)

for image in config["images"]:
    tag_base = f"{image['distro']}-{image['version']}-{image['arch']}"

    # Deterministic tag based on config
    hash_input = f"{image}".encode()
    digest = hashlib.sha256(hash_input).hexdigest()[:8]

    tag = f"{REGISTRY}/{tag_base}:{digest}"
    latest_tag = f"{REGISTRY}/{tag_base}:latest"

    print(f"Building {tag}")

    subprocess.run([
        "docker", "build",
        "--build-arg", f"DISTRO={image['distro']}",
        "--build-arg", f"VERSION={image['version']}",
        "-t", tag,
        "-t", latest_tag,
        "."
    ], check=True)

    subprocess.run(["docker", "push", tag], check=True)
    subprocess.run(["docker", "push", latest_tag], check=True)
