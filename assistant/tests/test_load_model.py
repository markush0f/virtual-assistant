from assistant.core.ia.ai_core import AICore


ai = AICore()

print("Local model started. Type 'salir' to exit.\n")
print("Model:", ai.model_name)
while True:
    text = input("Prompt: ")
    if text.lower() == "salir":
        break

    response = ai.ask(text)
    print("Model output:", response)
