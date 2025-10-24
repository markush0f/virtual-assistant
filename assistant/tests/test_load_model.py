from assistant.core.ia.ai_core import AICore


ai = AICore("deepseek-r1")

print("IA local iniciada. Escribe 'salir' para terminar.\n")

while True:
    text = input("Tú: ")
    if text.lower() == "salir":
        break

    response = ai.ask(text)
    print("Interpretación del modelo:", response)
