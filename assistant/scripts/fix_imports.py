import os

# Pattern to search and replace
ACTIONS_DIR = os.path.join(os.path.dirname(__file__), "core", "executor", "actions")
OLD_IMPORT = "from actions_registry import register_action"
NEW_IMPORT = "from assistant.actions_registry import register_action"


def fix_imports_in_file(filepath: str):
    """Replace old import in a single file if found."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if OLD_IMPORT in content:
        content = content.replace(OLD_IMPORT, NEW_IMPORT)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed import in: {os.path.basename(filepath)}")
    else:
        print(f"No changes in: {os.path.basename(filepath)}")


def main():
    """Iterate over all .py files inside actions folder and fix imports."""
    print(f"Scanning folder: {ACTIONS_DIR}\n")
    for file in os.listdir(ACTIONS_DIR):
        if file.endswith(".py"):
            fix_imports_in_file(os.path.join(ACTIONS_DIR, file))

    print("\nDone! All actions imports are up-to-date.\n")


if __name__ == "__main__":
    main()
