from abc import abstractmethod
import customtkinter as ctk
from common.config import Config
from gui.frame.common.header_frame import HeaderFrame
from gui.frame.matplotlib_frame.km2_svd_frame import Km2SvdFrame

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
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    @abstractmethod  
    def _custom_setup(self):
        """windowごとのsetup"""

