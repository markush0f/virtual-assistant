from assistant.core.generate_actions_json import load_all_actions
from assistant.decorators.actions_registry import ACTIONS, execute_action
from assistant.utils.app_manager import app_manager
from assistant.core.ia.ai_core import AICore
from assistant.speech import listen, speak


def bootstrap() -> AICore:
    """Initialize actions, cache apps and return the AI core."""
    print("Virtual Assistant - Modo voz")
    print("Modelo activo: mistral:7b-instruct")
    print("Iniciando entorno...\n")

    print("Cargando modulos de acciones...")
    load_all_actions()
    print(f"{len(ACTIONS)} acciones registradas.\n")

    try:
        app_data = app_manager.export_apps_to_json()
        total = len(app_data.get("desktop_apps", [])) + len(
            app_data.get("uwp_apps", [])
        )
        print(f"[info] Cache de apps actualizada ({total} apps detectadas)\n")
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] No se pudo escanear aplicaciones: {exc}\n")

    ai = AICore()
    return ai


def run_voice_loop(ai: AICore) -> None:
    """Main voice loop to listen, interpret and execute actions."""
    speak("Asistente listo. Di tu comando o di salir para terminar.")

    while True:
        print("\n--- Esperando comando de voz ---")
        user_input = listen().strip()

        if not user_input:
            speak("No se entendio el audio. Intenta de nuevo.")
            continue

        normalized = user_input.lower()
        if normalized in {"exit", "salir", "quit"}:
            speak("Saliendo del asistente de voz.")
            break

        response = ai.ask(user_input)

        if isinstance(response, dict):
            intent = response.get("intent")

            if intent == "error":
                speak(f"Error: {response.get('message')}")
                continue

            if intent == "text":
                speak(str(response.get("response", "")))
                continue

            if intent in ACTIONS:
                print(f"[accion] Ejecutando: {intent}")
                kwargs = {k: v for k, v in response.items() if k != "intent"}
                execute_action(intent, **kwargs)
                continue

            speak(f"No tengo registrada la accion {intent}.")
        else:
            speak(str(response))


def main() -> None:
    ai = bootstrap()
    run_voice_loop(ai)


if __name__ == "__main__":
    main()
