from typing import Sequence

import pandas as pd
import customtkinter as ctk
from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.plotter import SvdPlotter

from gui.frame.matplotlib_frame.noise_frame import NoiseFrame
from gui.frame.matplotlib_frame.peak_baseline_frame import PeakBaselineFrame
from gui.frame.matplotlib_frame.peak_frame import PeakFrame
from gui.frame.matplotlib_frame.singular_value_frame import SingularValueFrame


class TitrationFrame(ctk.CTkFrame):
    def __init__(self, titration_index: int, svd_calculator: SvdCalculator, master, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
        self.svd_calculator = svd_calculator
        self.setup_control_frame()
        self.setup_visualize_frame()
        self.svd_plotter = SvdPlotter(
            svd_calculator, 
            self.singular_value_frame.ax, 
            self.peak_frame.ax, 
            self.noise_frame.ax,
            self.peak_baseline_frame.ax
        )
        self.svd_plotter.singular_value_plot()
        self.svd_plotter.peak_plot()
        self.svd_plotter.noise_plot()
        self.titration_index = titration_index
        
    def setup_control_frame(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)
        # 数値入力用テキストボックス
        self.entry = ctk.CTkEntry(
            master=self.control_frame,
            width=100,
            placeholder_text="数値を入力",
            validate="key",
            validatecommand=(self.master.register(self._validate_numeric_input), "%d", "%P")
        )
        self.entry.pack(anchor="n", pady=5)
        self.entry.insert(0, str(self.svd_calculator.threshold))
        
        # 分析ボタン
        self.button = ctk.CTkButton(
            self.control_frame, text="Analysis", command=self.button_analysis_callback
        )
        self.button.pack(anchor="n", pady=5)
    
    def setup_visualize_frame(self):
        self.visualize_frame = ctk.CTkFrame(self)
        self.visualize_frame.pack(side="left", fill="y", padx=10, pady=10)
        # ピークフレーム
        self.peak_frame = PeakFrame(master=self.visualize_frame)
        self.peak_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # ノイズフレーム
        self.noise_frame = NoiseFrame(master=self.visualize_frame)
        self.noise_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        # 特異値フレーム
        self.singular_value_frame = SingularValueFrame(master=self.visualize_frame)
        self.singular_value_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        # ベースラインフレーム
        self.peak_baseline_frame = PeakBaselineFrame(master=self.visualize_frame)
        # self.peak_baseline_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        self.visualize_frame.grid_rowconfigure(0, weight=1)
        self.visualize_frame.grid_rowconfigure(1, weight=1)
        self.visualize_frame.grid_columnconfigure(0, weight=2)
        self.visualize_frame.grid_columnconfigure(1, weight=1)
    
    def button_analysis_callback(self):
        threshold = int(self.entry.get())
        self.svd_calculator.threshold = threshold
        self.svd_plotter.peak_plot()
        self.svd_plotter.noise_plot()
        self.peak_frame.redraw()
        self.noise_frame.redraw()
    
    def _validate_numeric_input(self, action, value_if_allowed):
        if action == "1":
            if value_if_allowed.isdigit():
                return True
            else:
                return False
        return True
