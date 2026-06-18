import random
from core.node import Node
from core.csp_puzzle import CSP_Puzzle
from core import globals as g

def min_conflicts(problem_matrix, max_steps=1000):
    csp = CSP_Puzzle()
    current = csp.assignment_from_state(problem_matrix)
    
    path = []
    path.append(Node(problem_matrix, None, "Init", 0, 0, 0))
    
    for step in range(1, max_steps + 1):
        g.tk_sinh_ra += 1
        
        if csp.is_solution(current):
            return path
        
        conflicted = [v for v in csp.variables if csp.count_conflicts(v, current[v], current) > 0]
        if not conflicted:
            return False
        
        var = random.choice(conflicted)
        min_conf = min(csp.count_conflicts(var, v, current) for v in range(9))
        best = [v for v in range(9) if csp.count_conflicts(var, v, current) == min_conf]
        
        current[var] = random.choice(best)
        g.tk_da_duyet += 1
        
        path.append(Node(csp.state_from_assignment(current), path[-1], f"x{var[0]*3+var[1]+1}={current[var]}", step, 0, 0))
    
    return False
