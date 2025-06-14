import sys

if __name__ == "__main__":
    sys.path.insert(0, "./src")

from writtenbookeditor.core.loader import load_builtin_plugins, load_plugin_dirs, load_plugins


def test_plugin_loader():
    load_builtin_plugins()
    load_plugin_dirs()


if __name__ == "__main__":
    test_plugin_loader()
