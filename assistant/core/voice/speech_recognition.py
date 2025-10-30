import speech_recognition as sr


class SpeechRecognizer:
    """Handles microphone input and speech-to-text conversion."""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout=5, phrase_time_limit=8) -> str | None:
        """Capture voice input and return recognized text."""
        with self.microphone as source:
            print("🎙️ Listening... (speak now)")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                text = self.recognizer.recognize_google(audio, language="es-ES")
                print(f"🗣️ You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("⏱️ No speech detected.")
            except sr.UnknownValueError:
                print("⚠️ Could not understand the audio.")
            except sr.RequestError:
                print("❌ Speech recognition service unavailable.")
        return None
