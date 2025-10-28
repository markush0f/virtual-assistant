import os
import psutil
from assistant.utils import app_manager
from assistant.actions_registry import register_action


@register_action(description="Open a desktop application by name")
def open_app(target: str) -> str:
    """Open a desktop application by name."""
    if not target:
        return "No app specified."

    found = app_manager.open_app(target)
    msg = f"Opened {target}" if found else f"Could not find {target}"
    print(f"{msg}")
    return msg


@register_action(description="Close an application process by name", type="safe")
def close_app(target: str) -> str:
    """Close an application process by name."""
    if not target:
        return "No app specified."

    for proc in psutil.process_iter(["name"]):
        try:
            if target.lower() in proc.info["name"].lower():
                proc.terminate()
                msg = f"Closed {target}"
                print(f"{msg}")
                return msg
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    msg = f"Could not find {target}"
    print(f"{msg}")
    return msg
