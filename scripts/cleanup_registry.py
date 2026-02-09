import datetime

SUPPORTED_BRANCHES = ["master", "release-2.27"]
RETENTION_DAYS = 90

def list_images():
    """
    Mock registry query.
    In real implementation, this would call registry HTTP APIs.
    """
    return [
        {
            "tag": "ubuntu-22.04-amd64:abcd1234",
            "created": datetime.datetime(2024, 1, 10),
            "branches": ["release-2.27"]
        },
        {
            "tag": "ubuntu-20.04-amd64:deadbeef",
            "created": datetime.datetime(2023, 5, 1),
            "branches": []
        }
    ]

def should_delete(image):
    age = (datetime.datetime.now() - image["created"]).days

    if age < RETENTION_DAYS:
        return False

    if any(branch in SUPPORTED_BRANCHES for branch in image["branches"]):
        return False

    return True

def main():
    images = list_images()

    for image in images:
        if should_delete(image):
            print(f"[DRY-RUN] Would delete {image['tag']}")
        else:
            print(f"Keeping {image['tag']}")

if __name__ == "__main__":
    main()
