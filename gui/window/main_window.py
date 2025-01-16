import customtkinter as ctk
from common.config import Config
from gui.frame.common.header_menu_frame import HeaderMenuFrame
from gui.frame.common.file_frame import FileFrame
from gui.frame.matplotlib_frame.km2_svd_frame import Km2SvdFrame
from gui.frame.tab_frame import TabFrame
from gui.window.base_window import BaseWindow

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()

    def _custom_setup(self):
        # main画面のheader
        self.header_menu_frame = HeaderMenuFrame(master=self)
        self.header_menu_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.read_file_frame = FileFrame(master=self)
        self.read_file_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # tab view
        tab_names=["RowData", "Power"]
        self.tab_frame = TabFrame(master=self, tab_names=tab_names)
        self.tab_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        
        # km2_svd出力表示用
        self.row_data_plot_frame = Km2SvdFrame(master=self.tab_frame, width=800, height=600)
        self.row_data_plot_frame.init()
        self.power_plot_frame = Km2SvdFrame(master=self.tab_frame, width=800, height=600)
        self.power_plot_frame.init()
        
        self.tab_frame.add_frame_to_tab("RowData", self.row_data_plot_frame)
        self.tab_frame.add_frame_to_tab("Power", self.power_plot_frame)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def km2_svd_row_data_visualize(self, csv_filepath):
        self.row_data_plot_frame.row_data_plot(csv_filepath)
    
    def km2_svd_power_visualize(self, csv_filepath):
        self.power_plot_frame.power_plot(csv_filepath, 10)
        
    def set_itc_file_path(self, path):
        self.header_menu_frame.set_itc_file_path(path)

