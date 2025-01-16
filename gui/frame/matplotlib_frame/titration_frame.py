from typing import Sequence

import pandas as pd
from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.axis_settings import titration_axis_setting
from km2_svd.plotter.titration_plotter import TitrationPlotter

class TitrationFrame(MatplotlibFrame):
    def __init__(self, master, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def init(self):
        titration_axis_setting(self.ax)
        
    def plot(self, noise_removal_power_df: pd.DataFrame):
        plotter=TitrationPlotter(noise_removal_power_df, self.ax)
        plotter.plot()
        self.redraw()

class TitrationFrames:
    def __init__(self, master, target_dfs: Sequence[pd.DataFrame],width=800, height=600, **kwargs):
        self.plotters = [TitrationFrame(master, width, height, **kwargs) for df in target_dfs]
    
    def init(self):
        for plotter in self.plotters:
            plotter.init()
    
    def plot(self, path, peak_threshold, s_window_size):
        reader = ItcReader(path)
        svd=SvdCalculator(reader, s_window_size)
        noise_removal_power_dfs = svd.get_noise_removal_power(peak_threshold)
        for noise_removal_power_df, plotter in zip(noise_removal_power_dfs, self.plotters):
            plotter.plot(noise_removal_power_df)
            plotter.redraw()
