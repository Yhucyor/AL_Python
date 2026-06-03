from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
# ====== Thuật toán BFS2 ======
def BFS2(problem_mat_trix):
    #global tk_da_duyet

    node = Node(problem_mat_trix)   
    if node.isGoal():
        return solution(node)
    frontier = deque([node])
    explored = set()
    state_frontier = set([str(node.ma_tran)])
    while len(frontier):
        node = frontier.popleft()
        g.tk_da_duyet += 1
        explored.add(str(node.ma_tran))
        state_frontier.remove(str(node.ma_tran))
        for child in node.expand():
            if str(child.ma_tran) not in explored and str(child.ma_tran) not in state_frontier:
                if child.isGoal():
                    return solution(child) 
                frontier.append(child)
                state_frontier.add(str(child.ma_tran))
    return False  