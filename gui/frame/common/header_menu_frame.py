from pathlib import Path
import customtkinter as ctk
from gui.window.titration_window import TitrationWindow

class HeaderMenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.titration_window = TitrationWindow()
        
        button_data = [("滴定", self._button_open_titration_window_callback)]

        for text, command in button_data:
            button = ctk.CTkButton(self, text=text, command=command)
            button.pack(side="left", padx=10, pady=5)
    
    def set_itc_file_path(self, path):
        self.titration_window.set_itc_file_path(path)
        
    def _button_open_titration_window_callback(self):
        """
        滴定windowを開くボタンが押されたときのコールバック。
        """
        self.titration_window.mainloop()
