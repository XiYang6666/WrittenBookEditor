import subprocess
import pathlib
import platform


def open_folder(path: str):
    filepath = pathlib.Path(path)
    if platform.system() == "Windows":
        if filepath.is_dir():
            subprocess.run(["explorer", str(filepath.resolve())])
        else:
            subprocess.run(["explorer", "/select,", str(filepath.resolve())])
    elif platform.system() == "Darwin":
        if filepath.is_dir():
            subprocess.run(["open", str(filepath.resolve())])
        else:
            subprocess.run(["open", "-R", str(filepath.resolve())])
    elif platform.system() == "Linux":
        if filepath.is_dir():
            subprocess.run(["xdg-open", str(filepath.resolve())])
        else:
            subprocess.run(["xdg-open", str(filepath.parent.resolve())])
