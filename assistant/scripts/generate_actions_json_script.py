from pathlib import Path
from assistant.core.generate_actions_json import export_actions_to_json, load_all_actions
from assistant.decorators.actions_registry import ACTIONS


if __name__ == "__main__":
    load_all_actions()
    export_actions_to_json()
