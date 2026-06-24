from core.belief_node import BeliefNode
from core.ulities import solution
from core import globals as g
from itertools import permutations

def resolve_hidden(matrix):
    seen = set()
    hidden = []
    
    for i in range(3):
        for j in range(3):
            val = matrix[i][j]
            if val != -1:
                seen.add(val)
            else:
                hidden.append((i, j))
                
    miss = [x for x in range(9) if x not in seen]
    if not hidden:
        return [matrix]
    res = []
    for p in permutations(miss):
        temp = [row[:] for row in matrix]
        for idx, (r, c) in enumerate(hidden):
            temp[r][c] = p[idx]
        res.append(temp)

    return res


# ====== Thuật toán DFS cho Môi trường quan sát một phần ======
def dfs_partial_state(problem_matrix, goal_matrix=None):

    if problem_matrix and type(problem_matrix[0][0]) is list:
        problem_matrix = problem_matrix[0]

    if goal_matrix is not None:
        if type(goal_matrix[0][0]) is int:
            goal_matrix = resolve_hidden(goal_matrix)
        else:
            resolved_goals = []
            for gl in goal_matrix:
                resolved_goals += resolve_hidden(gl)
            goal_matrix = resolved_goals

    start_mats = resolve_hidden(problem_matrix)

    node = BeliefNode(tap_ma_tran=start_mats)
    
    if node.isGoal(goal_matrix):
        return solution(node)
        
    frontier = [node]
    reached = {node.get_key()}
    frontier_states = {node.get_key()}
    
    while len(frontier):
        node = frontier.pop() 
        g.tk_da_duyet += 1
        
        frontier_states.discard(node.get_key())
        
        for child in node.expand(goal_matrix):
            if child.isGoal(goal_matrix):
                return solution(child) 
                
            child_key = child.get_key()
        
            if child_key not in reached and child_key not in frontier_states:
                frontier.append(child)
                frontier_states.add(child_key)
                reached.add(child_key)
                
    return False