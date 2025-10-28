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

# --- CONFIGURATION ---
START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
]

CACHE_PATH = Path(__file__).parent / "apps_cache.json"

_APPS_CACHE = None
_UWP_CACHE = None


# ---------- NORMAL .LNK APPS ----------
def scan_apps(force_refresh: bool = False) -> dict:
    """Scan Start Menu shortcuts and cache results."""
    global _APPS_CACHE
    if _APPS_CACHE is not None and not force_refresh:
        return _APPS_CACHE

    apps = {}
    for base_path in START_MENU_PATHS:
        if os.path.exists(base_path):
            for file in glob.glob(base_path + "/**/*.lnk", recursive=True):
                name = os.path.basename(file).replace(".lnk", "").lower()
                apps[name] = file

    _APPS_CACHE = apps
    print(f"🖥️ Found {len(apps)} desktop apps.")
    return apps


# ---------- UWP (MICROSOFT STORE) APPS ----------
def scan_uwp_apps(force_refresh: bool = False) -> dict:
    """Retrieve all UWP AppIDs using PowerShell, with manual decoding and fallback."""
    global _UWP_CACHE
    if _UWP_CACHE is not None and not force_refresh:
        return _UWP_CACHE

    try:
        ps_command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            "Get-StartApps | ForEach-Object { $_.Name + '::' + $_.AppID }",
        ]

        # Run without auto-decoding to handle ANSI safely
        result = subprocess.run(
            ps_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

        # Manual decoding (UTF-8 → fallback CP1252)
        try:
            output = result.stdout.decode("utf-8", errors="ignore")
        except UnicodeDecodeError:
            output = result.stdout.decode("cp1252", errors="ignore")

        # Fallback if PowerShell doesn't return anything
        if not output.strip():
            print("⚠️ 'Get-StartApps' returned nothing. Trying Get-AppxPackage...")
            alt_command = [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "Get-AppxPackage | ForEach-Object { $_.Name + '::' + $_.PackageFamilyName }",
            ]
            result = subprocess.run(
                alt_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=False,
            )
            try:
                output = result.stdout.decode("utf-8", errors="ignore")
            except UnicodeDecodeError:
                output = result.stdout.decode("cp1252", errors="ignore")

        if not output.strip():
            print("⚠️ PowerShell did not return any UWP apps.")
            _UWP_CACHE = {}
            return {}

        uwp_apps = {}
        for line in output.splitlines():
            if "::" in line:
                name, appid = line.split("::", 1)
                uwp_apps[name.lower().strip()] = appid.strip()

        print(f"📱 Found {len(uwp_apps)} UWP apps.")
        _UWP_CACHE = uwp_apps
        return uwp_apps

    except Exception as e:
        print(f"⚠️ Could not scan UWP apps: {e}")
        _UWP_CACHE = {}
        return {}


# ---------- CACHE EXPORT ----------
def export_apps_to_json():
    """Export all detected apps (.lnk + UWP) to apps_cache.json."""
    data = {
        "desktop_apps": scan_apps(force_refresh=True),
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
