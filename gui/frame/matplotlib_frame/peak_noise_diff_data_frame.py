from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.plotter.plotter import PeakNoiseDiffPlotter
from km2_svd.plotter.axis_settings import power_axis_setting

from gui.frame.tab_frame import TabFrame


class PeakNoiseDiffDataFrame(MatplotlibFrame):
    def __init__(self, master: TabFrame, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def init(self):
        power_axis_setting(self.ax)
        
    def plot(self):
        plotter=PeakNoiseDiffPlotter(self.master.master.svd_calculators, self.ax)
        plotter.plot()
        self.redraw()
