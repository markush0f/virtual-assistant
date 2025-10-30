import keyboard
from threading import Thread

class HotkeyListener:
    """Listens for Ctrl+L hotkey to trigger voice recognition."""

    def __init__(self, on_hotkey):
        self.on_hotkey = on_hotkey
        self.listener_thread = Thread(target=self._listen, daemon=True)

    def _listen(self):
        print("⌨️ Voice mode ready — press Ctrl + L to speak.")
        keyboard.add_hotkey("ctrl+l", self.on_hotkey)
        keyboard.wait()  # keeps thread alive

    def start(self):
        self.listener_thread.start()
