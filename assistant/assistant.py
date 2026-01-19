import importlib
import pkgutil
from pathlib import Path
from assistant.decorators.actions_registry import ACTIONS, execute_action, list_actions
from assistant.core.generate_actions_json import export_actions_to_json, load_all_actions


def initialize_actions():
    """Load all actions and generate JSON automatically."""
    load_all_actions()
    export_actions_to_json()
    print("\nActions JSON regenerated automatically.\n")


def main():
    """CLI test mode for the assistant."""
    initialize_actions()  # regenerate JSON here

    print("Virtual Assistant Ready!")
    print("Type 'list' to see all actions or 'exit' to quit.\n")

    while True:
        user_input = input("Command: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Bye!")
            break

        if user_input.lower() == "list":
            list_actions()
            print()
            continue

        if user_input in ACTIONS:
            func = ACTIONS[user_input]["callable"]
            params = func.__code__.co_varnames[: func.__code__.co_argcount]

            kwargs = {}
            for param in params:
                if param != "self":
                    value = input(f"Enter value for '{param}': ")
                    kwargs[param] = value

            execute_action(user_input, **kwargs)
        else:
            print("Unknown command. Type 'list' to see available actions.\n")


if __name__ == "__main__":
    main()
