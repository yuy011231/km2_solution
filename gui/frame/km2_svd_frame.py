from gui.frame.matplotlib_frame import MatplotlibFrame
from km2_svd.reader.itc_reader import ItcReader
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.axis_settings import power_axis_setting

class Km2SvdFrame(MatplotlibFrame):
    def __init__(self, master, width=800, height=600, **kwargs):
        super().__init__(master, width, height, **kwargs)
    
    def init(self):
        power_axis_setting(self.ax)
        
    def plot(self, path, peak_threshold, s_window_size):
        reader = ItcReader(path)
        svd=SvdCalculator(reader, peak_threshold, s_window_size)
        plotter_svd=svd.get_power_plotter(ax=self.ax)
        plotter_svd.plot()
        self.redraw()
