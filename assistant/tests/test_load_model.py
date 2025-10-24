from assistant.core.ia.ai_core import AICore


ai = AICore()

print("IA local iniciada. Escribe 'salir' para terminar.\n")
print("Modelo utilizado:", ai.model_name)
while True:
    text = input("Tú: ")
    if text.lower() == "salir":
        break

    response = ai.ask(text)
    print("Interpretación del modelo:", response)
