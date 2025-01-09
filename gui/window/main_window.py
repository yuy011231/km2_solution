import customtkinter as ctk
from common.config import Config
from gui.frame.common.header_frame import HeaderFrame
from gui.frame.matplotlib_frame.km2_svd_frame import Km2SvdFrame
from gui.frame.tab_frame import TabFrame
from gui.window.base_window import BaseWindow

class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__()

    def _custom_setup(self):
        # main画面のheader
        self.read_file_frame = HeaderFrame(master=self, header_name="ファイル読み込み")
        self.read_file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        # tab view
        tab_names=["RowData", "Power"]
        self.tab_frame = TabFrame(master=self, tab_names=tab_names)
        self.tab_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        
        # km2_svd出力表示用
        self.row_data_plot_frame = Km2SvdFrame(master=self.tab_frame, width=800, height=600)
        self.row_data_plot_frame.init()
        self.power_plot_frame = Km2SvdFrame(master=self.tab_frame, width=800, height=600)
        self.power_plot_frame.init()
        
        self.tab_frame.add_frame_to_tab("RowData", self.row_data_plot_frame)
        self.tab_frame.add_frame_to_tab("Power", self.power_plot_frame)
    
    def km2_svd_row_data_visualize(self, csv_filepath):
        self.row_data_plot_frame.row_data_plot(csv_filepath)
    
    def km2_svd_power_visualize(self, csv_filepath):
        self.power_plot_frame.power_plot(csv_filepath, 4, 10)

