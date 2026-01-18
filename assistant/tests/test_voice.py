"""
Voice repeater test app.
The app repeats what you say until it hears the word "salir".
"""

import speech_recognition as sr
import pyttsx3

# Init recognizer and TTS
recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    """Speak text using system TTS."""
    engine.say(text)
    engine.runAndWait()


def listen():
    """Capture audio and convert to text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No pude entender lo que dijiste"
        except sr.RequestError:
            return "Error con el servicio de reconocimiento"


if __name__ == "__main__":
    print("Dime algo y lo repetire")
    speak("Hola Markus, dime algo y lo repetire")

    while True:
        text = listen()
        print("Tu dijiste:", text)
        speak("Has dicho " + text)

        if "salir" in text.lower():
            speak("Adios")
            break
