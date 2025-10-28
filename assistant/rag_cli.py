from assistant.core.ia.ai_core import AICore
from assistant.actions_registry import ACTIONS, execute_action
from assistant.generate_actions_json import load_all_actions
from assistant.utils import app_manager


def main():
    print("🤖 Virtual Assistant RAG CLI")
    print("Modelo activo: mistral:7b-instruct")
    print("Inicializando entorno...\n")

    # ✅ 1️⃣ Cargar todas las acciones del sistema
    load_all_actions()
    print(f"✅ {len(ACTIONS)} acciones cargadas.\n")

    # ✅ 2️⃣ Escanear y generar cache de aplicaciones
    try:
        app_data = app_manager.export_apps_to_json()
        total = len(app_data["desktop_apps"]) + len(app_data["uwp_apps"])
        print(f"📁 App cache actualizado ({total} apps detectadas)\n")
    except Exception as e:
        print(f"⚠️ Error al escanear aplicaciones: {e}\n")

    # ✅ 3️⃣ Inicializar el modelo local
    ai = AICore()

    print("🎙️ Escribe una orden (ej. 'open spotify') o 'exit' para salir.\n")

    while True:
        user_input = input("❓ Pregunta: ").strip()
        if user_input.lower() in ["exit", "salir", "quit"]:
            print("👋 Saliendo del asistente.")
            break

        response = ai.ask(user_input)

        # --- Procesar respuesta del modelo ---
        if isinstance(response, dict):
            intent = response.get("intent")

            if intent == "error":
                print(f"⚠️ Error: {response.get('message')}\n")
                continue

            if intent == "text":
                print(f"💬 {response.get('response')}\n")
                continue

            if intent in ACTIONS:
                print(f"⚙️ Ejecutando acción: {intent}")
                kwargs = {k: v for k, v in response.items() if k != "intent"}
                execute_action(intent, **kwargs)
                print()
            else:
                print(f"❓ Acción '{intent}' no registrada.\n")
        else:
            print(f"💬 {response}\n")


if __name__ == "__main__":
    main()
