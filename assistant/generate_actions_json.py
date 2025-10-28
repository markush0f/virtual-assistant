import importlib
import inspect
import json
import pkgutil
from pathlib import Path
from assistant.actions_registry import ACTIONS


def load_all_actions():
    """Import all Python modules inside assistant/core/executor/actions."""
    actions_path = Path(__file__).parent / "core" / "executor" / "actions"
    for _, module_name, _ in pkgutil.iter_modules([str(actions_path)]):
        importlib.import_module(f"assistant.core.executor.actions.{module_name}")
    print("✅ All action modules loaded.")


def export_actions_to_json(output_file="actions_config.json"):
    """Export all registered actions from ACTIONS dict to a JSON file."""
    actions_data = {}
    for name, meta in ACTIONS.items():
        params = list(inspect.signature(meta["callable"]).parameters.keys())
        actions_data[name] = {
            "type": meta["type"],
            "description": meta["description"],
            "module": meta["module"].split(".")[-1],
            "function": meta["function"],
            "params": params,
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(actions_data, f, indent=4, ensure_ascii=False)

    print(f"🧾 Actions exported to {output_file} ({len(actions_data)} total)")


if __name__ == "__main__":
    load_all_actions()
    export_actions_to_json()
