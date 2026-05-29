import psutil
from typing import Dict, Any

class SystemInfo:
    def get_system_metrics(self) -> Dict[str, Any]:
        cpu_percent: float = psutil.cpu_percent(interval=None)
        memory_info: Any = psutil.virtual_memory()
        disk_info: Any = psutil.disk_usage('/')
        
        metrics: Dict[str, Any] = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
            "disk_percent": disk_info.percent
        }
        return metrics
