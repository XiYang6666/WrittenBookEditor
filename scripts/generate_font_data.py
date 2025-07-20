import json
import os
import shutil
from pathlib import Path
from typing import TypedDict

from isort import file

VERSIONS = [
    ("1.6.2", "legacy"),
    ("1.7.3", "1.7.3"),
    ("1.9", "1.9"),
    ("1.13", "1.13"),
    ("1.16", "1.16"),
    ("1.20", "5"),
    ("1.20.3", "12"),
    ("1.20.5", "16"),
    ("1.21", "17"),
    ("1.21.4", "19"),
    ("1.21.6", "26"),
]


class ObjectData(TypedDict):
    hash: str
    size: int


def get_jar_path(version: str) -> Path:
    return Path(f"D:\\Minecraft\\.minecraft\\versions\\font-test-{version}\\font-test-{version}.jar")


def get_index(index: str) -> dict[str, ObjectData]:
    with open(f"D:\\Minecraft\\.minecraft\\assets\\indexes\\{index}.json", "r") as f:
        return json.load(f)["objects"]


for i in range(len(VERSIONS)):
    version = VERSIONS[i][0]
    index = VERSIONS[i][1]
    # 提取资源
    Path(f"./data/font/minecraft_{version}/").mkdir(parents=True, exist_ok=True)
    os.system(f'python ./scripts/extract_fonts.py "{get_jar_path(version)}" -o "./data/font/minecraft_{version}/"')
    # 提取散列资源
    index_mapping = get_index(index)
    for file_name in index_mapping:
        if not file_name.startswith("minecraft/font/"):
            continue
        object_data = index_mapping[file_name]
        hash = object_data["hash"]
        path = Path(f"D:\\Minecraft\\.minecraft\\assets\\objects\\{hash[:2]}\\{hash}")
        target = Path(f"./data/font/minecraft_{version}/") / file_name.removeprefix("minecraft/font/")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)

    paths = [f"./data/font/minecraft_{v[0]}/" for v in reversed(VERSIONS[:i])]
    os.system(f"python ./scripts/compare_dirs.py --sources {' '.join(paths)} --target ./data/font/minecraft_{version}/ --clean")
