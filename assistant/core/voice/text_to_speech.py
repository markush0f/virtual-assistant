import pyttsx3

class TextToSpeech:
    """Converts text to spoken voice output."""

    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)
        self.engine.setProperty("volume", 1.0)
        # Try to pick a Spanish voice if available
        for voice in self.engine.getProperty("voices"):
            if "spanish" in voice.name.lower() or "es" in voice.id.lower():
                self.engine.setProperty("voice", voice.id)
                break

    def say(self, text: str):
        """Speak text aloud."""
        print(f"🗣️ Assistant says: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
