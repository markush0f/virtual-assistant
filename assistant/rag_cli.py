from assistant.core.ia.ai_core import AICore

def main():
    print("RAG CLI Assistant (Ollama Local)")
    print("Modelo activo: mistral:7b-instruct")
    print("Escribe tu pregunta o 'exit' para salir.\n")

    ai = AICore()

    while True:
        user_input = input("Pregunta: ").strip()
        if user_input.lower() in ["exit", "salir", "quit"]:
            print(" Saliendo del asistente RAG.")
            break
        response = ai.ask(user_input)

        if isinstance(response, dict):
            if "intent" in response:
                print(f"\nIntent detectado: {response.get('intent')}")
                if "target" in response:
                    print(f"Target: {response.get('target')}")
            elif "response" in response:
                print(f"\nRespuesta: {response.get('response')}")
            elif "message" in response:
                print(f"\nError: {response.get('message')}")
        else:
            print(f"\n{response}")

        print() 


if __name__ == "__main__":
    main()
