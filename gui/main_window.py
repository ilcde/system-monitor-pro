import customtkinter as ctk
from gui.dashboard import DashboardView
from gui.process_tab import ProcessView
from gui.network_tab import NetworkView
from core.scheduler import DataScheduler
from typing import Any

class MainWindow(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master)
        
        self.tab_view: ctk.CTkTabview = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_view.add("Dashboard")
        self.tab_view.add("Processes")
        self.tab_view.add("Network")
        
        self.dashboard_view: DashboardView = DashboardView(self.tab_view.tab("Dashboard"))
        self.dashboard_view.pack(fill="both", expand=True)
        
        self.data_scheduler: DataScheduler = DataScheduler(
            self.dashboard_view.update_metrics,
            self._update_processes_proxy,
            self._update_network_proxy
        )
        
        self.process_view: ProcessView = ProcessView(self.tab_view.tab("Processes"), self.data_scheduler.proc_manager)
        self.process_view.pack(fill="both", expand=True)

        self.network_view: NetworkView = NetworkView(self.tab_view.tab("Network"))
        self.network_view.pack(fill="both", expand=True)
        
    def start_monitoring(self) -> None:
        self.data_scheduler.start()

    def stop_monitoring(self) -> None:
        self.data_scheduler.stop()

    def _update_processes_proxy(self, data: Any) -> None:
        self.process_view.update_processes(data)
        
    def _update_network_proxy(self, data: Any) -> None:
        self.network_view.update_network(data)
