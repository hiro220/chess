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
TR = 0
CONTINUE = 2

class Log:
    def __init__(self):
        self.log = []

    def add(self, i, lx, ly, x, y):
        self.log.insert(0, [i, lx, ly, x, y])

    def get(self):
        if self.log:
            return self.log[0]

    def clear(self):
        self.log.clear()


class Threefold_Repetition:
    """千日手に対する処理を行うクラス"""
    def __init__(self):
        self.queue = [0 for i in range(4)]
        self.count = 0

    def add(self, item):
        # 引数itemに行動を入力する。
        self.queue.append(item)
        if item == self.queue.pop(0):
            self.count += 1
        else:
            self.count = 0

    def isTR(self):
        # addの直後に呼ぶ。千日手ならTrueが返る。
        return self.count == 6

class Chess_Board:
    def __init__(self):
        # 初期化
        self.reset()
        self.searchKing()
        self.log = Log()

    def reset(self):
        self.turn = WHITE   # 先手は白
        self._makePiece()
        self._makeBoaed()
        self.lmove = 0
        self.tr = Threefold_Repetition()
    
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

    def chenge_turn(self):
        # 手番を変える
        self.turn *= -1
        #self.searchKing()

    def searchKing(self):
        if self.turn == BLACK:
            piece = B_KING
        else:
            piece = W_KING 
        for i, p in enumerate(self.plist):
            if p.getPiece() == piece:
                x, y = self.getPosition(i)
                self.kingPosition = [x, y]
                return

    def getPosition(self, i):
        """ 引数で指定したIDの駒があるマスを返却する。
        return x, y"""
        for y, a in enumerate(self.board):
            for x, b in enumerate(a):
                if b == i:
                    return x, y

    def getPiece(self, x, y):
        # ボード(x, y)の駒のIDを返却。
        return self.board[y][x]

    def promotion(self, i, piece):
        # 引数で指定したIDの駒をpieceにする。"
        if piece == "rook":
            piece = B_ROOK
        if piece == "bishop":
            piece = B_BISHOP
        if piece == "knight":
            piece = B_KNIGHT
        if piece == "queen":
            piece = B_QUEEN
        if self.turn == WHITE:
            piece += 6
        self.plist[i].setPiece(piece)

    def getpList(self):
        """ボードの駒の情報を返却する"""
        li = [[0 for i in range(BOARD_SIZE)]for j in range(BOARD_SIZE)]
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                i = self.board[y][x]
                li[y][x] = self.plist[i].getPiece()
        return li

    def _move(self, i, x, y):
        # iの駒を(x, y)に移動させる。(仮)
        lx, ly = self.getPosition(i)
        self.board[ly][lx] = 0
        if self.board[y][x] != 0:
            self.plist[self.board[y][x]].deactivate()
        self.board[y][x] = i

    def move(self, i, x, y):
        # 実質の駒移動
        x1, y1 = self.getPosition(i)
        self.enpassant(i, x, y)
        self._move(i, x, y)
        self.plist[i].move()
        self.tr.add([i, x, y])
        self.log.add(i, x1, y1, x, y)
        if self.plist[i].getPiece() % 6 == B_KING: # i がキング
            # caslingのときの処理
            if not (-1 <= x-x1 <= 1):
                if x > x1:
                    self._move(i+3, x-1, y)
                    self.plist[i+3].move()
                else:
                    self._move(i-4, x+1, y)
                    self.plist[i-4].move()

    def enpassant(self, i, x, y):
        if not self.plist[i].getPiece() % 6 == B_PAWN:
            return False
        lx, ly = self.getPosition(i)
        if x - lx == 0:
            return False
        if self.board[y][x] == 0:
            pre = self.log.get()
            i, prex, prey = pre[0], pre[3], pre[4]
            self.plist[i].deactivate()
            self.board[prey][prex] = 0
            return True
        return False

    def makeList(self):
        # チェックリストと動かせる駒のリストを作成する。
        self.clist = self.makecList()
        self.makemList()

    def makemList(self):
        # 動かせる駒のリストを作る。
        self.mlist = []
        for i, p in enumerate(self.plist):
            if len(self.clist[i]) != 0:
                self.mlist.append(i)

    def makecList(self, rival=False):
        # チェックをかけている駒と、かかっている場所のリストを作る
        tmplist = []
        if rival:
            turn = self.turn * (-1)
        else:
            turn = self.turn
        for i, p in enumerate(self.plist):
            if not p.isActivate():
                # その駒が盤面に残っていないなら空のリストを追加するだけ。
                tmplist.append([])
                continue
            color = p.getColor()
            clist = []
            x, y = self.getPosition(i)
            if color == turn:
                piece = p.getPiece()
                piece = piece % 6   # pieceの値をすべてBLACKで考える。
                if piece == B_KING: # キングのとき
                    dif = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
                    for a in dif:
                        clist += self.simpleCheck(x, y, a[0], a[1], rival)
                        clist += self.casling(rival)
                        # キャスリングはとりあえず放置
                elif piece == B_PAWN:
                    # ポーンは動きが例外
                    clist += self.pawnCheck(x, y, rival)
                else:
                    single, dif = p.movingPosition() # 現在確認している駒の動き方を取得
                    for mas in dif:
                        if single:
                            clist += self.simpleCheck(x, y, mas[0], mas[1], rival)
                        else:
                            clist += self.recursionCheck(i, x, y, mas[0], mas[1], rival)

            tmplist.append(clist)
        return tmplist
            # あと、駒を動かしたことによるチェックも放置

    def pawnCheck(self, x, y, rival):
        # ポーン用のチェック探索
        index = self.board[y][x] # ポーンの位置をindexに格納
        li = []
        num = 1
        li += self.enpassantCheck(x, y)
        if (not self.plist[index].ismove()) and (not rival):
            # ポーンが動いていない、かつその手番のチェック
            num += 1
        for a in range(num):
            # チェック対象となるターンを設定
            if rival:
                turn = self.turn * (-1)
            else:
                turn = self.turn
            y += turn
            # 斜め前に駒がある場合移動可能
            if a == 0:
                for b in [1, -1]:
                    x1 = x + b
                    if (0 <= x1 < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
                        i = self.board[y][x1]
                        color = self.plist[i].getColor()
                        if ((color != turn) and (color != NONE)) or rival:
                            # 移動先に相手の駒がある、もしくは確認用チェック
                            if not rival:
                                # 確認用でない場合
                                rclist = self.rivalCheck(index, x1, y)
                                if self.kingPosition not in rclist:
                                    # キングにチェックがかかっていない
                                    li += [[x1, y]]
                            else:
                                # 確認用
                                li += [[x1, y]]
            # 前方移動
            if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE) and (not rival):
                i = self.board[y][x]
                if (self.plist[i].getColor() == NONE):
                    # 移動先に駒がない、かつ確認用
                    rclist = self.rivalCheck(index, x, y)
                    if self.kingPosition not in rclist:
                        # キングにチェックがかかっていない
                        li += [[x, y]]
                else:
                    # 移動先にどちらかの駒がある
                    break
        return li

    def enpassantCheck(self, x, y):
        pre = self.log.get()
        li = []
        if not pre:
            return li
        dif = abs(pre[2] - pre[4])
        piece = self.plist[pre[0]].getPiece()
        if (piece % 6 == B_PAWN) and (dif == 2):
            if (abs(x - pre[3]) == 1) and (y - pre[4] == 0):
                x = pre[3]
                y = (pre[2] + pre[4]) // 2
                li += [[x, y]]
        return li

    def recursionCheck(self, index, x, y, dx, dy, rival):
        # 再帰的に呼び出してチェックをかけられるか調べる。
        x += dx
        y += dy
        if rival:
            turn = self.turn * (-1)
            self.searchKing()
        else:
            turn = self.turn
        if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
            i = self.board[y][x]
            color = self.plist[i].getColor()
            if color == turn:
                # 移動先に自分の駒がある
                return []
            elif not rival:
                # 確認用でない
                rclist = self.rivalCheck(index, x, y)
                if color == NONE:
                    if self.kingPosition not in rclist:
                        return [[x, y]] + self.recursionCheck(index, x, y, dx, dy, rival)
                    else:
                        return self.recursionCheck(index, x, y, dx, dy, rival)
                else:
                    if self.kingPosition not in rclist:
                        return [[x, y]]
                    else:
                        return []
            else:
                if color == NONE:
                    return [[x, y]] + self.recursionCheck(index, x, y, dx, dy, rival)
                else:
                    return [[x, y]]
        return []

    def simpleCheck(self, x, y, dx, dy, rival):
        # 指定したマスにチェックをかけられるか調べる。
        index = self.board[y][x]
        x += dx
        y += dy
        if rival:
            turn = self.turn * (-1)
            self.searchKing()
        else:
            turn = self.turn
        if (0 <= x < BOARD_SIZE) and (0 <= y < BOARD_SIZE):
            i = self.board[y][x]
            color = self.plist[i].getColor()
            if color != turn:
                if not rival:
                    rclist = self.rivalCheck(index, x, y)
                    if self.kingPosition not in rclist:
                        return [[x, y]]
                    else:
                        return []
                else:
                    return [[x, y]]
        return []

    def casling(self, rival):
        if rival:
            return []
        self.searchKing()
        x, y = self.kingPosition[0], self.kingPosition[1]
        index = self.getPiece(x, y)
        li = []
        if self.plist[index].ismove(): # キングが動いているか
            return []
        # 右方探索
        flag = True
        if not self.plist[index+3].ismove(): # キング方向のルークが動いていないか
            for i in range(2):
                if len(self.simpleCheck(x, y, 1+i, 0, rival)) == 0:
                    flag = False
                    break
                rclist = self.rivalCheck(index, x+i+1, y)
                if [x, y] in rclist:
                    flag = False
                    break
            if flag:
                li.append([x+2, y])
        # 左方探索
        flag = True
        if not self.plist[index-4].ismove(): # クイーン方向のルークが動いていないか
            for i in range(3):
                if len(self.simpleCheck(x, y, -1-i, 0, rival)) == 0:
                    flag = False
                    break
                rclist = self.rivalCheck(index, x-i-1, y)
                if [x, y] in rclist:
                    flag = False
                    break
            if flag:
                li.append([x-3, y])
        return li

    def rivalCheck(self, i, x, y):
        lx, ly = self.getPosition(i) # iのボード位置を取得
        lsti = self.board[y][x] # 移動させる駒の位置lstiを保持
        self._move(i, x, y) # 実際に駒を移動させる
        tmplist = self.makecList(rival=True) # 相手が駒で取ることができる位置のリストを取得
        self.board[y][x] = lsti # 移動して上書きした駒情報を戻す。
        self.board[ly][lx] = i # 移動元に駒を戻す。
        # deactivateにした駒をactivateにする。
        if self.board[y][x] != 0:
            self.plist[self.board[y][x]].activate()
        # plistの順番に対応したリストになっているtmplistを、ただの一重のリストにする。
        rclist = []
        for maslist in tmplist:
            for mas in maslist:
                if mas != []:
                    rclist.append(mas)
        return rclist

    def incList(self, x, y):
        # 指定したマスに駒がチェックをかけているか
        for a in self.clist:
            if [x, y] in a:
                return True
        return False

    def inmList(self, x, y):
        # 指定したマスの駒が動けるか
        return self.board[y][x] in self.mlist

    def checked(self, i, x, y):
        return [x, y] in self.clist[i]

    def checkResult(self):
        if self.tr.isTR():
            return TR
        elif len(self.mlist) == 0:
            return self.turn
        return CONTINUE

    def isPromotion(self, x, y):
        i = self.board[y][x]
        if self.plist[i].getPiece() % 6 == B_PAWN:
            y += self.turn
            return not (0 <= y < BOARD_SIZE)
        return False
        
if __name__=='__main__':
    test = Chess_Board()
    for a in test.board:
        for b in a:
            print(test.plist[b].getPiece(), end=' ')
        print()
    test.makeList()
    test.move(1, 4,4)
    print(test.board)
    print(test.mlist)
    print(test.clist)
    print(test.incList(0,5))