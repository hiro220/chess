#!/usr/bin/env python
# coding:utf-8

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Promotion(tk.Toplevel):
    # Toplevelクラスを継承している。
    def __init__(self):
        super().__init__()
        self.title("Choice what to Promote")
        self.geometry("400x300+100+40")

        self.main_frame = tk.Frame(self, height=300, width=400)
        self.main_frame.pack()
        self.canvas_frame = tk.Frame(self.main_frame, height=250, width=400)
        self.canvas_frame.pack()
        self.canvas = tk.Canvas(self.canvas_frame, height=250, width=400)
        self.button_frame = tk.Frame(self.main_frame,height=50, width=400)
        self.canvas.pack()
        self.button_frame.pack()

        # ボタンの作成
        self.rook_button = tk.Button(self.button_frame, text="ROOK", command=self.rook)
        self.knight_button = tk.Button(self.button_frame, text="KNIGHT", command=self.knight)
        self.bishop_button = tk.Button(self.button_frame, text="BISHOP", command=self.bishop)
        self.queen_button = tk.Button(self.button_frame, text="QUEEN", command=self.queen)
        self.rook_button.pack(side=tk.LEFT)
        self.knight_button.pack(side=tk.LEFT)
        self.bishop_button.pack(side=tk.LEFT)
        self.queen_button.pack(side=tk.LEFT)

        # 駒の画像をopenする。
        self._openImage()
        # フォーカスをセットする。
        self.focus_set()
        # ウィンドウを閉じようとしたときのメソッドの設定。
        self.protocol("WM_DELETE_WINDOW", self._close_message)
        # 親ウィンドウへフォーカスできないようにする。
        self.grab_set()
        self.show()
        self.select = ""
    
    def _openImage(self):
        self.file = []
        for i in (1, 2, 3, 4):
            image = Image.open("image/chess"+str(i)+".png")
            self.file.append(ImageTk.PhotoImage(image))

    def rook(self):
        self.select = 'rook'

    def knight(self):
        self.select = 'kngiht'
    
    def bishop(self):
        self.select = 'bishop'

    def queen(self):
        self.select = 'queen'

    def _close_message(self):
        messagebox.showwarning("Warning", "プロモーションする駒を選択してください。")
        self.destroy()

    def show(self):
        # 駒を表示する。
        for i in range(len(self.file)):
            x = i * 100 + 50
            y = 100
            self.canvas.create_image(x, y, image=self.file[i], tag="piece")

    def isSelect(self):
        return self.select != ""
        