import tkinter as tk
import customtkinter as ctk
import os
from common.config import Config

class HeaderFrame(ctk.CTkFrame):
    def __init__(self, *args, header_name="ReadFileFrame", **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (Config.font_type(), 15)
        self.header_name = header_name

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        # フレームのラベルを表示
        self.label = ctk.CTkLabel(self, text=self.header_name, font=(Config.font_type(), 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        # ファイルパスを指定するテキストボックス。これだけ拡大したときに、幅が広がるように設定する。
        self.textbox = ctk.CTkEntry(master=self, placeholder_text="ITC ファイルを読み込む", width=120, font=self.fonts)
        self.textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

        # ファイル選択ボタン
        self.button_select = ctk.CTkButton(master=self, 
            fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),   # ボタンを白抜きにする
            command=self.button_select_callback, text="ファイル選択", font=self.fonts)
        self.button_select.grid(row=1, column=1, padx=10, pady=(0,10))
        
        # 開くボタン
        self.button_open = ctk.CTkButton(master=self, command=self.button_open_callback, text="開く", font=self.fonts)
        self.button_open.grid(row=1, column=2, padx=10, pady=(0,10))

    def button_select_callback(self):
        """
        選択ボタンが押されたときのコールバック。ファイル選択ダイアログを表示する
        """
        # エクスプローラーを表示してファイルを選択する
        file_name = HeaderFrame.file_read()

        if file_name is not None:
            # ファイルパスをテキストボックスに記入
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0, file_name)

    def button_open_callback(self):
        """
        開くボタンが押されたときのコールバック。
        """
        # ひとまずプロット
        # 裏で計算準備
        file_name = self.textbox.get()
        self.master.km2_svd_power_visualize(file_name)
        self.master.km2_svd_row_data_visualize(file_name)
            
    @staticmethod
    def file_read():
        """
        ファイル選択ダイアログを表示する
        """
        current_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = tk.filedialog.askopenfilename(filetypes=[("itcファイル","*.itc")],initialdir=current_dir)

        if len(file_path) != 0:
            return file_path
        else:
            return None
