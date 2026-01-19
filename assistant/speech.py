import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 175)  # speech rate
engine.setProperty("volume", 1.0)


def speak(text: str):
    """Speak text aloud."""
    print(f"[speak] {text}")
    engine.say(text)
    engine.runAndWait()


def listen() -> str:
    """Listen from microphone and return recognized text in Spanish."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[listening] Escuchando...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print(f"Escuchado: {text}")
        return text
    except sr.UnknownValueError:
        print("No se entendio el audio.")
        return ""
    except sr.RequestError:
        print("Error con el servicio de reconocimiento.")
        return ""
