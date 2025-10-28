from assistant.core.ia.ai_core import AICore
from assistant.actions_registry import ACTIONS, execute_action
from assistant.generate_actions_json import load_all_actions


def main():
    print("🤖 Virtual Assistant RAG CLI")
    print("Modelo activo: mistral:7b-instruct")
    print("Escribe tu orden o 'exit' para salir.\n")

    # ✅ Cargar todas las acciones registradas al inicio
    load_all_actions()
    print(f"✅ {len(ACTIONS)} acciones cargadas.\n")

    ai = AICore()

    while True:
        user_input = input("❓ Pregunta: ").strip()
        if user_input.lower() in ["exit", "salir", "quit"]:
            print("👋 Saliendo del asistente.")
            break

        response = ai.ask(user_input)

        # --- Si la IA devuelve un intent JSON ---
        if isinstance(response, dict):
            intent = response.get("intent")

            if intent == "error":
                print(f"⚠️ Error: {response.get('message')}\n")
                continue

            # Si es texto normal (no comando)
            if intent == "text":
                print(f"💬 {response.get('response')}\n")
                continue

            # Si es una acción registrada (intent válido)
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
