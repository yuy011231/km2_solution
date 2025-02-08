from abc import abstractmethod
import customtkinter as ctk
from common.config import Config

class BaseWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.fonts = (Config.font_type(), 15) # font
        self._setup_form()
        self._custom_setup()
    
    def _setup_form(self):
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        self.geometry(Config.app_initial_window_size()) # size
        self.title("Km2_itc")
    
    @abstractmethod  
    def _custom_setup(self):
        """windowごとのsetup"""

