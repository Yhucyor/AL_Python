from collections import deque
import copy
from core.node import Node
from core.csp_puzzle import CSP_Puzzle
from core import globals as g

def arc_consistency_3(problem_matrix):
    csp = CSP_Puzzle()
    
    queue = deque()
    for xi in csp.variables:
        for xj in csp.variables:
            if xi != xj:
                queue.append((xi, xj))
                g.tk_sinh_ra += 1
    
    while queue:
        xi, xj = queue.popleft()
        g.tk_da_duyet += 1
        
        if csp.rm_inconsistent_values(xi, xj):
            if len(csp.domains[xi]) == 0:
                return False
            
            for xk in csp.neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))
                    g.tk_sinh_ra += 1
    
    #Thực hiện hiển thị lời giải 
    nodes = []
    state = [[-1]*3 for _ in range(3)]
    nodes.append(Node(state, None, "Init", 0, 0, 0))
    
    for i, var in enumerate(csp.variables):
        val = csp.domains[var][0]
        state = copy.deepcopy(state)
        state[var[0]][var[1]] = val
        nodes.append(Node(state, nodes[-1], f"x{var[0]*3+var[1]+1}={val}", i+1, 0, 0))
    
    return nodes
