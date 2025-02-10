from datetime import datetime
from pathlib import Path
from tkinter import filedialog
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from gui.frame.common.header_menu_frame import HeaderMenuFrame
from gui.frame.common.file_frame import FileFrame
from gui.frame.matplotlib_frame.raw_data_frame import RawDataFrame
from gui.frame.matplotlib_frame.peak_noise_diff_data_frame import PeakBaselineDiffDataFrame
from gui.frame.tab_frame import TabFrame
from gui.window.base_window import BaseWindow
from gui.window.titration_window import TitrationWindow

class MainWindow(BaseWindow):
    def __init__(self):
        self.reader = None
        self.svd_calculators = None
        super().__init__()

    def _custom_setup(self):
        self.header_menu_frame = HeaderMenuFrame(master=self)
        self.read_file_frame = FileFrame(master=self)
        tab_names=["RawData", "PeakNoiseDiffData"]
        self.tab_frame = TabFrame(master=self, tab_names=tab_names)
        self.raw_data_frame = RawDataFrame(master=self.tab_frame, width=800, height=600)
        self.peak_noise_diff_data_frame = PeakBaselineDiffDataFrame(master=self.tab_frame, width=800, height=600)
        self.titration_window = TitrationWindow(main_window=self)
        
        # main画面のheader
        self.header_menu_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        # ファイル読み込みフレーム
        self.read_file_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        # tab view
        self.tab_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        # km2_svd出力表示用
        self.raw_data_frame.init()
        self.peak_noise_diff_data_frame.init()
        
        # tabにフレームを追加
        self.tab_frame.add_frame_to_tab("RawData", self.raw_data_frame)
        self.tab_frame.add_frame_to_tab("PeakNoiseDiffData", self.peak_noise_diff_data_frame)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)
        self.grid_columnconfigure(0, weight=1)
    
    def km2_svd_row_data_visualize(self):
        self.raw_data_frame.plot()
    
    def km2_svd_peak_noise_diff_visualize(self):
        self.peak_noise_diff_data_frame.plot()
        
    def set_itc_file_path(self, path):
        self.titration_window.set_itc_file_path(path)
    
    # headerメニューのコールバック
    def button_open_titration_window_callback(self):
        self.titration_window.plot()
        self.titration_window.mainloop()
    
    def button_save_fig_callback(self):
        file_path = filedialog.askdirectory(title="保存先のフォルダを選択")
        
        if not file_path:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path=Path(file_path) / f"{timestamp}_main"
        output_path.mkdir(parents=True, exist_ok=True)
        
        self.raw_data_frame.plotter.save_fig(output_path / "row_data.png")
        self.raw_data_frame.plotter.save_csv(output_path)
        self.peak_noise_diff_data_frame.plotter.save_fig(output_path / "peak_noise_diff_data.png")
    
    # fileフレームのコールバック
    def button_open_callback(self):
        file_name = self.read_file_frame.textbox.get()
        self.reader = ItcReader(file_name)
        self.svd_calculators = [
            SvdCalculator(self.reader.get_titration_df(i), 10, 1, 4) 
            for i 
            in range(1, self.reader.split_count)
        ]
        self.raw_data_frame.set_plotter()
        self.peak_noise_diff_data_frame.set_plotter()
        self.set_itc_file_path(file_name)
        self.km2_svd_row_data_visualize()
        self.header_menu_frame.enable_buttons()
