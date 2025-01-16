from pathlib import Path
import customtkinter as ctk
from common.config import Config
from gui.window.base_window import BaseWindow
from gui.frame.matplotlib_frame.titration_frame import TitrationFrame
from gui.frame.common.titration_header_menu_frame import TitrationHeaderMenuFrame
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.axis_settings import titration_axis_setting
from km2_svd.plotter.titration_plotter import TitrationPlotter

class TitrationWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.title("titration")
        self.itc_file_path = None
    
    def set_itc_file_path(self, path: Path):
        self.itc_file_path = path
        
    def _custom_setup(self):
        # main画面のheader
        self.header_menu_frame = TitrationHeaderMenuFrame(master=self)
        self.header_menu_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        # scrollable_frame
        self.scrollable_frame = ctk.CTkScrollableFrame(master=self)
        self.scrollable_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def plot(self):
        if self.itc_file_path is None:
            raise ValueError("itc_file_path is not set")
        
        reader = ItcReader(self.itc_file_path)
        svd = SvdCalculator(reader, 10)
        noise_removal_power_dfs = svd.get_noise_removal_power(4)
        
        self.row_data_plot_frames = [TitrationFrame(master=self.scrollable_frame, width=800, height=600) for _ in range(len(noise_removal_power_dfs))]
        for frame, noise_removal_power_df in zip(self.row_data_plot_frames, noise_removal_power_dfs):
            frame.pack(padx=5, pady=5)
            frame.plot(noise_removal_power_df)
