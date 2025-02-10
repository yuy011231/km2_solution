import customtkinter as ctk
from km2_svd.svd_calculator import SvdCalculator
from km2_svd.plotter.plotter import SvdPlotter

from gui.frame.matplotlib_frame.noise_frame import NoiseFrame
from gui.frame.matplotlib_frame.peak_baseline_frame import PeakBaselineFrame
from gui.frame.matplotlib_frame.peak_frame import PeakFrame
from gui.frame.matplotlib_frame.singular_value_frame import SingularValueFrame
from gui.frame.tab_frame import TabFrame


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
        self.set_plotter()
        self.svd_plotter.singular_value_plot()
        self.svd_plotter.peak_plot()
        self.svd_plotter.noise_plot()
        self.svd_plotter.peak_baseline_plot()
        self.titration_index = titration_index
        
    def setup_control_frame(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(side="left", fill="y", padx=10, pady=10)

        # 採用特異値
        self.label_singular = ctk.CTkLabel(self.control_frame, text="採用特異値 0~")
        self.label_singular.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_singular = ctk.CTkEntry(
            master=self.control_frame,
            width=100,
            placeholder_text="数値を入力",
            validate="key",
            validatecommand=(self.master.register(self._validate_numeric_input), "%d", "%P")
        )
        self.entry_singular.insert(0, str(self.svd_calculator.threshold))
        self.entry_singular.grid(row=1, column=0, padx=10, pady=10)

        # ピーク開始地点
        self.label_peak_start = ctk.CTkLabel(self.control_frame, text="ピーク開始地点")
        self.label_peak_start.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_peak_start = ctk.CTkEntry(self.control_frame, width=100)
        self.entry_peak_start.insert(0, str(self.svd_calculator.start_idx))
        self.entry_peak_start.grid(row=3, column=0, padx=10, pady=10)

        # ピーク終了地点
        self.label_peak_end = ctk.CTkLabel(self.control_frame, text="ピーク終了地点")
        self.label_peak_end.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_peak_end = ctk.CTkEntry(self.control_frame, width=100)
        self.entry_peak_end.insert(0, str(self.svd_calculator.end_idx))
        self.entry_peak_end.grid(row=5, column=0, padx=10, pady=10)

        # ラジオボタンの選択変数
        self.fit_type = ctk.StringVar(value="linear")  # デフォルト: 一次フィッティング

        # 一次フィッティングのラジオボタン
        self.radio_linear = ctk.CTkRadioButton(self.control_frame, text="一次フィッティング", variable=self.fit_type, value="linear")
        self.radio_linear.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        # 二次フィッティングのラジオボタン
        self.radio_quadratic = ctk.CTkRadioButton(self.control_frame, text="二次フィッティング", variable=self.fit_type, value="quadratic")
        self.radio_quadratic.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        
        # 分析ボタン
        self.button = ctk.CTkButton(
            self.control_frame, text="Analysis", command=self.button_analysis_callback
        )
        self.button.grid(row=8, column=0, padx=10, pady=5, sticky="w")
    
    def setup_visualize_frame(self):
        self.visualize_frame = ctk.CTkFrame(self)
        self.visualize_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # ベースラインフレーム
        self.peak_baseline_frame = PeakBaselineFrame(master=self.visualize_frame)
        self.peak_baseline_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.peak_noise_frame = ctk.CTkFrame(self)
        self.singular_frame = ctk.CTkFrame(self)
        # ピークフレーム
        self.peak_frame = PeakFrame(master=self.peak_noise_frame)
        self.peak_frame.pack(side="top", fill="both", expand=False, padx=10, pady=5)
        # ノイズフレーム
        self.noise_frame = NoiseFrame(master=self.peak_noise_frame)
        self.noise_frame.pack(side="top", fill="both", expand=False, padx=10, pady=5)
        # 特異値フレーム
        self.singular_value_frame = SingularValueFrame(master=self.singular_frame)
        self.singular_value_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        tab_names=["PeakNoise", "Singular"]
        self.tab_frame = TabFrame(master=self.visualize_frame, tab_names=tab_names)
        self.tab_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.tab_frame.add_frame_to_tab("PeakNoise", self.peak_noise_frame)
        self.tab_frame.add_frame_to_tab("Singular", self.singular_frame)
        
        self.visualize_frame.grid_columnconfigure(0, weight=3)
        self.visualize_frame.grid_columnconfigure(1, weight=2)
    
    def set_plotter(self):
        self.peak_frame.plotter = self.svd_plotter.peak_plotter
        self.noise_frame.plotter = self.svd_plotter.noise_plotter
    
    def button_analysis_callback(self):
        singular_threshold = int(self.entry_singular.get())
        peak_start = int(self.entry_peak_start.get())
        peak_end = int(self.entry_peak_end.get())
        fit_type = self.fit_type.get()
        self.svd_calculator.threshold = singular_threshold
        self.svd_calculator.set_start_idx(peak_start)
        self.svd_calculator.set_end_idx(peak_end)
        # TODO: フラグではなく文字列で判定したい
        self.svd_calculator.is_linear = True if fit_type == "linear" else False
        self.svd_plotter.peak_plot()
        self.svd_plotter.noise_plot()
        self.svd_plotter.peak_baseline_plot()
        self.peak_frame.redraw()
        self.noise_frame.redraw()
    
    def _validate_numeric_input(self, action, value_if_allowed):
        if action == "1":
            if value_if_allowed.isdigit():
                return True
            else:
                return False
        return True
