class Puzzle_CSP:
    def __init__(self, goal):
        self.goal = goal
        self.vars = [
            (0,0),(0,1),(0,2),
            (1,0),(1,1),(1,2),
            (2,0),(2,1),(2,2)
        ]
        #Dung cho forward backtracking 
        self.domains = {
            var: set(range(9))
            for var in self.vars
        }
        
    def assignment_to_matrix(self, assig):
        ma_tran = [[-1]*3 for _ in range(3)]
        for (i, j), val in assig.items():
            ma_tran[i][j] = val
        return ma_tran
    
    def is_complete(self, assig):
        if len(assig) != 9:
            return False
        
        ma_tran = self.assignment_to_matrix(assig)
        return ma_tran == self.goal
    
    def select_unassigned_var(self, assignment):
        for var in self.vars:
            if var not in assignment:
                return var
        return None 
    
    def domain_values(self, var, assig):
        return self.domains[var]
        
    def is_consistent(self, var, val, assignment):
        return val not in assignment.values()
    
    def forward_check(self, var, value, assignment):
        removed = []
        for nvar in self.vars:
            if nvar not in assignment:
                if nvar == var:
                    continue
                if value in self.domains[nvar]:
                    self.domains[nvar].remove(value)
                    removed.append((nvar, value))
                if len(self.domains[nvar]) == 0:
                    self.restore(removed)
                    return False
        return removed
        
    def restore(self, removed):
        if removed:
            for var, val in removed:
                self.domains[var].add(val)
