import json
import subprocess
from pathlib import Path
from assistant.core.ia.load_model import ModelLoader


class AICore:
    def __init__(self):
        loader = ModelLoader()
        loader.load_model("mistral:7b-instruct")
        self.model_name = loader.get_active_model()

    def _load_actions_description(self) -> str:
        """Read all available actions dynamically from assistant/common."""
        try:
            # Detect the project root dynamically (the folder that contains 'assistant/')
            current_file = Path(__file__).resolve()
            project_root = next(
                (
                    p
                    for p in current_file.parents
                    if (p / "assistant" / "common").exists()
                ),
                None,
            )

            if not project_root:
                print("⚠️ Could not locate project root containing 'assistant/common'")
                return "No actions available."

            common_dir = project_root / "assistant" / "common"

            # Look for any JSON containing "actions" in the name
            possible_files = list(common_dir.glob("actions*.json"))
            if not possible_files:
                print(f"⚠️ No action configuration files found in {common_dir}")
                return "No actions available."

            # Prefer actions_config.json if present
            config_path = next(
                (f for f in possible_files if "actions_config" in f.name),
                possible_files[0],
            )

            print(f"📂 Using actions file: {config_path}")

            with open(config_path, "r", encoding="utf-8") as f:
                actions = json.load(f)

            actions_text = "\n".join(
                f"- {name}: {info.get('description', 'No description')}"
                for name, info in actions.items()
                if name != "actions_description"
            )

            # print("\n✅ Loaded actions:\n", actions_text, "\n")
            return actions_text or "No actions available."

        except Exception as e:
            print(f"⚠️ Error while loading actions: {e}")
            return "No actions available."

    def ask(self, prompt: str) -> dict:
        try:
            available_actions = self._load_actions_description()
            system_prompt = f"""
You are a local virtual assistant that executes commands through registered actions.

You have access to the following actions:
{available_actions}

Behavior rules:
1. Respond ONLY with a JSON object if the input matches one of these actions.
   Example:
   "open spotify" -> {{"intent": "open_app", "target": "spotify"}}
   "search AI news on google" -> {{"intent": "search_google", "query": "AI news"}}
2. If the user says something unrelated to an action, reply concisely (max 10 words) in the same language.
3. Never explain, never reason, never use markdown.
Important:
Always reply using a JSON object with the key name "intent".
Never use "action", "command" or "task" instead of "intent".
User:
"""
            full_prompt = f"{system_prompt}\n{prompt}"

            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=full_prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore",
            )

            raw_output = result.stdout.strip()
            if not raw_output:
                raw_output = "No response from model."

            print(f"\nRAW MODEL OUTPUT:\n{raw_output}\n")

            json_start = raw_output.find("{")
            json_end = raw_output.rfind("}")
            if json_start != -1 and json_end != -1:
                json_str = raw_output[json_start : json_end + 1]
                data = json.loads(json_str)

                if "intent" not in data and len(data) > 0:
                    first_key = next(iter(data))
                    data["intent"] = data.pop(first_key)

                if "intent" not in data:
                    data["intent"] = None

                return data

            return {"intent": "text", "response": raw_output}

        except Exception as e:
                return {"intent": "error", "message": str(e)}
