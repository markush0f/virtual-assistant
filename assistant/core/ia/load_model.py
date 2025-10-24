"""
load_model.py
----------------
Handles loading and configuration of local LLM models through Ollama.
This module centralizes model selection, configuration, and validation.
"""

import subprocess
import json
from pathlib import Path


class ModelLoader:
    def __init__(self, config_path: str | None = None):
        """
        Initialize the model loader.
        Args:
            config_path (str): Optional path to a JSON config file (default = models/config.json)
        """
        default_path = Path(__file__).parent.parent.parent / "system" / "config.py"
        self.config_path = config_path or default_path
        self.active_model = None

    def _check_ollama_installed(self) -> bool:
        """Checks if Ollama CLI is installed and accessible."""
        try:
            subprocess.run(
                ["ollama", "--version"], capture_output=True, text=True, check=True
            )
            return True
        except Exception:
            print("Ollama is not installed or not in PATH.")
            return False

    def list_local_models(self) -> list[str]:
        """Returns a list of locally available models."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            return models
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

    def load_model(self, model_name: str) -> bool:
        """
        Loads a model by name and validates it.
        Returns True if the model is ready to use.
        """
        if not self._check_ollama_installed():
            return False

        available = self.list_local_models()
        if model_name not in available:
            print(f"Model '{model_name}' not found locally. Pulling from Ollama...")
            try:
                subprocess.run(["ollama", "pull", model_name], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to pull model '{model_name}' from Ollama.")
                return False

        self.active_model = model_name
        print(f"Model '{model_name}' successfully loaded and ready.")
        return True

    def get_active_model(self) -> str | None:
        """Returns the currently active model name."""
        return self.active_model

    def validate_model(self) -> bool:
        """Runs a simple check to confirm the model responds correctly."""
        if not self.active_model:
            print("No model is currently loaded.")
            return False

        print(f"Testing model '{self.active_model}'...")
        try:
            test_prompt = "Say 'ok' if you are ready."
            result = subprocess.run(
                ["ollama", "run", self.active_model],
                input=test_prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            output = result.stdout.strip().lower()
            if "ok" in output:
                print("Model test passed.")
                return True
            print("Model did not respond correctly.")
            return False
        except Exception as e:
            print(f"Error validating model: {e}")
            return False
