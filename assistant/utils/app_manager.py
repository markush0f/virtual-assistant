import os
import glob

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
]


def scan_apps():
    """Scan Start Menu folders and return a dict of app_name -> path."""
    apps = {}
    for base_path in START_MENU_PATHS:
        if os.path.exists(base_path):
            for file in glob.glob(base_path + "/**/*.lnk", recursive=True):
                app_name = os.path.basename(file).replace(".lnk", "").lower()
                apps[app_name] = file
    return apps


def open_app(app_name: str, apps_dict: dict):
    """Open app by name using the scanned dictionary."""
    app_name = app_name.lower().strip()
    if app_name in apps_dict:
        os.startfile(apps_dict[app_name])  
        return True
    else:
        return False


if __name__ == "__main__":
    apps = scan_apps()
    print("Aplicaciones detectadas:")
    for app in apps.keys():  
        print("-", app)

    # Ejemplo de prueba
    choice = input("\nEscribe el nombre de una app a abrir: ").lower()
    if open_app(choice, apps):
        print(f"Abriendo {choice}...")
    else:
        print(f"No encontré {choice}.")
