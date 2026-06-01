import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g

# Thuật toán Simple Hill Climbing
def SHC_Highest(problem_ma_trix):

    """
    Thuật toán Simple Hill Climbing Highest
    """
    #Hàm tính chi phí
    def manhattan(matrix):
        val = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if matrix[i][j] != 0:
                    for ix in range(0, 3):
                        for jy in range(0, 3):
                            if matrix[i][j] == g.goal_ma_tran[ix][jy]:
                                val += abs(i-ix) + abs(j - jy)
        return val
    
    node = Node(problem_ma_trix)
    node.cost = manhattan(problem_ma_trix)
    cur_node = node

    if cur_node.isGoal():
        return solution(cur_node)

    while True:
        g.tk_da_duyet += 1
        #Lưu lại vị trí nhỏ nhất
        min_node = cur_node
        tmp_val = cur_node.cost 

        for child in cur_node.expand():
            child_val = manhattan(child.ma_tran)
            child.cost = child_val
            
            if child.isGoal():
                return solution(child)
            if child_val < tmp_val:
                tmp_val = child_val
                min_node = child
            
        if min_node.ma_tran == cur_node.ma_tran:
            return False
        cur_node = min_node