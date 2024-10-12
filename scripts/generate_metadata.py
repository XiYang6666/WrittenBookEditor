import tomllib
import json
import sys

with open("./pyproject.toml", "rb") as f:
    pyproject_data = tomllib.load(f)

with open("./data/metadata.json", "w", encoding="utf-8") as f:
    version = pyproject_data["project"]["version"]
    if len(sys.argv) == 2:
        version += sys.argv[1]
    metadata = {
        "version": version,
    }
    json.dump(metadata, f)
