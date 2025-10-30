from assistant.core.ia.ai_core import AICore
from assistant.decorators.actions_registry import ACTIONS, execute_action
from assistant.core.voice.speech_recognition import SpeechRecognizer
from assistant.core.voice.text_to_speech import TextToSpeech
from assistant.core.voice.hotkey_listener import HotkeyListener
import platform
import winsound
from pathlib import Path

# PASS TO OTHER MODULE
# -------------------------------------------------
try:
    from playsound import playsound
except ImportError:
    playsound = None


def play_beep():
    """Play a short beep when listening starts."""
    system = platform.system()
    if system == "Windows":
        winsound.Beep(800, 180)
    else:
        sound_file = Path(__file__).parent / "beep.wav"
        if playsound and sound_file.exists():
            playsound(str(sound_file))


# -------------------------------------------------


class VoiceAssistant:
    """Voice-based AI assistant that listens and talks."""

    def __init__(self):
        self.ai = AICore()
        self.speech = SpeechRecognizer()
        self.tts = TextToSpeech()

    def handle_voice_command(self):
        """Triggered when Ctrl+L is pressed."""
        play_beep()
        text = self.speech.listen()
        if not text:
            self.tts.say("No te he entendido.")
            return

        response = self.ai.ask(text)

        if not isinstance(response, dict):
            self.tts.say(response)
            return

        intent = response.get("intent")
        if not intent:
            self.tts.say("No entendí la acción.")
            return

        if intent in ACTIONS:
            self.tts.say(f"Ejecutando {intent.replace('_', ' ')}.")
            kwargs = {k: v for k, v in response.items() if k != "intent"}
            execute_action(intent, **kwargs)
        else:
            self.tts.say("Esa acción no está registrada.")

    def start(self):
        """Start voice assistant."""
        hotkey = HotkeyListener(self.handle_voice_command)
        hotkey.start()
        self.tts.say("Asistente de voz activado. Pulsa Control más L para hablar.")
        print("🎧 Voice assistant running. Press Ctrl + L to speak.")
        while True:
            pass  # keep alive
