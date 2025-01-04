import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class MatplotlibFrame(ctk.CTkFrame):
    def __init__(self, master, width=400, height=300, **kwargs):
        super().__init__(master, **kwargs)
        self.width = width
        self.height = height
        
        # MatplotlibのFigureを作成
        self.figure = Figure(figsize=(self.width / 100, self.height / 100), dpi=100)
        self.ax = self.figure.add_subplot(111)  # 1x1プロット領域
        
        # FigureCanvasTkAggを使用してTkinterに埋め込む
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
    
    def plot(self):
        """データをプロットする"""
        pass
    
    def redraw(self):
        """再描画"""
        self.canvas.draw()
