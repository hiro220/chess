#!/usr/bin/env python
# coding:utf-8

import tkinter as tk
from PIL import Image, ImageTk
from chessboard import Chess_Board
import time

# マスのサイズ
MAS_SIZE = 50
# ボードのサイズ〇x〇
BOARD_SIZE = 8
# ボードの中心
CENTER = [250, 270]
# 盤の枠線の左上の座標 x1, y2, 右下の座標 x2, y2 を格納した辞書型配列
F = {"x1":CENTER[0]-BOARD_SIZE*MAS_SIZE/2, "y1":CENTER[1]-BOARD_SIZE*MAS_SIZE/2, "x2":CENTER[0]+BOARD_SIZE*MAS_SIZE/2, "y2":CENTER[1]+BOARD_SIZE*MAS_SIZE/2}
# 盤の色
BG1 = "wheat"
BG2 = "chocolate"
# マウスカーソル上のマスの色
MC = "gray"
# 移動可能なマスの色
CC1 = "red"
CC2 = "red"

class GraphicalChess(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Chess")
        master.geometry("+100+40")
        self.pack()
        self._init()

    def _init(self):
        # チェスを処理するためのクラスを呼ぶ
        self.chess = Chess_Board()

        # ウィンドウの枠組みを作る
        self.main_frame = tk.Frame(self, height=500, width=500)
        self.main_frame.pack()
        self.text_frame = tk.Frame(self.main_frame, height=60, width=600)
        self.text_frame.pack(side=tk.BOTTOM)
        self.left_frame = tk.Frame(self.main_frame, height=500, width=100)
        self.left_frame.pack(side=tk.RIGHT)
        self.button_frame = tk.Frame(self.left_frame, height=100, width=100)
        self.button_frame.pack()
        self.list_frame = tk.Frame(self.left_frame, height=400, width=100)
        self.list_frame.pack()
        self.canvas = tk.Canvas(self.main_frame, height=500, width=500)
        self.canvas.pack(side=tk.LEFT)
        self._openImage()

        # チェスのロゴ
        self.canvas.create_text(325, 30, font=('MV Boli', '20', 'underline'), text="Python Chess")
        
        # 盤の作成
        self.mas = [[0 for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
        self.stone = [[0 for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1, y1, = F["x1"] + j * MAS_SIZE, F["y1"] + i * MAS_SIZE
                x2, y2 = x1 + MAS_SIZE, y1 + MAS_SIZE
                if (i+j) % 2 == 0:
                    self.mas[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=BG1)
                else:
                    self.mas[i][j] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=BG2)

        # 盤の座標表記
        f = ('Century', '13', 'bold')
        for i in range(BOARD_SIZE):
            self.canvas.create_text(F["x1"]+(MAS_SIZE/2+MAS_SIZE*i), F["y1"]-12, font=f, text=chr(i+ord('a')))
            self.canvas.create_text(F["x1"]-12, F["y2"]-(MAS_SIZE/2+MAS_SIZE*i), font=f, text=i+1)

        self.canvas.bind("<Button-1>", self._clicked)
        self.canvas.bind("<Motion>", self._moved)

        # ボタン
        self.button = tk.Button(self.button_frame, text="Start", command=self.start)

        # ウィンドウ下部にテキストを表示する枠を用意
        self.msg = tk.StringVar()
        f = ('ＭＳ明朝', '14', 'bold')
        self.label = tk.Label(self.text_frame, textvariable=self.msg, font=f, relief="sunken", width=50)
        self.msg.set("Pythonでチェス！")

        # スクロールバー付きのリストボックスを作成する。
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT,fill="y")
        self.list_box = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set, width=15, height=20)
        self.scrollbar.config(command=self.list_box.yview)

        # キャンバス、リストボックス、ラベルをウィンドウに取り付ける。
        self.button.pack(side=tk.TOP)
        self.list_box.pack(side=tk.LEFT)
        self.label.pack(side=tk.BOTTOM)
        self.lboard = []

        self.lmouse = [0, 0, BG1]
        self.count = 0
        self.x, self.y = -1, -1

    def _board_position(self, x, y):
        # キャンバス上での座標をボードのマス基準の座標に変換する。
        x = (x - F["x1"]) // MAS_SIZE
        y = (y - F["y1"]) // MAS_SIZE
        return int(x), int(y)

    def start(self):
        self.button.configure(state='disable')
        self.update()
        self.game()

    def game(self):
        self.chess.makeList()
        self.showmPiece()
        #x, y = self.getMouse()
        #self.showCheck(x, y)
        #self.game()

    def _canvas_position(self, x, y):
        # マス基準の座標をキャンバス上におけるそのマスの中心値に変換する。
        x = F["x1"] + MAS_SIZE/2 + MAS_SIZE * x
        y = F["y1"] + MAS_SIZE/2 + MAS_SIZE * y
        return x, y

    def _clicked(self, e):
        self.x, self.y = e.x, e.y
        print(e.x, e.y)

    def _moved(self, e):
        # マウスが動いたときの処理
        if 0 <= self.lmouse[0] < BOARD_SIZE and 0 <= self.lmouse[1] < BOARD_SIZE:
            # 色を変えていたマスの色を戻す。
            self._set_bgcolor(self.lmouse[1], self.lmouse[0], self.lmouse[2])
        x, y = self._board_position(e.x, e.y)
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            # マウスカーソル上のマスの色を変える。
            self.lmouse = [x, y, self.canvas.itemcget(self.mas[y][x], "fill")]
            self._setbgcolor(y, x, MC)

    def _set_bgcolor(self, y, x, color):
        # (x, y)のマスの色をcolorにする。マウスカーソル上のマスだったなら、保存している色を更新する。
        if [self.lmouse[0], self.lmouse[1]] == [x, y]:
            self.lmouse[2] = color
        self._setbgcolor(y, x, color)
    
    def _setbgcolor(self, y, x, color):
        # (x, y)のマスの色をcolorにする。
        self.canvas.itemconfigure(self.mas[y][x], fill=color)

    def update(self):
        time.sleep(0.1)
        self.show()

    def _openImage(self):
        self.file = []
        for i in range(12):
            image = Image.open("image/chess"+str(i)+".png")
            self.file.append(ImageTk.PhotoImage(image))

    def resetColor(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if (x+y)%2 == 0:
                    self._setbgcolor(y, x, BG1)
                else:
                    self._setbgcolor(y, x, BG2)

    def showmPiece(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self.chess.inmList(x, y):
                    if (x+y)%2 == 0:
                        self._setbgcolor(y, x, CC1)
                    else:
                        self._setbgcolor(y, x, CC2)

    def getMouse(self):
        x, y =  self._board_position(self.x, self.y)
        self.x, self.y = -1, -1
        return x, y

    def showCheck(self, x, y):
        self.resetColor()
        i = self.chess.board[y][x]
        li = self.chess.clist[i]
        for a in li:
            x, y = a[0], a[1]
            if self.chess.incList(x, y):
                if (x+y)%2 == 0:
                    self._setbgcolor(y, x, CC1)
                else:
                    self._setbgcolor(y, x, CC2)

    def show(self):
        """盤に駒を表示する"""
        self.resetColor()
        self.canvas.delete("piece")
        self.image = []
        for y1, a in enumerate(self.chess.getpList()):
            for x1, b in enumerate(a):
                if 0 <= b < 12:
                    x, y = self._canvas_position(x1, y1)
                    self.image.append(self.canvas.create_image(x, y, image=self.file[b], tag="piece"))

    def append_list(self, text):
        """リストの末尾に要素textを追加する。"""
        self.list_box.insert(tk.END, text)
        self.list_box.yview_scroll(1, "units")

    def del_list(self):
        """リストの要素をすべて消す。"""
        self.list_box.delete(0, tk.END)



if __name__=='__main__':
    root = tk.Tk()
    game = GraphicalChess(master=root)
    game.mainloop()