import glob
import os
import json
import subprocess
from pathlib import Path
from rapidfuzz import process

# --- Paths ---
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
    return apps


# ---------- UWP (MICROSOFT STORE) APPS ----------
def scan_uwp_apps(force_refresh: bool = False) -> dict:
    """Retrieve all UWP AppIDs using PowerShell."""
    global _UWP_CACHE
    if _UWP_CACHE is not None and not force_refresh:
        return _UWP_CACHE

    try:
        ps_command = "Get-StartApps | ForEach-Object { $_.Name + '::' + $_.AppID }"
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        uwp_apps = {}
        for line in result.stdout.splitlines():
            if "::" in line:
                name, appid = line.split("::", 1)
                uwp_apps[name.lower()] = appid.strip()
        _UWP_CACHE = uwp_apps
        return uwp_apps
    except Exception as e:
        print(f"⚠️ Could not scan UWP apps: {e}")
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

    print(
        f"📁 App cache exported to {CACHE_PATH} ({len(data['desktop_apps']) + len(data['uwp_apps'])} total apps)"
    )
    return data


# ---------- OPEN FUNCTION ----------
def open_app(app_name: str) -> str:
    """Open an application (normal .lnk or UWP)."""
    app_name = app_name.lower().strip()

    # 1️⃣ Try normal desktop apps
    apps_dict = scan_apps()
    _open_normal_app(app_name, apps_dict)

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
    _open_uwp_app(app_name, uwp_dict)

    # 4️⃣ Fuzzy match among UWP apps
    if uwp_dict:
        matches = process.extract(app_name, uwp_dict.keys(), limit=1)
        if matches and matches[0][1] >= 80:
            best_match = matches[0][0]
            appid = uwp_dict[best_match]
            subprocess.run(["explorer.exe", f"shell:AppsFolder\\{appid}"], shell=True)
            return f"✅ No encontré '{app_name}', pero abrí '{best_match}' (UWP)"

    return f"❌ No se encontró ninguna aplicación llamada '{app_name}'"

def _open_normal_app(app_name: str, apps_dict: dict) -> str:
    if app_name in apps_dict:
        try:
            os.startfile(apps_dict[app_name])
            return f"✅ Abriendo {app_name}"
        except Exception as e:
            return f"❌ Error al abrir {app_name}: {e}"
        
def _scan_uwp_apps(force_refresh: bool = False) -> dict:
    """Retrieve all UWP AppIDs using classic PowerShell."""
    global _UWP_CACHE
    if _UWP_CACHE is not None and not force_refresh:
        return _UWP_CACHE

    try:
        # Explicitly call Windows PowerShell (not pwsh)
        ps_command = (
            "powershell.exe -Command "
            "\"Get-StartApps | ForEach-Object { $_.Name + '::' + $_.AppID }\""
        )

        result = subprocess.run(
            ps_command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # ✅ Validar salida
        if not result.stdout:
            print("⚠️ PowerShell did not return any apps. Maybe run as admin?")
            _UWP_CACHE = {}
            return {}

        uwp_apps = {}
        for line in result.stdout.splitlines():
            if "::" in line:
                name, appid = line.split("::", 1)
                uwp_apps[name.lower()] = appid.strip()

        _UWP_CACHE = uwp_apps
        print(f"🔍 Found {len(uwp_apps)} UWP apps.")
        return uwp_apps

    except Exception as e:
        print(f"⚠️ Could not scan UWP apps: {e}")
        _UWP_CACHE = {}
        return {}
