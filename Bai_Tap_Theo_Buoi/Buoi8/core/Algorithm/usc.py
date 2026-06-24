import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
from core.globals import goal_ma_tran

def UCS(problem_ma_tran):
    

    def chi_phi(ma_tran):
        cost = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if ma_tran[i][j] != goal_ma_tran[i][j]:
                    cost += 1
        return cost 
       
    node = Node(problem_ma_tran)
    node.cost = 0

    frontier = []
    heapq.heappush(frontier, node)
    reached = {str(node.ma_tran): node.cost}


    while len(frontier):
        node = heapq.heappop(frontier)
        g.tk_da_duyet += 1

        if node.isGoal():
            return solution(node)
        
        for child in node.expand():
            child.cost = node.cost + chi_phi(child.ma_tran)
            state_child = str(child.ma_tran)
            if state_child not in reached or child.cost < reached[state_child]:
                reached[state_child] = child.cost
                heapq.heappush(frontier, child)

    return False