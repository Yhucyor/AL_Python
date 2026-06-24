from core import globals as g
from core.puzzle_csp2 import Puzzle_CSP
from core.node import Node

def _backtracking_forward_search(csp):
    return backtrack_fc({}, csp)

def backtracking_forward_search(problem_matrix):
    csp = Puzzle_CSP(problem_matrix)
    assignment = _backtracking_forward_search(csp)

    if assignment:
        nodes = []
        state = [[-1]*3 for _ in range(3)]
        nodes.append(Node(state, None, "Init", 0, 0, 0))
        
        for idx, (var, val) in enumerate(assignment.items()):
            state = [row[:] for row in state]
            state[var[0]][var[1]] = val
            nodes.append(Node(state, nodes[-1], f"x{var[0]*3+var[1]+1}={val}", idx+1, 0, 0))
        return nodes
    return False

def backtrack_fc(assignment, csp):
    if csp.is_complete(assignment):
        return assignment

    var = csp.select_unassigned_var(assignment)

    if var is None:
        return None
    
    for val in csp.domain_values(var, assignment):
        g.tk_sinh_ra += 1
        if csp.is_consistent(var, val, assignment):
            assignment[var] = val
            removed = csp.forward_check(var, val, assignment)
            if removed is not False:
                g.tk_da_duyet += 1
                result = backtrack_fc(assignment, csp)
                if result is not None:
                    return result
            csp.restore(removed)
            del assignment[var]

    return None