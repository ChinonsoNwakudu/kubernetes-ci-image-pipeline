import yaml
import subprocess
import hashlib

REGISTRY = "registry.example.com/kubespray-ci"

with open("config/images.yml") as f:
    images = yaml.safe_load(f)["images"]

for image in images:
    tag_base = f"{image['distro']}-{image['version']}-{image['arch']}"
    digest = hashlib.sha256(str(image).encode()).hexdigest()[:8]

    image_tag = f"{REGISTRY}/{tag_base}:{digest}"
    latest_tag = f"{REGISTRY}/{tag_base}:latest"

    subprocess.run([
        "docker", "build",
        "-t", image_tag,
        "-t", latest_tag,
        "."
    ], check=True)

    subprocess.run(["docker", "push", image_tag], check=True)
    subprocess.run(["docker", "push", latest_tag], check=True)
