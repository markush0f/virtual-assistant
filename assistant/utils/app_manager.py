"""
Gestor de aplicaciones que permite detectar y abrir automáticamente
programas instalados en Windows utilizando sus accesos directos.
"""

import glob
import os
from rapidfuzz import process 

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"),
]


def scan_apps():
    """Escanea accesos directos (.lnk) del menú inicio y devuelve un diccionario."""
    apps = {}
    for base_path in START_MENU_PATHS:
        if os.path.exists(base_path):
            for file in glob.glob(base_path + "/**/*.lnk", recursive=True):
                app_name = os.path.basename(file).replace(".lnk", "").lower()
                apps[app_name] = file
    return apps


def open_app(app_name: str, apps_dict: dict):
    """Abre una aplicación si el nombre coincide exactamente."""
    app_name = app_name.lower().strip()
    if app_name in apps_dict:
        os.startfile(apps_dict[app_name])
        print(f"✅ Abriendo {app_name}")
        return True
    else:
        return False


def open_app_fuzzy(app_name: str, apps_dict: dict, threshold: int = 60):
    """
    Busca las 3 aplicaciones más parecidas y deja al usuario elegir.
    - app_name: nombre escrito por el usuario
    - apps_dict: diccionario de apps detectadas
    - threshold: porcentaje mínimo de similitud aceptado (0-100)
    """
    app_name = app_name.lower().strip()
    if not apps_dict:
        print("⚠️ No hay aplicaciones detectadas")
        return False

    # Buscar las 3 coincidencias más cercanas
    matches = process.extract(app_name, apps_dict.keys(), limit=3)

    if not matches or matches[0][1] < threshold:
        print("No se encontró ninguna aplicación con un nombre parecido")
        return False

    print("\n🔍 Coincidencias encontradas:")
    for i, (match, score, _) in enumerate(matches, start=1):
        print(f"{i}. {match} ({score:.1f}%)")

    try:
        choice = int(input("\nElige una aplicación (1-3): "))
        if 1 <= choice <= len(matches):
            selected_app = matches[choice - 1][0]
            os.startfile(apps_dict[selected_app])
            print(f"✅ Abriendo '{selected_app}'")
            return True
    except ValueError:
        print("Entrada no válida")

    return False


if __name__ == "__main__":
    apps = scan_apps()
    print("📂 Aplicaciones detectadas:")
    for app in apps.keys():
        print("-", app)

    choice = input("\nEscribe el nombre de una app a abrir: ").lower()
    
    if not open_app(choice, apps):  
        open_app_fuzzy(choice, apps)  
