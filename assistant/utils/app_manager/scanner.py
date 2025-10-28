import glob
import os
import subprocess

# private constants
ps_command = [
    "powershell.exe",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    "Get-StartApps | ForEach-Object { $_.Name + '::' + $_.AppID }",
]

alt_command = [
    "powershell.exe",
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-Command",
    "Get-AppxPackage | ForEach-Object { $_.Name + '::' + $_.PackageFamilyName }",
]

_APPS_CACHE = None
_UWP_CACHE = None


# ---------- NORMAL .LNK APPS ----------
def scan_apps(
    start_menu_paths=None,
    force_refresh: bool = False,
) -> dict:
    """Scan Start Menu shortcuts and cache results."""
    global _APPS_CACHE
    if _APPS_CACHE is not None and not force_refresh:
        return _APPS_CACHE

    apps = {}
    for base_path in start_menu_paths:
        if os.path.exists(base_path):
            for file in glob.glob(base_path + "/**/*.lnk", recursive=True):
                name = os.path.basename(file).replace(".lnk", "").lower()
                apps[name] = file

    _APPS_CACHE = apps
    print(f"Found {len(apps)} desktop apps.")
    return apps


# ---------- UWP (MICROSOFT STORE) APPS ----------
def scan_uwp_apps(force_refresh: bool = False) -> dict:
    """Retrieve all UWP AppIDs using PowerShell, with manual decoding and fallback."""
    global _UWP_CACHE
    if _UWP_CACHE is not None and not force_refresh:
        return _UWP_CACHE

    try:

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
            print("'Get-StartApps' returned nothing. Trying Get-AppxPackage...")

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
            print("PowerShell did not return any UWP apps.")
            _UWP_CACHE = {}
            return {}

        uwp_apps = {}
        for line in output.splitlines():
            if "::" in line:
                name, appid = line.split("::", 1)
                uwp_apps[name.lower().strip()] = appid.strip()

        print(f"Found {len(uwp_apps)} UWP apps.")
        _UWP_CACHE = uwp_apps
        return uwp_apps

    except Exception as e:
        print(f"Could not scan UWP apps: {e}")
        _UWP_CACHE = {}
        return {}
