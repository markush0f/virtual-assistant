import inspect

# Global dictionary to store all actions
ACTIONS = {}

def register_action(description="", type="safe"):
    """
    Decorator to register assistant actions dynamically.
    Usage:
    @register_action(description="Opens an app")
    def open_app(target: str): ...
    """
    def decorator(func):
        ACTIONS[func.__name__] = {
            "description": description,
            "type": type,
            "function": func.__name__,
            "module": func.__module__,
            "callable": func,
        }
        # print(f"Registered action: {func.__name__}")
        return func
    return decorator


def execute_action(action_name: str, **args):
    """Execute a registered action by name."""
    action = ACTIONS.get(action_name)
    if not action:
        print(f"Action '{action_name}' not found.")
        return None

    func = action["callable"]
    print(f"Executing: {action_name} | Params: {args}")
    return func(**args)
