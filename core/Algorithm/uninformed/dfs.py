from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
# ====== Thuật toán DFS ======
def DFS(problem_mat_trix):

    node = Node(problem_mat_trix)   
    if node.isGoal():
        return solution(node)
    frontier = [node]
    reached = {str(node.ma_tran)}
    frontier_states = {str(node.ma_tran)}
    while len(frontier):
        node = frontier.pop()
        g.tk_da_duyet += 1
        frontier_states.discard(str(node.ma_tran))
        for child in node.expand():
            if child.isGoal():
                return solution(child) 
            if str(child.ma_tran) not in reached and str(child.ma_tran) not in frontier_states:
                frontier.append(child)
                frontier_states.add(str(child.ma_tran))
                reached.add(str(child.ma_tran))
    return False 