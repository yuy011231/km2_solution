from pathlib import Path
import customtkinter as ctk

class TitrationHeaderMenuFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master)
        
        button_data = [
            {
                "text": "Analysis",
                "command": self._view_titration
            }
        ]
        
        for i, data in enumerate(button_data):
            button = ctk.CTkButton(
                master=self,
                text=data["text"],
                command=data["command"]
            )
            button.grid(row=0, column=i, padx=5, pady=5)
    
    def _view_titration(self):
        self.master.plot()
