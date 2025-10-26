"""
Acts as a router that dispatches intents to their corresponding action modules.
"""

import json
import os
from importlib import import_module


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
        """Route the intent to its corresponding action module and function."""
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

        module_name = action_info["module"]
        func_name = action_info["function"]

        try:
            # dynamic import
            module = import_module(f"assistant.core.executor.actions.{module_name}")
            func = getattr(module, func_name)

            # determine which argument to pass
            args = []
            if "command" in action_info["params"]:
                args.append(command)
            elif "target" in action_info["params"]:
                args.append(target)

            # execute the function
            return func(*args)
        except Exception as e:
            return f"Error executing {intent}: {e}"
