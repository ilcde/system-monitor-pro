import customtkinter as ctk
from typing import Dict, Any, List
import tkinter as tk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master: Any) -> None:
        super().__init__(master)
        
        self.cpu_label: ctk.CTkLabel = ctk.CTkLabel(self, text="CPU: 0.0%", font=("Arial", 20, "bold"), text_color="cyan")
        self.cpu_label.pack(pady=10)
        
        self.memory_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Memory: 0.0%", font=("Arial", 20, "bold"), text_color="lime")
        self.memory_label.pack(pady=10)

        self.disk_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Disk: 0.0%", font=("Arial", 20, "bold"), text_color="orange")
        self.disk_label.pack(pady=10)

        self.canvas: tk.Canvas = tk.Canvas(self, bg="#2b2b2b", highlightthickness=0, height=200)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.history_len: int = 50
        self.cpu_history: List[float] = [0.0] * self.history_len
        self.memory_history: List[float] = [0.0] * self.history_len
        self.disk_history: List[float] = [0.0] * self.history_len

    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        self.after(0, self._apply_updates, metrics)

    def _apply_updates(self, metrics: Dict[str, Any]) -> None:
        cpu_val: float = metrics.get("cpu_percent", 0.0)
        mem_val: float = metrics.get("memory_percent", 0.0)
        disk_val: float = metrics.get("disk_percent", 0.0)
        
        self.cpu_label.configure(text=f"CPU: {cpu_val}%")
        self.memory_label.configure(text=f"Memory: {mem_val}%")
        self.disk_label.configure(text=f"Disk: {disk_val}%")
        
        self.cpu_history.pop(0)
        self.cpu_history.append(cpu_val)
        self.memory_history.pop(0)
        self.memory_history.append(mem_val)
        self.disk_history.pop(0)
        self.disk_history.append(disk_val)
        
        self.canvas.delete("all")
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        max_val: float = 100.0
        x_step: float = width / (self.history_len - 1)
        
        cpu_coords: List[float] = []
        mem_coords: List[float] = []
        disk_coords: List[float] = []
        
        for i in range(self.history_len):
            x: float = i * x_step
            cpu_y: float = height - (self.cpu_history[i] / max_val * height)
            mem_y: float = height - (self.memory_history[i] / max_val * height)
            disk_y: float = height - (self.disk_history[i] / max_val * height)
            
            cpu_coords.extend([x, cpu_y])
            mem_coords.extend([x, mem_y])
            disk_coords.extend([x, disk_y])
            
        if len(cpu_coords) >= 4:
            self.canvas.create_line(cpu_coords, fill="cyan", width=2, smooth=True)
            self.canvas.create_line(mem_coords, fill="lime", width=2, smooth=True)
            self.canvas.create_line(disk_coords, fill="orange", width=2, smooth=True)
