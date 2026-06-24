from collections import deque
from core.belief_node import BeliefNode
from core import globals as g
from core.ulities import solution

def bfs_belief_state(start_matrices, goal_matrix=None):

    if start_matrices and type(start_matrices[0][0]) is int:
        start_matrices = [start_matrices]
        
    # Chỉ xử lý ép kiểu mảng cho goal_matrix nếu nó tồn tại
    if goal_matrix is not None and type(goal_matrix[0][0]) is int:
        goal_matrix = [goal_matrix]

    init_node = BeliefNode(start_matrices)

    if init_node.isGoal(goal_matrix):
        return solution(init_node)
    
    frontier = deque([init_node])
    explored = set()
    state_frontier = set([init_node.get_key()])

    while len(frontier) > 0:
        
        node_hien_tai = frontier.popleft()
        g.tk_da_duyet += 1

        current_key = node_hien_tai.get_key()
        explored.add(current_key)
        state_frontier.remove(current_key)

        for child in node_hien_tai.expand(goal_matrix):
            child_key = child.get_key()
            if child_key not in explored and child_key not in state_frontier:
                if child.isGoal(goal_matrix):
                    return solution(child)
                
                frontier.append(child)
                state_frontier.add(child_key)
                
    return False