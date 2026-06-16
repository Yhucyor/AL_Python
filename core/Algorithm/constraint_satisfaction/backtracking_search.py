
from core.node import Node
from collections import deque
from core.ulities import solution
from core import globals as g
from core.puzzle_csp import Puzzle_CSP

def _backtracking_search(csp):
    return backtrack({}, csp)

def backtracking_search(problem_matrix):
    csp = Puzzle_CSP(problem_matrix, max_depth = 15)
    assignment = _backtracking_search(csp)
    if assignment:
        return [assignment[i] for i in sorted(assignment.keys())]
    return False

def backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment
    
    var = csp.select_unassigned_var(assignment)
    if var is None:
        return None
    
    for val in csp.domain_values(var, assignment):
        if csp.is_consistent(var, val, assignment):
            assignment[var] = val
            g.tk_da_duyet += 1

            result = backtrack(assignment, csp)
            if result is not None:
                return result
            
            del assignment[var]
    
    return None

