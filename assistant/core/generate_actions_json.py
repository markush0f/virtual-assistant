import importlib
import inspect
import json
import pkgutil
from pathlib import Path
from assistant.decorators.actions_registry import ACTIONS


def load_all_actions() -> None:
    """Import all Python modules inside assistant/core/executor/actions."""
    actions_path = Path(__file__).parent / "executor" / "actions"

    for _, module_name, _ in pkgutil.iter_modules([str(actions_path)]):
        full_module_name = f"assistant.core.executor.actions.{module_name}"
        try:
            importlib.import_module(full_module_name)
        except Exception as e:  # noqa: BLE001
            print(f"Could not import {module_name}: {e}")

    print("All action modules loaded.")


def export_actions_to_json(output_file: str | None = None) -> None:
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

    output_file = output_file or str(Path(__file__).parent.parent / "common" / "actions_config.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(actions_data, f, indent=4, ensure_ascii=False)

    print(f"Actions exported to {output_file} ({len(actions_data)} total)\n")


if __name__ == "__main__":
    load_all_actions()
    export_actions_to_json()
