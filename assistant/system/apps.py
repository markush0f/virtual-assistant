import os
import webbrowser

APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
}


def open_app(app_name: str):
    """Open a local application if available in dictionary."""
    if app_name in APPS:
        os.system(APPS[app_name])
    else:
        print(f"App '{app_name}' not found in dictionary")
