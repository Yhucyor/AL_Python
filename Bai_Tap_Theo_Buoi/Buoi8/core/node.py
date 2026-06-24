from core.globals import goal_ma_tran
from core import globals as g

class Node():
    def __init__(self, ma_tran, parent = None, action = "_", cost = 0, g = 0, h = 0):
        self.ma_tran = ma_tran
        self.parent = parent 
        self.action = action
        self.cost = cost
        self.g = 0
        self.h = 0
        
    def isGoal(self):
        for i in range(3):
            for j in range(3):
                if self.ma_tran[i][j] != goal_ma_tran[i][j]:
                    return False
        return True 
    def blank(self):
        for i in range(3):
            for j in range(3):
                if self.ma_tran[i][j] == 0:
                    return (i, j)
        return (0, 0) 

    def expand(self):
        dxy = {"L": [0, -1], "R": [0, 1], "U":[-1, 0], "D": [1, 0]}
        x, y = self.blank()
        ma_tran_expand = []
        for i in dxy:
            new_x = x + dxy[i][0]
            new_y = y + dxy[i][1]
            if new_x >= 0 and new_x <= 2 and new_y >= 0 and new_y <= 2:
                tmp_ma_tran = [r[:] for r in self.ma_tran]
                tmp_ma_tran[x][y], tmp_ma_tran[new_x][new_y] = tmp_ma_tran[new_x][new_y], tmp_ma_tran[x][y]
                tmp_Node = Node(
                    tmp_ma_tran, 
                    parent = self,
                    action = i,
                    cost = self.cost + 1
                )
                ma_tran_expand.append(tmp_Node)
                g.tk_sinh_ra += 1
                
        return ma_tran_expand
    #Định nghĩa hàm so sánh
    def __lt__(self, node):
        return self.cost < node.cost 