# Virtual Assistant (RAG + Voice)

Local desktop assistant that runs with a local LLM (Ollama), understands speech, replies via TTS, and executes registered actions (open apps, volume, searches, etc.) through text or voice.

---

## Features

- Local model (Mistral 7B on Ollama) to interpret commands.
- Actions registered via decorators and loaded dynamically.
- Automatic app scan (.lnk and UWP) to open by name.
- Voice mode with `speech_recognition` (microphone) and spoken replies via `pyttsx3`.
- Lightweight CLI for text interaction.
- Automatic export of actions to JSON for internal use.

---

## Installation

1) Clone and enter the project:
```bash
git clone https://github.com/markush0f/virtual-assistant.git
cd virtual-assistant
```

2) Create a virtual environment:
```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3) Install dependencies:
```bash
pip install -r requirements.txt
```

4) Install Ollama and pull the model:
```bash
ollama pull mistral:7b-instruct
```

---

## Usage

### CLI (text)
```bash
python -m assistant.core.cli.assistant_cli
```
Examples: `open spotify`, `search google artificial intelligence`, `volume up`, `open calculator`.

### Voice mode
```bash
python main.py
```
Speak your command; say "salir" or "exit" to quit. Requires a microphone and audio permissions.

---

## Available actions

Loaded from `assistant/core/executor/actions`. Common examples:
- System: `volume_up`, `volume_down`, `mute_toggle`, `take_screenshot`
- Browser: `search_google`, `open_gmail`, `read_news`
- Multimedia: `open_spotify_song`, `search_youtube`
- Apps: `open_app`, `close_app`

---

## Regenerate actions JSON
```bash
python -m assistant.core.generate_actions_json
```

---

## Tests
```bash
pytest
```

---

## Next improvements

External integrations, plugin system, neural voices, multi-language, and persistent memory.
