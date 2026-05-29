import threading
import time
from typing import Callable, Dict, Any, List, Optional
from core.system_info import SystemInfo
from core.process_manager import ProcessManager
from core.network_monitor import NetworkMonitor

class DataScheduler:
    def __init__(self, 
                 ui_update_callback: Callable[[Dict[str, Any]], None], 
                 processes_update_callback: Callable[[List[Dict[str, Any]]], None],
                 network_update_callback: Callable[[Dict[str, int]], None],
                 update_interval: float = 1.0) -> None:
        self.sys_info: SystemInfo = SystemInfo()
        self.proc_manager: ProcessManager = ProcessManager()
        self.net_monitor: NetworkMonitor = NetworkMonitor()
        
        self.ui_update_callback: Callable[[Dict[str, Any]], None] = ui_update_callback
        self.processes_update_callback: Callable[[List[Dict[str, Any]]], None] = processes_update_callback
        self.network_update_callback: Callable[[Dict[str, int]], None] = network_update_callback
        
        self.update_interval: float = update_interval
        self._running: bool = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False

    def _loop(self) -> None:
        while self._running:
            metrics: Dict[str, Any] = self.sys_info.get_system_metrics()
            self.ui_update_callback(metrics)
            
            processes: List[Dict[str, Any]] = self.proc_manager.get_processes()
            self.processes_update_callback(processes)
            
            network: Dict[str, int] = self.net_monitor.get_network_metrics()
            self.network_update_callback(network)
            
            time.sleep(self.update_interval)
