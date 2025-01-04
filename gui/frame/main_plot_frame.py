import tkinter as tk
import customtkinter
import os
from common.config import Config
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotMainFrame(customtkinter.CTkFrame):
    """
    プロットを表示するメインフレーム
    """
    def __init__(self, *args, header_name="PlotMainFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.fonts = (Config.font_type(), 15)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        """
        フォームデザインのセットアップ
        """
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(1, weight=1)

        # 左側のGUI調整ボタンを ウィジェットとしてインポートする
        self.plot_edit_frame = PlotConfigFrame(master=self, header_name="プロット設定", plot_config=self.plot_control.config)
        self.plot_edit_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

        # プロットをキャンバスに貼り付ける
        self.canvas = FigureCanvasTkAgg(self.plot_control.fig,  master=self)
        self.canvas.get_tk_widget().grid(row=0,column=1, padx=20, pady=20, sticky="nsew")

        # 保存ボタンを置く
        self.button_save = customtkinter.CTkButton(master=self, command=self.button_save_callback, text="保存", font=self.fonts)
        self.button_save.grid(row=0, column=2, padx=10, pady=20, sticky="s")   

    def update(self, csv_filepath=None, config=None):
        """
        プロット描画を更新する
        """
        self.plot_control.replot(csv_filepath, config)
        self.canvas.draw()
    
    def button_save_callback(self):
        """
        保存ボタンが押されたときのコールバック。pngに出力する
        """
        filepath = self.plot_control.save_fig()
        if filepath is not None:
            tk.messagebox.showinfo("確認", f"{filepath} に出力しました。")

class PlotConfigFrame(customtkinter.CTkFrame):
    """
    プロットを線種を調整するサブフレーム
    """
    def __init__(self, *args, header_name="PlotConfigFrame", plot_config=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name
        # plog のコンフィグ設定をコピーする
        self.plot_config = plot_config.copy()
        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        """
        フォームデザインのセットアップ
        """
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=0)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="nw")

        # 線の太さを選択する
        self.slider_label = customtkinter.CTkLabel(self, text="ライン幅 2.5", font=(FONT_TYPE, 13))
        self.slider_label.grid(row=1, column=0, padx=20, pady=(20,0), sticky="ew")

        self.slider = customtkinter.CTkSlider(master=self, from_=0.5, to=5, number_of_steps=9, hover=False, width=150, command=self.slider_event)
        self.slider.grid(row=2, column=0, padx=20, pady=(0,20), sticky="ew")

        # 線の種類を選択する
        self.combobox_label = customtkinter.CTkLabel(self, text="線種", font=(FONT_TYPE, 13))
        self.combobox_label.grid(row=3, column=0, padx=20, pady=(20,0), sticky="ew")

        self.combobox = customtkinter.CTkComboBox(master=self, font=self.fonts,
                                     values=["line", "dashed", "line + marker"],
                                     command=self.combobox_callback)
        self.combobox.grid(row=4, column=0, padx=20, pady=(0,20), sticky="ew")

    def slider_event(self, value):
        """
        スライダーで線の太さを変更するときのコールバック
        """
        # マウスでバーを動かすと、何回も更新がかかることがあるので、数値に変化があったか確認する
        old_label = self.slider_label.cget("text")
        new_label = f"ライン幅 {value}"
        if old_label != new_label:
            # 値に変更があったときのみ更新をかける
            self.slider_label.configure(text=new_label)
            self.plot_config["linewidth"] = value
            self.master.update(config=self.plot_config)
    
    def combobox_callback(self,value):
        """
        プルダウンで線種を変更するときのコールバック
        """
        self.plot_config["linetype"] = value
        self.master.update(config=self.plot_config)
