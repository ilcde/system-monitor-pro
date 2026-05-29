import os
import customtkinter as ctk
from gui.main_window import MainWindow

class SystemMonitorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("System Monitor Pro")
        self.geometry("800x600")
        
        if os.path.exists("assets/app_icon.ico"):
            self.iconbitmap("assets/app_icon.ico")
        
        self.main_window: MainWindow = MainWindow(self)
        self.main_window.pack(fill="both", expand=True)
        self.main_window.start_monitoring()

    def destroy(self) -> None:
        self.main_window.stop_monitoring()
        super().destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app: SystemMonitorApp = SystemMonitorApp()
    app.mainloop()
