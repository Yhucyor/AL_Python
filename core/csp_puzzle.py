from core import globals as g
from core.node import Node
import copy

class CSP_Puzzle:
    
    def __init__(self, init_state=None):
        self.variables = [(r, c) for r in range(3) for c in range(3)]
        self.domains = {var: list(range(9)) for var in self.variables}
        self.goal = g.goal_ma_tran
        
        #Có thể gán giá trị từ 0 - 8 cho từng biến 
        for var in self.variables:
            self.domains[var] = [self.goal[var[0]][var[1]]]
    
    def neighbors(self, X_i):
        return [v for v in self.variables if v != X_i]
    
    def constraint(self, x, y):
        return x != y
    
    def rm_inconsistent_values(self, X_i, X_j):
        revised = False
        to_remove = []
        
        for x in self.domains[X_i]:
            valid_y = False
            for y in self.domains[X_j]:
                if self.constraint(x, y):
                    valid_y = True
                    break
            
            if not valid_y:
                to_remove.append(x)
                revised = True
        
        for x in to_remove:
            self.domains[X_i].remove(x)
        
        return revised
    
    def is_solution(self, assignment):
        if len(assignment) != 9:
            return False
        
        for var, val in assignment.items():
            if self.goal[var[0]][var[1]] != val:
                return False
        
        vals = list(assignment.values())
        if len(set(vals)) != 9:
            return False
        
        return True
    
    def count_conflicts(self, var, value, assignment):
        conflicts = 0
        
        if self.goal[var[0]][var[1]] != value:
            conflicts += 1
        
        for _var, _val in assignment.items():
            if _var != var and _val == value:
                conflicts += 1
        
        return conflicts
    
    def state_from_assignment(self, assignment):
        state = [[0]*3 for _ in range(3)]
        for var, val in assignment.items():
            state[var[0]][var[1]] = val
        return state
    
    def assignment_from_state(self, state):
        assignment = {}
        for i in range(3):
            for j in range(3):
                assignment[(i, j)] = state[i][j]
        return assignment
