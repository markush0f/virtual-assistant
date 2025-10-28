"""
App Manager
-----------
Handles scanning, caching and opening of Windows desktop (.lnk) and UWP (Microsoft Store) apps.

✅ Features:
- Scans Start Menu shortcuts recursively
- Scans UWP apps via PowerShell (safe decoding)
- Opens both normal and UWP apps (with fuzzy search)
- Exports app cache to JSON for faster access
"""

import glob
import os
import json
import subprocess
from pathlib import Path
from rapidfuzz import process

from assistant.utils.app_manager.scanner import scan_apps, scan_uwp_apps

# --- CONFIGURATION ---
START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
]

CACHE_PATH = Path(__file__).parent / "apps_cache.json"





# ---------- CACHE EXPORT ----------
def export_apps_to_json():
    """Export all detected apps (.lnk + UWP) to apps_cache.json."""
    data = {
        "desktop_apps": scan_apps(force_refresh=True, start_menu_paths=START_MENU_PATHS),
        "uwp_apps": scan_uwp_apps(force_refresh=True),
    }

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    total = len(data["desktop_apps"]) + len(data["uwp_apps"])
    print(f"📁 App cache exported to {CACHE_PATH} ({total} total apps)")
    return data


# ---------- OPEN FUNCTION ----------
def open_app(app_name: str) -> str:
    """Open an application (normal .lnk or UWP)."""
    app_name = app_name.lower().strip()

    # 1️⃣ Try normal desktop apps
    apps_dict = scan_apps()
    if app_name in apps_dict:
        try:
            os.startfile(apps_dict[app_name])
            return f"✅ Abriendo {app_name}"
        except Exception as e:
            return f"❌ Error al abrir {app_name}: {e}"

    # 2️⃣ Fuzzy match among .lnk
    if apps_dict:
        matches = process.extract(app_name, apps_dict.keys(), limit=1)
        if matches and matches[0][1] >= 80:
            best_match = matches[0][0]
            try:
                os.startfile(apps_dict[best_match])
                return f"✅ No encontré '{app_name}', pero abrí '{best_match}'"
            except Exception as e:
                return f"❌ Error al abrir '{best_match}': {e}"

    # 3️⃣ Try UWP (Microsoft Store) apps
    uwp_dict = scan_uwp_apps()
    if app_name in uwp_dict:
        appid = uwp_dict[app_name]
        try:
            subprocess.run(["explorer.exe", f"shell:AppsFolder\\{appid}"], shell=True)
            return f"✅ Abriendo app UWP '{app_name}'"
        except Exception as e:
            return f"❌ Error al abrir UWP '{app_name}': {e}"

    # 4️⃣ Fuzzy match among UWP apps
    if uwp_dict:
        matches = process.extract(app_name, uwp_dict.keys(), limit=1)
        if matches and matches[0][1] >= 80:
            best_match = matches[0][0]
            appid = uwp_dict[best_match]
            subprocess.run(["explorer.exe", f"shell:AppsFolder\\{appid}"], shell=True)
            return f"✅ No encontré '{app_name}', pero abrí '{best_match}' (UWP)"

    return f"❌ No se encontró ninguna aplicación llamada '{app_name}'"
