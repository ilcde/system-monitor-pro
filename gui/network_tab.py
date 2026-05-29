import customtkinter as ctk
from typing import Dict, Any, List
from utils.formatting import format_bytes
import tkinter as tk

class NetworkView(ctk.CTkFrame):
    def __init__(self, master: Any) -> None:
        super().__init__(master)
        
        self.upload_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Upload Speed: 0 B/s", text_color="red", font=("Arial", 20, "bold"))
        self.upload_label.pack(pady=10)
        
        self.download_label: ctk.CTkLabel = ctk.CTkLabel(self, text="Download Speed: 0 B/s", text_color="green", font=("Arial", 20, "bold"))
        self.download_label.pack(pady=10)

        self.canvas: tk.Canvas = tk.Canvas(self, bg="#2b2b2b", highlightthickness=0, height=200)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.history_len: int = 50
        self.upload_history: List[int] = [0] * self.history_len
        self.download_history: List[int] = [0] * self.history_len

    def update_network(self, network: Dict[str, int]) -> None:
        self.after(0, self._apply_updates, network)

    def _apply_updates(self, network: Dict[str, int]) -> None:
        upload_speed: int = network.get("upload_speed", 0)
        download_speed: int = network.get("download_speed", 0)
        
        up_formatted: str = format_bytes(upload_speed)
        down_formatted: str = format_bytes(download_speed)
        
        self.upload_label.configure(text=f"Upload Speed: {up_formatted}/s")
        self.download_label.configure(text=f"Download Speed: {down_formatted}/s")
        
        self.upload_history.pop(0)
        self.upload_history.append(upload_speed)
        self.download_history.pop(0)
        self.download_history.append(download_speed)
        
        self.canvas.delete("all")
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        max_val: int = max(max(self.upload_history), max(self.download_history), 1024)
        x_step: float = width / (self.history_len - 1)
        
        up_coords: List[float] = []
        down_coords: List[float] = []
        
        for i in range(self.history_len):
            x: float = i * x_step
            up_y: float = height - (self.upload_history[i] / max_val * height)
            down_y: float = height - (self.download_history[i] / max_val * height)
            
            up_coords.extend([x, up_y])
            down_coords.extend([x, down_y])
            
        if len(up_coords) >= 4:
            self.canvas.create_line(up_coords, fill="red", width=2, smooth=True)
            self.canvas.create_line(down_coords, fill="green", width=2, smooth=True)
