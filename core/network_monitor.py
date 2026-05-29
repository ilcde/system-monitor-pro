import psutil
import time
from typing import Dict

class NetworkMonitor:
    def __init__(self) -> None:
        self._last_bytes_sent: int = 0
        self._last_bytes_recv: int = 0
        self._last_time: float = time.time()
        self._first_read: bool = True

    def get_network_metrics(self) -> Dict[str, float]:
        io_counters = psutil.net_io_counters()
        current_sent: int = io_counters.bytes_sent
        current_recv: int = io_counters.bytes_recv
        current_time: float = time.time()

        if self._first_read:
            self._last_bytes_sent = current_sent
            self._last_bytes_recv = current_recv
            self._last_time = current_time
            self._first_read = False
            return {"upload_speed": 0.0, "download_speed": 0.0}

        
        time_delta = current_time - self._last_time
        if time_delta <= 0:
            time_delta = 1.0

        
        upload_speed = (current_sent - self._last_bytes_sent) / time_delta
        download_speed = (current_recv - self._last_bytes_recv) / time_delta

        
        self._last_bytes_sent = current_sent
        self._last_bytes_recv = current_recv
        self._last_time = current_time

        return {
            "upload_speed": max(0.0, upload_speed),
            "download_speed": max(0.0, download_speed)
        }