from collections import deque

from core.node import Node
from core.puzzle import solution

#Thuật toán BFS1
def BFS1(problem_ma_tran):
    node = Node(problem_ma_tran)
    frontier = deque([node])
    reached = set([str(node.ma_tran)])

    while len(frontier):
        node = frontier.popleft()
        if node.isGoal():
            return solution(node)
        reached.add(str(node.ma_tran))
        for i in node.expand():
            state_child = str(i.ma_tran)
            if state_child not in reached:
                frontier.append(i)
                reached.add(state_child)

    return False

#Thuật toán BFS2
def BFS2(problem_mat_trix):
    node = Node(problem_mat_trix)   
    if node.isGoal():
        return solution(node)
    frontier = deque([node])
    explored = set()
    state_frontier = set([str(node.ma_tran)])
    while len(frontier):
        node = frontier.popleft()
        explored.add(str(node.ma_tran))
        state_frontier.remove(str(node.ma_tran))
        for child in node.expand():
            if str(child.ma_tran) not in explored and str(child.ma_tran) not in state_frontier:
                if child.isGoal():
                    return solution(child) 
                frontier.append(child)
                state_frontier.add(str(child.ma_tran))
    return False    