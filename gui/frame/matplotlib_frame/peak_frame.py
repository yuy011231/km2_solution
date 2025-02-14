import customtkinter as ctk
from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.plotter.axis_settings import peak_noise_axis_setting
from km2_svd.plotter.plotter import PeakPlotter

from gui.frame.tab_frame import TabFrame


class PeakFrame(MatplotlibFrame):
    def __init__(self, master: ctk.CTkFrame, width=800, height=300, **kwargs):
        super().__init__(master, width, height, **kwargs)
        self.plotter: PeakPlotter|None = None
    
    def init(self):
        peak_noise_axis_setting(self.ax)
        
    def plot(self):
        if self.plotter is None:
            return
        self.plotter.plot()
        self.redraw()
