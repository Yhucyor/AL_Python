import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g

def A_Star(problem_ma_tran):
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
                value = ma_tran[i][j]
                if value != 0:
                    for i_m in range(0, 3):
                        for j_m in range(0, 3):
                            if value == g.goal_ma_tran[i_m][j_m]:
                                h_value += abs(i - i_m) + abs(j - j_m)
                                break
        return h_value
    
    s_node = Node(problem_ma_tran)
    s_node.g = 0
    s_node.h = h(problem_ma_tran)
    s_node.cost = s_node.g + s_node.h
    
    frontier = []
    heapq.heappush(frontier, s_node)
    frontier_dict = {str(s_node.ma_tran): s_node.g}
    reached = {}
    
    while len(frontier) > 0:
        node = heapq.heappop(frontier)
        cur_state = str(node.ma_tran)
        
        if cur_state in frontier_dict:
            del frontier_dict[cur_state]
        
        g.tk_da_duyet += 1
        
        if node.isGoal():
            return solution(node)
        
        reached[cur_state] = node.g
        
        for child in node.expand():
            child.g = node.g + mis_g(child.ma_tran)
            child.h = h(child.ma_tran)
            child.cost = child.g + child.h
            
            child_state = str(child.ma_tran)
            
            if child_state in reached and reached[child_state] <= child.g:
                continue
            
            if child_state in frontier_dict and frontier_dict[child_state] <= child.g:
                continue
            
            heapq.heappush(frontier, child)
            frontier_dict[child_state] = child.g
    
    return False
