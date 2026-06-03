from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
import heapq
from core.globals import goal_ma_tran

# ====== Thuật toán Greedy Search ======
def Greedy_Search(problem_ma_tran):

    def heuristic(ma_tran):
        cost = 0
        for i in range(3):
            for j in range(3):
                if ma_tran[i][j] != goal_ma_tran[i][j]:
                    cost += 1
        return cost 
    
    node = Node(problem_ma_tran)
    value = heuristic(node.ma_tran)
    node.cost = value
    frontier = []
    heapq.heappush(frontier, (value, node))
    frontier_states = {str(node.ma_tran): value}
    reached = {}

    while len(frontier) > 0:
        v, node = heapq.heappop(frontier)
        ma_tran = str(node.ma_tran)
        if ma_tran in frontier_states:
            del frontier_states[ma_tran]
        g.tk_da_duyet += 1

        if node.isGoal():
            return solution(node)

        #Nếu khác Frontier thì ta có thể xem giá trị là bao nhiêu 
        if str(node.ma_tran) in reached and v >= reached[ma_tran]:
            continue 
        reached[ma_tran] = v

        for child in node.expand():
            child_ma_tran = str(child.ma_tran)
            v_con = heuristic(child.ma_tran)
            child.cost = v_con
            if child_ma_tran not in frontier_states and child_ma_tran not in reached:
                heapq.heappush(frontier, (v_con, child))
                frontier_states[child_ma_tran] = v_con
            elif child_ma_tran in frontier_states and v_con < frontier_states[child_ma_tran]:
                heapq.heappush(frontier, (v_con, child))
                frontier_states[child_ma_tran] = v_con
            elif child_ma_tran in reached and v_con < reached[child_ma_tran]:
                heapq.heappush(frontier, (v_con, child))
                frontier_states[child_ma_tran] = v_con
    return False