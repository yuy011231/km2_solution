import customtkinter as ctk

class TabFrame(ctk.CTkTabview):
    def __init__(self, master, tab_names, **kwargs):
        super().__init__(master, width=400, height=300, **kwargs)
        for tab_name in tab_names:
            self._add_tab(tab_name)

    def _add_tab(self, tab_name):
        """タブを追加する"""
        self.add(tab_name)

    def add_frame_to_tab(self, tab_name, frame: ctk.CTkFrame):
        """既存のタブにフレームを追加するメソッド"""
        tab_frame = self.tab(tab_name)  # タブのフレームを取得
        if tab_frame:
            # フレームをタブ内に配置
            frame.pack(pady=10, padx=10, fill="both", expand=True, in_=tab_frame)
        else:
            raise ValueError(f"タブ '{tab_name}' は存在しません。")
        