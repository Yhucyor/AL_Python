from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g

# ====== Thuật toán IDS ======
def IDS(problem_mat_trix):

    def is_cycle(node):
        node_parent = node.parent
        while node_parent is not None:
            if node_parent.ma_tran == node.ma_tran:
                return True
            node_parent = node_parent.parent
        return False
    
    def DLS(problem, depth):
        frontier = [Node(problem)]
        result = "failure"
        while len(frontier):
            node = frontier.pop()
            g.tk_da_duyet += 1
            if node.isGoal():
                return solution(node)
            if node.cost >= depth:
                result = "cutoff"
            elif not is_cycle(node):
                for child in node.expand():
                    frontier.append(child)
        return result
        
    #Có thể thay inf = 100 để giới hạn 
    for depth in range(0, 100):
        result = DLS(problem_mat_trix, depth)
        if result != "cutoff":
            if result == "failure":
                return False
            return result

    return False 