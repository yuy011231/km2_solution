import customtkinter as ctk
from common.config import Config
from gui.frame.header_frame import HeadderFrame
from gui.frame.km2_svd_frame import Km2SvdFrame

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # メンバー変数の設定
        self.fonts = (Config.font_type(), 15)

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # フォームサイズ設定
        self.geometry(Config.app_initial_window_size())
        self.title("Km2_itc")

        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        # 1つ目のフレームの設定
        # stickyは拡大したときに広がる方向のこと。nsew で4方角で指定する。
        self.read_file_frame = HeadderFrame(master=self, header_name="ファイル読み込み")
        self.read_file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.matplotlib_frame= Km2SvdFrame(master=self, width=800, height=600)
        self.matplotlib_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.matplotlib_frame.init()
    
    def km2_svd_power_visualize(self, csv_filepath):
        self.matplotlib_frame.plot(csv_filepath, 4, 10)

