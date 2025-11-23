# 🤖 Virtual Assistant (RAG + Voice)

Local desktop assistant with AI, voice recognition, and system action execution. It allows opening applications, controlling volume, performing web searches, running system operations, or browsing the internet through text or voice commands.

Built with Python, Ollama (Mistral 7B), Fast RAG logic, and voice control using speech_recognition and pyttsx3.

---

## 🚀 Main Features

* Local LLM model (Mistral 7B) to interpret natural instructions.
* Execution of registered actions (open apps, volume, searches, etc.).
* Interactive voice mode (press Ctrl + L to talk).
* Spoken responses with pyttsx3.
* Automatic application scanning (.lnk + UWP).
* Modular action system with decorators and dynamic registry.
* Automatic export of actions to JSON.
* Lightweight and extensible CLI.

---

## ⚙️ Installation

1. Clone the repository:
   git clone https://github.com/markush0f/virtual-assistant.git
   cd virtual-assistant

2. Create virtual environment:
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows

3. Install dependencies:
   pip install -r requirements.txt

4. Install Ollama and pull the model:
   ollama pull mistral:7b-instruct (or other model)

---

## 🧩 Usage

### CLI

python -m assistant.core.cli.assistant_cli

Examples:
open spotify
search google artificial intelligence
volume up
open calculator

### Voice Mode

python -m assistant.assistant_voice  
Press Ctrl + L to activate the microphone.

---

## 🗂️ Available Actions

System: volume_up, volume_down, mute_toggle, take_screenshot  
Browser: search_google, open_gmail, read_news  
Multimedia: open_spotify_song, search_youtube  
Apps: open_app, close_app  

---

## 🧾 Generate Actions JSON

python -m assistant.core.generate_actions_json

---

## 🧪 Tests

pytest

---

## 💡 Future Improvements

External API integrations  
Plugin system  
Neural voices  
Multi-language  
Persistent memory  

---

