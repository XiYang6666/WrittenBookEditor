from . import App

if __name__ == "__main__":
    import sys

    app = App(sys.argv)
    sys.excepthook = app.on_exception
    sys.exit(app.exec())
