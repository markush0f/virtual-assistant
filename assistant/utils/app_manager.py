"""
app_manager.py
---------------
Scans Windows Start Menu shortcuts (.lnk) and allows opening apps by name.
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

    # Fuzzy match (find best 3)
    matches = process.extract(app_name, apps_dict.keys(), limit=3)
    if not matches or matches[0][1] < 60:
        return f"❌ No se encontró ninguna aplicación llamada '{app_name}'"

    best_match, score, _ = matches[0]
    if score >= 85:
        os.startfile(apps_dict[best_match])
        return f"✅ Abriendo {best_match}"
    else:
        # Show options to user
        options = "\n".join(
            [f"{i+1}. {m[0]} ({m[1]:.1f}%)" for i, m in enumerate(matches)]
        )
        print(f"\nCoincidencias encontradas:\n{options}")
        try:
            choice = int(input("\nElige una aplicación (1-3): "))
            if 1 <= choice <= len(matches):
                selected_app = matches[choice - 1][0]
                os.startfile(apps_dict[selected_app])
                return f"✅ Abriendo {selected_app}"
            else:
                return "⚠️ Opción fuera de rango."
        except ValueError:
            return "⚠️ Entrada no válida."


def app_exists(app_name: str) -> bool:
    """
    Checks if an app is known in the Start Menu cache.
    """
    apps_dict = scan_apps()
    return app_name.lower() in apps_dict


def list_apps(limit: int = 20) -> list[str]:
    """
    Returns a limited list of detected apps (for debugging or UI display).
    """
    apps = scan_apps()
    return sorted(apps.keys())[:limit]


# --- CLI for standalone test ---
if __name__ == "__main__":
    apps = scan_apps()
    print(f"📦 {len(apps)} aplicaciones detectadas.")
    for app in list_apps(20):
        print("-", app)

    choice = input("\nEscribe el nombre de una app a abrir: ").strip()
    print(open_app(choice))
