import importlib
import pkgutil
from pathlib import Path


def load_all_actions():
    """Auto-import all modules in the actions folder."""
    actions_path = Path(__file__).parent / "actions"
    for _, module_name, _ in pkgutil.iter_modules([str(actions_path)]):
        importlib.import_module(f"actions.{module_name}")
    print("All action modules loaded.")
