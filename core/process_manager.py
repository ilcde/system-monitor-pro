import psutil
from typing import Dict, Any, List

class ProcessManager:
    def get_processes(self) -> List[Dict[str, Any]]:
        process_list: List[Dict[str, Any]] = []
        for proc in psutil.process_iter():
            try:
                with proc.oneshot():
                    pid: int = proc.pid
                    if pid == 0:
                        continue
                    name: str = proc.name()
                    cpu: float = proc.cpu_percent()
                    mem: float = proc.memory_percent()
                    process_list.append({
                        "pid": pid,
                        "name": name,
                        "cpu_percent": cpu,
                        "memory_percent": mem
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        process_list.sort(key=lambda p: p.get('cpu_percent', 0.0) or 0.0, reverse=True)
        return process_list

    def kill_process(self, pid: int) -> bool:
        try:
            target_proc: psutil.Process = psutil.Process(pid)
            target_proc.terminate()
            target_proc.wait(timeout=3)
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            try:
                target_proc.kill()
                return True
            except Exception:
                return False
        except Exception:
            return False
