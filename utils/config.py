from typing import Dict, Any

class ConfigManager:
    def __init__(self) -> None:
        self.settings: Dict[str, Any] = {
            "update_interval": 1.0,
            "theme": "blue",
            "appearance": "System"
        }

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
