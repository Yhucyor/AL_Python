from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
# ====== Thuật toán BFS1 ======
def BFS1(problem_ma_tran):

    node = Node(problem_ma_tran)
    frontier = deque([node])
    reached = set([str(node.ma_tran)])

    while len(frontier):
        node = frontier.popleft()
        g.tk_da_duyet += 1
        if node.isGoal():
            return solution(node)
        reached.add(str(node.ma_tran))
        for i in node.expand():
            state_child = str(i.ma_tran)
            if state_child not in reached:
                frontier.append(i)
                reached.add(state_child)

    return False