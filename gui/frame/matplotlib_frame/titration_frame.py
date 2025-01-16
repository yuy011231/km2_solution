from typing import Sequence

import pandas as pd
import customtkinter as ctk
from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.axis_settings import titration_axis_setting
from km2_svd.plotter.titration_plotter import TitrationPlotter

class TitrationPlotFrame(MatplotlibFrame):
    def __init__(self, master, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def init(self):
        titration_axis_setting(self.ax)
        
    def plot(self, noise_removal_power_df: pd.DataFrame):
        plotter=TitrationPlotter(noise_removal_power_df, self.ax)
        plotter.plot()
        self.redraw()

class TitrationFrame(ctk.CTkFrame):
    def __init__(self, master, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
        # 左側のフレーム
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        # 数値入力用テキストボックス
        self.entry = ctk.CTkEntry(
            master=self.left_frame,
            width=100,
            placeholder_text="数値を入力",
            validate="key",  # 入力ごとにバリデーションを実行
            validatecommand=(master.register(self._validate_numeric_input), "%d", "%P")  # 引数: action, value_if_allowed
        )
        self.entry.pack(anchor="n", pady=5)  # 左上に配置

        # 分析ボタン
        self.button = ctk.CTkButton(self.left_frame, text="Analysis", command=self.button_analysis_callback)
        self.button.pack(anchor="n", pady=5)  # テキストボックスの下に配置

        # 右側のプロットフレーム
        self.titration_plot_frame = TitrationPlotFrame(self, width=600, height=600, **kwargs)
        self.titration_plot_frame.pack(side="left", padx=10, pady=10)
        
    
    def init(self):
        titration_axis_setting(self.ax)
        
    def plot(self, noise_removal_power_df: pd.DataFrame):
        self.titration_plot_frame.plot(noise_removal_power_df)
    
    def button_analysis_callback(self):
        self.titration_plot_frame.plot()
    
    def _validate_numeric_input(self, action, value_if_allowed):
        if action == "1":
            if value_if_allowed.isdigit():  # 入力が数字のみなら許可
                return True
            else:
                return False  # 数字以外は拒否
        return True  # 削除（action == "0"）は常に許可
