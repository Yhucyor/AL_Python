from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g

# ====== Thuật toán IDA ======
def IDA(problem_mat_trix):

    def mis_g(ma_tran):
        g_value = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if ma_tran[i][j] != g.goal_ma_tran[i][j]:
                    g_value += 1
        return g_value

    def h(ma_tran):
        h_value = 0
        for i in range(0, 3):
            for j in range(0, 3):
                i_m, j_m = 0, 0
                value = ma_tran[i][j]
                if value != 0:
                    for i_m in range(0, 3):
                        for j_m in range(0, 3):
                            if value == g.goal_ma_tran[i_m][j_m]:
                                h_value += abs(i - i_m) + abs(j - j_m)
                                break
        return h_value
    
    def is_cycle(node):
        node_parent = node.parent
        while node_parent is not None:
            if node_parent.ma_tran == node.ma_tran:
                return True
            node_parent = node_parent.parent
        return False
    
    def search(node, g_cost, limit):
        g.tk_da_duyet += 1
        f = g_cost + h(node.ma_tran)
        if f > limit:
            return "cutoff"
        if node.isGoal():
            return solution(node)
        result = "failure"
        for child in node.expand():
            if not is_cycle(child):
                child.g = g_cost + mis_g(child.ma_tran)
                child.h = h(child.ma_tran)
                child.cost = child.g + child.h
                t = search(child, child.g, limit)
                if t != "cutoff" and t != "failure":
                    return t
                if t == "cutoff":
                    result = "cutoff"
        return result
        
    node = Node(problem_mat_trix)
    limit = h(problem_mat_trix)
    
    for depth in range(limit, 100):
        result = search(node, 0, depth)
        if result != "cutoff":
            if result == "failure":
                return False
            return result
        limit += 1

    return False
