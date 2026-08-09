import importlib
import os


class SystemCheck:
    """Run lightweight checks required before starting the world runtime."""

    CORE_MODULES = (
        "backend.core.world_loader",
        "backend.core.retriever",
        "backend.core.state_manager",
        "backend.core.context_builder",
        "backend.core.prompt_builder",
        "backend.core.player_runtime",
        "backend.core.world_runtime",
        "backend.core.world_controller",
    )

    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        self.world_dir = os.path.join(self.project_root, "world")
        self.memory_dir = os.path.join(self.project_root, "memory")
        self.env_file = os.path.join(self.project_root, ".env")

    def _check_world(self):
        return os.path.isdir(self.world_dir)

    def _check_memory(self):
        try:
            os.makedirs(self.memory_dir, exist_ok=True)
            probe = os.path.join(self.memory_dir, ".system_check")
            with open(probe, "w", encoding="utf-8") as file:
                file.write("ok")
            os.remove(probe)
            return True
        except (OSError, IOError):
            return False

    def _env_value(self, key):
        value = os.environ.get(key, "").strip()
        if value:
            return value

        if not os.path.exists(self.env_file):
            return ""

        try:
            with open(self.env_file, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    name, env_value = line.split("=", 1)
                    if name.strip() == key:
                        return env_value.strip().strip("\"'")
        except (OSError, IOError):
            return ""

        return ""

    def _check_llm_config(self):
        return bool(self._env_value("OPENAI_API_KEY"))

    def _check_core_imports(self):
        try:
            for module_name in self.CORE_MODULES:
                importlib.import_module(module_name)
        except (ImportError, ModuleNotFoundError):
            return False
        return True

    def run(self):
        checks = {
            "world": self._check_world(),
            "memory": self._check_memory(),
            "llm": self._check_llm_config(),
            "imports": self._check_core_imports(),
        }
        return {
            "status": "ok" if all(checks.values()) else "error",
            "checks": checks,
        }

    def check(self):
        return self.run()
