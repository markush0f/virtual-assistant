import sys
import subprocess
from pathlib import Path
import customtkinter as ctk

DEBUG_MODE = False  # True only for development


def _ensure_repo_path():
    if getattr(sys, "frozen", False):
        return
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


_ensure_repo_path()

from assistant.core.ia.provider_store import get_provider_config, set_provider_config


PROVIDER_MODELS = {
    "local": ["mistral:7b-instruct", "llama3:8b-instruct", "phi-3-mini"],
    "openai": ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
}


# ============================================================
# PROCESS MANAGER (ROBUST WINDOWS VERSION)
# ============================================================


class ProcessManager:
    def __init__(self):
        self.process: subprocess.Popen | None = None

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self, cmd: list[str]):
        if self.is_running():
            raise RuntimeError("Assistant already running")

        flags = (
            subprocess.CREATE_NEW_CONSOLE if DEBUG_MODE else subprocess.CREATE_NO_WINDOW
        )

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=flags,
        )

    def stop(self):
        if not self.is_running():
            self.process = None
            return

        pid = self.process.pid

        # 1) Try graceful terminate
        try:
            self.process.terminate()
            self.process.wait(timeout=2)
            self.process = None
            return
        except Exception:
            pass

        # 2) Force kill entire process tree (Windows)
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
                check=False,
            )
        finally:
            self.process = None


# ============================================================
# GUI
# ============================================================


class ConfigApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Virtual Assistant")
        self.geometry("480x400")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.provider_var = ctk.StringVar()
        self.model_var = ctk.StringVar()
        self.api_key_var = ctk.StringVar()
        self.status_var = ctk.StringVar(value="Ready.")

        self.process_manager = ProcessManager()

        self._build_ui()
        self._load_config()
        self._validate_state()

    # ---------------- UI ----------------

    def _build_ui(self):
        pad = {"padx": 16, "pady": 8}

        ctk.CTkLabel(self, text="Provider").grid(row=0, column=0, sticky="w", **pad)
        self.provider_opt = ctk.CTkOptionMenu(
            self,
            variable=self.provider_var,
            values=list(PROVIDER_MODELS.keys()),
            command=self._on_provider_change,
        )
        self.provider_opt.grid(row=0, column=1, sticky="ew", **pad)

        ctk.CTkLabel(self, text="Model").grid(row=1, column=0, sticky="w", **pad)
        self.model_opt = ctk.CTkOptionMenu(
            self,
            variable=self.model_var,
            values=[],
            command=lambda _: self._validate_state(),
        )
        self.model_opt.grid(row=1, column=1, sticky="ew", **pad)

        self.api_label = ctk.CTkLabel(self, text="API Key (OpenAI)")
        self.api_label.grid(row=2, column=0, sticky="w", **pad)

        self.api_entry = ctk.CTkEntry(self, textvariable=self.api_key_var, show="*")
        self.api_entry.grid(row=2, column=1, sticky="ew", **pad)
        self.api_key_var.trace_add("write", lambda *_: self._validate_state())

        self.save_btn = ctk.CTkButton(self, text="Save config", command=self._save)
        self.save_btn.grid(row=3, column=0, sticky="ew", **pad)

        self.toggle_btn = ctk.CTkButton(
            self, text="Start Assistant", command=self._toggle_assistant
        )
        self.toggle_btn.grid(row=3, column=1, sticky="ew", **pad)

        self.status = ctk.CTkLabel(self, textvariable=self.status_var, anchor="w")
        self.status.grid(row=4, column=0, columnspan=2, sticky="ew", padx=16, pady=14)

        self.columnconfigure(1, weight=1)

    # ---------------- CONFIG ----------------

    def _load_config(self):
        cfg = get_provider_config()

        provider = cfg.get("provider", "local")
        self.provider_var.set(provider)
        self._update_models(provider)

        model = cfg.get("model") or PROVIDER_MODELS[provider][0]
        self.model_var.set(model)

        self.api_key_var.set(cfg.get("api_key") or "")
        self._toggle_api_field()
        self.status_var.set("Config loaded.")

    def _save(self):
        try:
            set_provider_config(
                provider=self.provider_var.get(),
                model=self.model_var.get(),
                api_key=self.api_key_var.get().strip() or None,
            )
            self.status_var.set("Configuration saved.")
        except Exception as exc:
            self.status_var.set(f"Save failed: {exc}")

    # ---------------- PROVIDER ----------------

    def _on_provider_change(self, provider: str):
        self._update_models(provider)
        self._toggle_api_field()
        self._validate_state()

    def _update_models(self, provider: str):
        models = PROVIDER_MODELS.get(provider, [])
        self.model_opt.configure(values=models)
        if models:
            self.model_var.set(models[0])

    def _toggle_api_field(self):
        is_openai = self.provider_var.get() == "openai"
        if is_openai:
            self.api_label.grid()
            self.api_entry.grid()
            self.api_entry.configure(state="normal")
        else:
            self.api_entry.delete(0, "end")
            self.api_entry.configure(state="disabled")
            self.api_label.grid_remove()
            self.api_entry.grid_remove()

    def _validate_state(self):
        provider = self.provider_var.get()
        model = self.model_var.get()
        api_key = self.api_key_var.get().strip()

        valid = (
            provider in PROVIDER_MODELS
            and model in PROVIDER_MODELS[provider]
            and (provider != "openai" or api_key)
        )

        self.save_btn.configure(state="normal" if valid else "disabled")
        self.toggle_btn.configure(state="normal" if valid else "disabled")
        self.status_var.set(
            "Configuration valid." if valid else "Invalid configuration."
        )

    # ---------------- START / STOP ----------------

    def _toggle_assistant(self):
        if self.process_manager.is_running():
            self._stop_assistant()
        else:
            self._start_assistant()

    def _start_assistant(self):
        try:
            cmd = self._build_assistant_command()
            self.process_manager.start(cmd)
            self.toggle_btn.configure(text="Stop Assistant")
            self.status_var.set("Assistant running.")
        except Exception as exc:
            self.status_var.set(f"Failed to start assistant: {exc}")

    def _stop_assistant(self):
        self.process_manager.stop()
        self.toggle_btn.configure(text="Start Assistant")
        self.status_var.set("Assistant stopped.")

    def _build_assistant_command(self) -> list[str]:
        # DEV
        if not getattr(sys, "frozen", False):
            project_root = Path(__file__).resolve().parents[2]
            main_path = project_root / "main.py"
            return ["python", str(main_path)]

        # PROD
        exe_dir = Path(sys.executable).parent
        assistant_exe = exe_dir / "AssistantCore.exe"

        if not assistant_exe.exists():
            raise FileNotFoundError(
                "AssistantCore.exe not found next to the GUI executable."
            )

        return [str(assistant_exe)]

    # ---------------- CLOSE ----------------

    def _on_close(self):
        if self.process_manager.is_running():
            self.process_manager.stop()
        self.destroy()


if __name__ == "__main__":
    app = ConfigApp()
    app.mainloop()
