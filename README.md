# Virtual Assistant (RAG + Voice)

Assistant for Windows that runs locally with Ollama or via OpenAI, understands voice, replies with TTS, and executes registered actions (open apps, control volume, web searches, etc.) through text or voice. Includes a GUI to pick provider/model and launch the assistant.

---

## Highlights
- Local model (Ollama, default `mistral:7b-instruct`) or OpenAI chat models.
- Voice loop with `speech_recognition` + `pyttsx3`.
- Automatic app scan (.lnk and UWP) to open by name.
- Dynamic action registry (decorators) exported to JSON.
- GUI configurator to select provider/model/API key and start CLI or voice.

---

## Requirements
- Python 3.11+
- Windows (pycaw, PowerShell scan of Start Menu).
- Ollama installed for local mode.
- Microphone for voice mode.
- For OpenAI: API key and `openai` dependency (already in `requirements.txt`).

---

## Setup
```bash
git clone https://github.com/markush0f/virtual-assistant.git
cd virtual-assistant
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
# If using local mode: ollama pull mistral:7b-instruct
```

---

## Usage

### GUI configurator (provider + launcher)
```bash
python assistant/gui/configurator.py
```
- Pick provider (`local` or `openai`), model, and API key (if OpenAI).
- Save config (stored in `assistant/common/settings.db`).
- Launch CLI or Voice from the buttons.

To build a Windows exe of the GUI:
```bash
pyinstaller --noconsole --onefile --collect-all assistant --paths . assistant/gui/configurator.py
# run dist\configurator.exe
```

### CLI (text)
```bash
python -m assistant.core.cli.assistant_cli
```
Examples: `open spotify`, `search google artificial intelligence`, `volume up`, `open calculator`.

### Voice mode
```bash
python main.py
```
Speak your command; say "salir"/"exit" to quit.

---

## Provider selection (code)
Default is local Ollama. To switch:
```python
from assistant.core.ia.provider_store import set_provider_config
set_provider_config("openai", "gpt-4o-mini", api_key="YOUR_OPENAI_KEY")
set_provider_config("local", "mistral:7b-instruct")
```

---

## Actions
Actions live in `assistant/core/executor/actions`. Examples:
- System: `volume_up`, `volume_down`, `mute_toggle`, `take_screenshot`
- Browser: `search_google`, `open_gmail`, `read_news`
- Multimedia: `open_spotify_song`, `search_youtube`
- Apps: `open_app`, `close_app`

Regenerate actions JSON:
```bash
python -m assistant.core.generate_actions_json
```

---

## Tests
```bash
pytest
```

---

## Notes
- Settings persist in SQLite at `assistant/common/settings.db`.
- Voice mode needs microphone permissions.
- Keep Ollama running/installed for local provider. For OpenAI, ensure internet access and a valid API key.
