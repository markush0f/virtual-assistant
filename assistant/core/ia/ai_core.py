import json
import subprocess
from assistant.core.ia.load_model import ModelLoader


class AICore:
    def __init__(self):
        loader = ModelLoader()
        loader.load_model("mistral:7b-instruct")
        self.model_name = loader.get_active_model()

    def ask(self, prompt: str) -> dict:
        """
        Sends the user input directly to Ollama (non-blocking version).
        Uses the same instruction-tuned system prompt as before.
        """
        try:
            system_prompt = """
You are a local command interpreter assistant.

Behavior rules:
1. Respond SHORT and DIRECT.
2. If the input is a command, reply ONLY with a JSON object.
   Examples:
   "open spotify" -> {"intent": "open_app", "target": "spotify"}
   "close chrome" -> {"intent": "close_app", "target": "chrome"}
   "increase volume" -> {"intent": "volume_up"}
   "decrease volume" -> {"intent": "volume_down"}
3. If the input is not a command, reply briefly (max 10 words) in the same language.
4. Never explain, reason, or output markdown.
User:
"""
            full_prompt = f"{system_prompt}\n{prompt}"

            # Launch Ollama process (streaming, non-blocking)
            process = subprocess.Popen(
                ["ollama", "run", self.model_name],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            # Send the prompt and close input stream
            stdout_data, stderr_data = process.communicate(full_prompt)

            raw_output = (stdout_data or "").strip()
            if not raw_output:
                raw_output = "No response from model."

            print(f"\nRAW MODEL OUTPUT:\n{raw_output}\n")

            # Try extracting JSON
            json_start = raw_output.find("{")
            json_end = raw_output.rfind("}")
            if json_start != -1 and json_end != -1:
                json_str = raw_output[json_start : json_end + 1]
                return json.loads(json_str)

            return {"intent": "text", "response": raw_output}

        except Exception as e:
            return {"intent": "error", "message": str(e)}

