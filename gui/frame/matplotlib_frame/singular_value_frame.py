import customtkinter as ctk
from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.plotter.axis_settings import singular_value_axis_setting


class SingularValueFrame(MatplotlibFrame):
    def __init__(self, master: ctk.CTkFrame, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def init(self):
        singular_value_axis_setting(self.ax)
        
    def plot(self):
        self.master.svd_plotter.singular_value_plotter.plot()
        self.redraw()
