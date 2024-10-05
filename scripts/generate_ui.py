from pathlib import Path
from os import system

path = Path("src/writtenbookeditor/gui")
for file in path.glob("*.ui"):
    system(f"pyside6-uic {file} -o {file.parent.joinpath('ui_' + file.stem + '.py')}")
