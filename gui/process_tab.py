import customtkinter as ctk
from typing import List, Dict, Any
from core.process_manager import ProcessManager

class ProcessView(ctk.CTkFrame):
    def __init__(self, master: Any, process_manager: ProcessManager) -> None:
        super().__init__(master)
        
        self.process_manager: ProcessManager = process_manager
        
        self.control_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=5, pady=5)
        
        self.sort_label: ctk.CTkLabel = ctk.CTkLabel(self.control_frame, text="Sort by:")
        self.sort_label.pack(side="left", padx=5)
        
        self.sort_var: ctk.StringVar = ctk.StringVar(value="CPU %")
        self.sort_menu: ctk.CTkOptionMenu = ctk.CTkOptionMenu(
            self.control_frame, 
            values=["CPU %", "Memory %", "Name", "Active Status"], 
            variable=self.sort_var
        )
        self.sort_menu.pack(side="left", padx=5)
        
        self.scroll_frame: ctk.CTkScrollableFrame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.headers: List[str] = ["PID", "Name", "CPU %", "Memory %", "Action"]
        for col, text in enumerate(self.headers):
            lbl: ctk.CTkLabel = ctk.CTkLabel(self.scroll_frame, text=text, font=("Arial", 16, "bold"))
            lbl.grid(row=0, column=col, padx=10, pady=5, sticky="w")
            
        self.scroll_frame.grid_columnconfigure(1, weight=1)
        self.row_widgets: List[List[Any]] = []

    def update_processes(self, processes: List[Dict[str, Any]]) -> None:
        self.after(0, self._apply_updates, processes)

    def kill_process_ui(self, pid: int) -> None:
        self.process_manager.kill_process(pid)

    def _apply_updates(self, processes: List[Dict[str, Any]]) -> None:
        sort_mode: str = self.sort_var.get()
        if sort_mode == "CPU %":
            processes.sort(key=lambda p: float(p.get("cpu_percent", 0.0) or 0.0), reverse=True)
        elif sort_mode == "Memory %":
            processes.sort(key=lambda p: float(p.get("memory_percent", 0.0) or 0.0), reverse=True)
        elif sort_mode == "Name":
            processes.sort(key=lambda p: str(p.get("name", "")).lower())
        elif sort_mode == "Active Status":
            processes.sort(key=lambda p: int(p.get("pid", 0)))

        display_limit: int = 50
        target_count: int = min(len(processes), display_limit)
        
        while len(self.row_widgets) < target_count:
            row_idx: int = len(self.row_widgets) + 1
            
            pid_lbl: ctk.CTkLabel = ctk.CTkLabel(self.scroll_frame, text="")
            pid_lbl.grid(row=row_idx, column=0, padx=10, pady=2, sticky="w")
            
            name_lbl: ctk.CTkLabel = ctk.CTkLabel(self.scroll_frame, text="")
            name_lbl.grid(row=row_idx, column=1, padx=10, pady=2, sticky="w")
            
            cpu_lbl: ctk.CTkLabel = ctk.CTkLabel(self.scroll_frame, text="")
            cpu_lbl.grid(row=row_idx, column=2, padx=10, pady=2, sticky="w")
            
            mem_lbl: ctk.CTkLabel = ctk.CTkLabel(self.scroll_frame, text="")
            mem_lbl.grid(row=row_idx, column=3, padx=10, pady=2, sticky="w")
            
            kill_btn: ctk.CTkButton = ctk.CTkButton(self.scroll_frame, text="Kill", width=60, fg_color="red", hover_color="darkred")
            kill_btn.grid(row=row_idx, column=4, padx=10, pady=2)
            
            self.row_widgets.append([pid_lbl, name_lbl, cpu_lbl, mem_lbl, kill_btn])
            
        while len(self.row_widgets) > target_count:
            widgets: List[Any] = self.row_widgets.pop()
            for widget in widgets:
                widget.destroy()
                
        for i in range(target_count):
            proc: Dict[str, Any] = processes[i]
            pid_val: int = proc.get("pid", 0)
            cpu_val: float = round(proc.get("cpu_percent", 0.0) or 0.0, 1)
            mem_val: float = round(proc.get("memory_percent", 0.0) or 0.0, 1)
            
            self.row_widgets[i][0].configure(text=str(pid_val))
            self.row_widgets[i][1].configure(text=str(proc.get("name", "")))
            self.row_widgets[i][2].configure(text=f"{cpu_val}%")
            self.row_widgets[i][3].configure(text=f"{mem_val}%")
            
            self.row_widgets[i][4].configure(command=lambda p=pid_val: self.kill_process_ui(p))
