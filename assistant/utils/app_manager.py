"""
app_manager.py
---------------
Scans Windows Start Menu shortcuts (.lnk) and allows opening apps by name.
Fully autonomous — no user input required.
Integrated with the assistant intent system.
"""

import glob
import os
from rapidfuzz import process

# --- Directories to scan ---
START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
]

# --- Cache of scanned applications ---
_APPS_CACHE = None


def scan_apps(force_refresh: bool = False) -> dict:
    """
    Scans Windows Start Menu shortcuts and builds a dictionary of available apps.
    Cached to improve performance.
    """
    global _APPS_CACHE
    if _APPS_CACHE is not None and not force_refresh:
        return _APPS_CACHE

    apps = {}
    for base_path in START_MENU_PATHS:
        if os.path.exists(base_path):
            for file in glob.glob(base_path + "/**/*.lnk", recursive=True):
                app_name = os.path.basename(file).replace(".lnk", "").lower()
                apps[app_name] = file

    _APPS_CACHE = apps
    return apps


def open_app(app_name: str) -> str:
    """
    Opens an app by name (case-insensitive, fuzzy matching fallback).
    Returns a message for the assistant to display.
    """
    apps_dict = scan_apps()
    app_name = app_name.lower().strip()

    if not apps_dict:
        return "❌ No se detectaron accesos directos en el sistema."

    # Exact match
    if app_name in apps_dict:
        try:
            os.startfile(apps_dict[app_name])
            return f"✅ Abriendo {app_name}"
        except Exception as e:
            return f"❌ Error al abrir {app_name}: {e}"

    # Fuzzy match (find best candidate)
    matches = process.extract(app_name, apps_dict.keys(), limit=3)

    if not matches:
        return f"❌ No se encontró ninguna aplicación llamada '{app_name}'"

    best_match, score, _ = matches[0]

    # Autoselect best match if high confidence
    if score >= 80:
        try:
            os.startfile(apps_dict[best_match])
            return f"✅ No encontré '{app_name}', pero abrí '{best_match}' (coincidencia {score:.0f}%)"
        except Exception as e:
            return f"❌ Error al abrir '{best_match}': {e}"

    return f"❌ No se encontró ninguna aplicación suficientemente parecida a '{app_name}' (mejor coincidencia: {best_match}, {score:.0f}%)"


def app_exists(app_name: str) -> bool:
    """Checks if an app is known in the Start Menu cache."""
    apps_dict = scan_apps()
    return app_name.lower() in apps_dict


def list_apps(limit: int = 20) -> list[str]:
    """Returns a limited list of detected apps (for debugging or UI display)."""
    apps = scan_apps()
    return sorted(apps.keys())[:limit]
