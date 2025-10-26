import psutil
import platform
import math


def list_processes(limit=10):
    """List running processes."""
    print("Listing running processes:")
    for proc in psutil.process_iter(["pid", "name"]):
        print(f"{proc.info['pid']} - {proc.info['name']}")
        limit -= 1
        if limit == 0:
            break


def kill_process(name: str):
    """Kill a process by partial name."""
    name = name.lower()
    for proc in psutil.process_iter(["pid", "name"]):
        if name in proc.info["name"].lower():
            psutil.Process(proc.info["pid"]).terminate()
            print(f"❌ Killed {proc.info['name']}")
            return
    print("Process not found.")


def get_system_info():
    """Return system information."""
    info = {
        "os": platform.system(),
        "version": platform.version(),
        "cpu_usage": psutil.cpu_percent(),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
    }
    print(f"💽 System info: {info}")
    return info


def calculate(expression: str):
    """Safely evaluate a math expression."""
    allowed = {"__builtins__": None, "math": math}
    try:
        result = eval(expression, allowed, {})
        print(f"🧮 {expression} = {result}")
        return result
    except Exception:
        print("⚠️ Invalid expression.")
        return None
