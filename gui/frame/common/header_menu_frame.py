from pathlib import Path
import customtkinter as ctk
from gui.window.titration_window import TitrationWindow

class HeaderMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        button_data = [("滴定", self.master.button_open_titration_window_callback)]

        for text, command in button_data:
            button = ctk.CTkButton(self, text=text, command=command)
            button.pack(side="left", padx=10, pady=5)
