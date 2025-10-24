import json
import os


class IntentExecutor:
    def __init__(self, dev_mode: bool = False):
        self.dev_mode = dev_mode
        self.actions = self._load_actions()

    def _load_actions(self) -> dict:
        """Load actions dynamically from JSON file."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        actions_path = os.path.join(base_dir, "../../common/actions.json")
        try:
            with open(actions_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Could not load actions.json: {e}")
            return {}

    def execute(self, intent_data: dict) -> str:
        intent = intent_data.get("intent")
        target = intent_data.get("target", "")
        command = intent_data.get("command", "")

        if not intent:
            return "No intent provided."

        action_info = self.actions.get(intent)
        if not action_info:
            return f"Unknown intent: {intent}"

        # Developer-only actions
        if action_info["type"] == "developer" and not self.dev_mode:
            return "Developer mode is disabled."

        func_name = action_info["function"]
        if hasattr(self, func_name):
            func = getattr(self, func_name)
            try:
                if "command" in action_info["params"]:
                    return func(command)
                return func(target)
            except Exception as e:
                return f"Error executing {intent}: {e}"
        return f"Function '{func_name}' not implemented."

    def execute_system_command(self, command):
        confirm = (
            input(f"\nExecute system command?\n> {command}\n(y/n): ").strip().lower()
        )
        if confirm.lower() != "y":
            return "Command cancelled."
        os.system(command)
        return "Command executed."
