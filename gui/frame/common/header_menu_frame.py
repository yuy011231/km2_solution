from pathlib import Path
from typing import Sequence
import customtkinter as ctk
from gui.window.titration_window import TitrationWindow

class HeaderMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.buttons: Sequence[ctk.CTkButton] = []
        
        button_data = [
            ("Titration", self.master.button_open_titration_window_callback), 
            ("Save", self.master.button_save_fig_callback)
        ]

        for text, command in button_data:
            button = ctk.CTkButton(self, text=text, command=command)
            button.configure(state="disabled")
            button.pack(side="left", padx=10, pady=5)
            self.buttons.append(button)
    
    def enable_buttons(self):
        for button in self.buttons:
            button.configure(state="normal")
