ACTIONS = {}


def register_action(type="safe", description=""):
    """
    Decorator to register an assistant action automatically.
    - type: safe | developer | dangerous
    - description: short explanation
    """

    def wrapper(func):
        ACTIONS[func.__name__] = {
            "type": type,
            "description": description or func.__doc__,
            "module": func.__module__,
            "function": func.__name__,
            "callable": func,  # reference to actual function
        }
        return func

    return wrapper


def list_actions():
    """List all registered actions."""
    for name, meta in ACTIONS.items():
        print(f"{name} → {meta['module']} ({meta['type']})")


def execute_action(name: str, **kwargs):
    """Execute a registered action by name."""
    if name not in ACTIONS:
        print(f"Unknown action: {name}")
        return
    action = ACTIONS[name]
    func = action["callable"]

    # Get only parameters required by the function
    func_params = func.__code__.co_varnames[: func.__code__.co_argcount]
    args = {k: v for k, v in kwargs.items() if k in func_params}

    print(f"Executing: {name} | Params: {args}")
    return func(**args)
