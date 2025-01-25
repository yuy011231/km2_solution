import tkinter as tk
import customtkinter as ctk
import os
from common.config import Config

class FileFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fonts = (Config.font_type(), 15)
        self.textbox = ctk.CTkEntry(master=self, placeholder_text="ITC ファイルを読み込む", width=120, font=self.fonts)
        self.button_select = ctk.CTkButton(master=self, 
            fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
            command=self.button_select_callback, text="ファイル選択", font=self.fonts)
        self.button_open = ctk.CTkButton(master=self, command=self.button_open_callback, text="開く", font=self.fonts)
        self.setup_form()

    def setup_form(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.button_select.grid(row=1, column=1, padx=10, pady=10)
        self.button_open.grid(row=1, column=2, padx=10, pady=10)

    def button_select_callback(self):
        """
        選択ボタンが押されたときのコールバック。ファイル選択ダイアログを表示する
        """
        # エクスプローラーを表示してファイルを選択する
        file_name = FileFrame.file_read()

        if file_name is not None:
            # ファイルパスをテキストボックスに記入
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0, file_name)

    def button_open_callback(self):
        """
        開くボタンが押されたときのコールバック。
        """
        self.master.button_open_callback()
            
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
