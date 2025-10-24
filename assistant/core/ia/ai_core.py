import json
import subprocess


class AICore:
    def __init__(self, model_name: str = "deepseek-r1"):
        self.model_name = model_name

    def ask(self, prompt: str) -> dict:
        """
        Sends a text prompt to the local model using Ollama subprocess.
        Returns a structured JSON (intent + target) if found.

        Args:
            prompt (str): prompt to send to the model.

        Returns:
            str: Response from the model.
        """
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",  
                errors="ignore", 
            )
            raw_output = result.stdout.strip()
            print(f"\nRAW MODEL OUTPUT:\n{raw_output}\n")

            json_start = raw_output.find("{")
            json_end = raw_output.rfind("}")
            if json_start != -1 and json_end != -1:
                json_str = raw_output[json_start : json_end + 1]
                return json.loads(json_str)

            return {"intent": "unknown", "raw_output": raw_output}

        except Exception as e:
            print(f"Error communicating with the model: {e}")
            return {"intent": "error", "message": str(e)}
