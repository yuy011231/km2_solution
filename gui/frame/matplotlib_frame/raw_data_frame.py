from gui.frame.matplotlib_frame.matplotlib_frame import MatplotlibFrame
from km2_svd.plotter.axis_settings import raw_axis_setting
from km2_svd.plotter.plotter import RawDataPlotter

from gui.frame.tab_frame import TabFrame


class RawDataFrame(MatplotlibFrame):
    def __init__(self, master: TabFrame, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def set_plotter(self):
        self.plotter = RawDataPlotter(self.master.master.reader.data_df, self.ax)
    
    def init(self):
        raw_axis_setting(self.ax)
        
    def plot(self):
        self.plotter.plot()
        self.redraw()
