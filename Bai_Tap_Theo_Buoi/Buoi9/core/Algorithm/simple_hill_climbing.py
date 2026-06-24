import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g

# Thuật toán Simple Hill Climbing
def SHC(problem_ma_trix):

    """
    Thuật toán Simple Hill Climbing
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
    #Lấy giá trị lớn nhất có lượt đầu
    node.cost = manhattan(problem_ma_trix)
    cur_node = node
    if cur_node.isGoal():
        return solution(cur_node)

    while True:
        g.tk_da_duyet += 1
        #Kiểm tra xem có con nhỏ hơn không 
        check = False

        for child in cur_node.expand():
            child_val = manhattan(child.ma_tran)
            
            if child_val < cur_node.cost:
                child.cost = child_val 
                cur_node = child
                check = True
                if child.isGoal():
                    return solution(child)
                break
        if check == False:
            return False 

    
        
        
    
