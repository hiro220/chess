# coding:utf-8

from piece import Chess_Piece
import copy

# 定義
BOARD_SIZE = 8
B_PAWN = 0
B_ROOK = 1
B_KNIGHT = 2
B_BISHOP = 3
B_QUEEN = 4
B_KING = 5
W_PAWN = 6
W_ROOK = 7
W_KNIGHT = 8
W_BISHOP = 9
W_QUEEN = 10
W_KING = 11
BLACK = 1
WHITE = -1
NONE = 20

class Chess_Board:
    def __init__(self):
        # 初期化
        self.turn = WHITE   # 先手は白
        self._makePiece()
        self._makeBoaed()
        self._makeDummy()
        self.lmove = 0
    
    def chenge_turn(self):
        # 手番を変える
        self.turn *= -1

    def _makePiece(self):
        # 使う駒のリストを作る
        self.plist = []
        blist = [B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_BISHOP, B_KNIGHT, B_ROOK]
        wlist = [W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_BISHOP, W_KNIGHT, W_ROOK]
        i = 0
        self.plist.append(Chess_Piece(NONE)) # 駒がないことを表すダミー
        for a in blist:
            i += 1
            self.plist.append(Chess_Piece(a))
        for j in range(BOARD_SIZE):
            i += 1
            self.plist.append(Chess_Piece(B_PAWN))
        for j in range(BOARD_SIZE):
            i += 1
            self.plist.append(Chess_Piece(W_PAWN))
        for a in wlist:
            i += 1
            self.plist.append(Chess_Piece(a))
    
    def _makeBoaed(self):
        # ボードには駒のIDを保存しておく
        self.board = [[0 for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            self.board[0][i] = i + 1
            self.board[1][i] = i + 1 + BOARD_SIZE
            self.board[BOARD_SIZE-1][i] = i + 1 + BOARD_SIZE * 3
            self.board[BOARD_SIZE-2][i] = i + 1 + BOARD_SIZE * 2

    def _makeDummy(self):
        # ボードをもう一つ計算用に用意する。
        self.dummy = copy.deepcopy(self.board)

    def getPosition(self, i):
        # 引数で指定したIDの駒があるマスを返却する。
        for y, a in enumerate(self.board):
            for x, b in enumerate(a):
                if b == i:
                    return x, y

    def promotion(self, i, piece):
        # 引数で指定したIDの駒をpieceにする。
        self.plist[i].setPiece(piece)

    def getpList(self):
        """ボードの駒の情報を返却する"""
        li = [[0 for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                i = self.board[y][x]
                li[y][x] = self.plist[i].getPiece()
        return li

    def move(self, i, x, y):
        # iの駒を(x, y)に移動させる。
        lx, ly = self.getPosition(i)
        self.plist[i].move()
        self.board[ly][lx] = 0
        if self.board[y][x] != 0:
            self.plist[self.board[y][x]].deactivate()
        self.board[y][x] = i

    def makeList(self):
        # チェックリストと動かせる駒のリストを作成する。
        self.makecList()
        self.makemList()

    def makecList(self):
        # チェックをかけている駒と、かかっている場所のリストを作る
        self.clist = []
        for i, p in enumerate(self.plist):
            if not p.isActivate():
                # 駒が盤面に残っていないならスルー。
                self.clist.append([])
                continue
            color = p.getColor()
            clist = []
            x, y = self.getPosition(i)
            if color == self.turn:
                piece = p.getPiece()
                piece = piece % 6   # pieceの値をすべてBLACKで考える。
                if piece == B_ROOK: # ルークのとき
                    dif = [[1,0],[-1,0],[0,1],[0,-1]]
                    for a in dif:
                        clist += self.recursionCheck(x, y, a[0], a[1])
                elif piece == B_KNIGHT: # ナイトのとき
                    dif = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
                    for a in dif:
                        clist += self.simpleCheck(x, y, a[0], a[1])
                elif piece == B_BISHOP: # ビショップのとき
                    dif = [[1,1],[1,-1],[-1,1],[-1,-1]]
                    for a in dif:
                        clist += self.recursionCheck(x, y, a[0], a[1])
                elif piece == B_QUEEN: # クイーンのとき
                    dif = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                    for a in dif:
                        clist += self.recursionCheck(x, y, a[0], a[1])
                elif piece == B_KING: # キングのとき
                    dif = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                    for a in dif:
                        clist += self.simpleCheck(x, y, a[0], a[1])
                        # キャスリングはとりあえず放置
                elif piece == B_PAWN:
                    # ポーンは動きが例外
                    clist += self.pawnCheck(x, y)
            self.clist.append(clist)
            # あと、駒を動かしたことによるチェックも放置

    def pawnCheck(self, x, y):
        # ポーン用のチェック探索
        i = self.board[y][x]
        li = []
        num = 1
        if not self.plist[i].ismove():
            num += 1
        for a in range(num):
            y += self.turn
            if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
                i = self.board[y][x]
                if self.plist[i].getColor() == NONE:
                    li.append([x, y])
            if a == 0:
                for b in [1, -1]:
                    x1 = x + b
                    if (0 <= x1 < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
                        i = self.board[y][x1]
                        color = self.plist[i].getColor()
                        if (color != self.turn) and (color != NONE):
                            li.append([x1, y])
        return li

    def recursionCheck(self, x, y, dx, dy):
        # 再帰的に呼び出してチェックをかけられるか調べる。
        x += dx
        y += dy
        if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
            i = self.board[y][x]
            color = self.plist[i].getColor()
            if color == NONE:
                return [[x, y]] + self.recursionCheck(x, y, dx, dy)
            elif color == self.turn:
                return []
            else:
                return [[x, y]]
        return []

    def simpleCheck(self, x, y, dx, dy):
        # 指定したマスにチェックをかけられるか調べる。
        x += dx
        y += dy
        if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
            i = self.board[y][x]
            color = self.plist[i].getColor()
            if color != self.turn:
                return [[x, y]]
            else:
                return []
        return []

    def incList(self, x, y):
        # 指定したマスに駒がチェックをかけているか
        for a in self.clist:
            if [x, y] in a:
                return True
        return False

    def checked(self, i, x, y):
        return [x, y] in self.clist[i]

    def makemList(self):
        # 動かせる駒のリストを作る。
        self.mlist = []
        for i, p in enumerate(self.plist):
            if len(self.clist[i]) != 0:
                self.mlist.append(i)

    def inmList(self, x, y):
        # 指定したマスの駒が動けるか
        return self.board[y][x] in self.mlist

    def getPiece(self, x, y):
        # ボード(x, y)の駒のIDを返却。
        return self.board[y][x]

if __name__=='__main__':
    test = Chess_Board()
    for a in test.board:
        for b in a:
            print(test.plist[b].getPiece(), end=' ')
        print()
    test.makeList()
    test.move(1, 4,4)
    print(test.board)
    print(test.dummy)
    print(test.mlist)
    print(test.clist)
    print(test.incList(0,5))