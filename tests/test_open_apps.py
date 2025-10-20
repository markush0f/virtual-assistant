import os
import webbrowser


def open_youtube():
    webbrowser.open("https://youtube.com")


def open_notepad():
    os.system("notepad")  # Windows


def open_calculator():
    os.system("calc")  # Windows


if __name__ == "__main__":
    print("Probando apertura de apps...")

    print("→ Abriendo YouTube en el navegador")
    open_youtube()

    input("Presiona ENTER para abrir el bloc de notas...")
    open_notepad()

    input("Presiona ENTER para abrir la calculadora...")
    open_calculator()

    print("✅ Prueba terminada")
