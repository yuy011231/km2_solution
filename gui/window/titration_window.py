from datetime import datetime
from pathlib import Path
from tkinter import filedialog
import customtkinter as ctk
from gui.window.base_window import BaseWindow
from gui.frame.titration_frame import TitrationFrame
from gui.frame.common.titration_header_menu_frame import TitrationHeaderMenuFrame


class TitrationWindow(BaseWindow):
    def __init__(self, main_window: ctk.CTk):
        self.main_window = main_window
        super().__init__()
        self.title("titration")
        self.itc_file_path = None
    
    def set_itc_file_path(self, path: Path):
        self.itc_file_path = path
        
    def _custom_setup(self):
        # header
        self.header_menu_frame = TitrationHeaderMenuFrame(main_window=self.main_window, master=self)
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
        
        self.svd_plot_frames = [
            TitrationFrame(titration_index=i, svd_calculator=svd_calculator, master=self.scrollable_frame, width=800, height=600) 
            for i, svd_calculator 
            in enumerate(self.main_window.svd_calculators)
        ]
        for frame in self.svd_plot_frames:
            frame.pack(padx=5, pady=5, fill="both", expand=True)
    
    def save_titration_plot(self):
        file_path = filedialog.askdirectory(title="保存先のフォルダを選択")
        
        if not file_path:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path=Path(file_path) / timestamp
        output_path.mkdir(parents=True, exist_ok=True)
        for frame in self.svd_plot_frames:
            titration_dir=output_path / f"{frame.titration_index}"
            titration_dir.mkdir(parents=True, exist_ok=True)
            # TODO: ピーク/ノイズ/ベースライン成分csv
            frame.svd_plotter.save_fig(titration_dir)
