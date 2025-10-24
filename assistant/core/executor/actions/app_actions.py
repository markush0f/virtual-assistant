import os
import psutil
from assistant.utils import app_manager


def open_app(target: str) -> str:
    if not target:
        return "No app specified."
    found = app_manager.open_app(target)
    return f"Opened {target}" if found else f"Could not find {target}"


def close_app(target: str) -> str:
    if not target:
        return "No app specified."
    for proc in psutil.process_iter(["name"]):
        if target.lower() in proc.info["name"].lower():
            proc.terminate()
            return f"Closed {target}"
    return f"Could not find {target}"
