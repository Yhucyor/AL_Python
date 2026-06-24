from core import globals as g

class BeliefNode:
    def __init__(self, tap_ma_tran, parent = None, action = "_", cost = 0):
        self.ma_tran = tap_ma_tran
        self.parent = parent
        self.action = action
        self.cost = cost
    
    def isGoal(self, goal_matrix = None):
        if goal_matrix is None:
            return len(self.ma_tran) == 1
        
        if len(goal_matrix) == 1:
            gm = goal_matrix[0]
            for m in self.ma_tran:
                for r in range(3):
                    for c in range(3):
                        if gm[r][c] != -1 and m[r][c] != gm[r][c]:
                            return False
            return True
        else:
            for ma_tran in self.ma_tran:
                any_match = False
                for goal in goal_matrix:
                    match = True
                    for r in range(3):
                        for c in range(3):
                            if goal[r][c] != -1 and ma_tran[r][c] != goal[r][c]:
                                match = False
                                break
                        if not match:
                            break
                    if match:
                        any_match = True
                        break
                if not any_match:
                    return False
            return True
        
    def blank(self, ma_tran):
        for i in range(3):
            for j in range(3):
                if ma_tran[i][j] == 0:
                    return (i, j)
        return (0, 0)
    
    def simulate_move(self, ma_tran, move, dxy, goal_matrix):
        if goal_matrix is not None:
            if len(goal_matrix) == 1 and ma_tran == goal_matrix[0]:
                return ma_tran
            elif len(goal_matrix) >= 2 and ma_tran in goal_matrix:
                return ma_tran
        #Nếu chưa đạt đích thì di chuyển như bình thường
        x, y = self.blank(ma_tran)
        new_x = x + dxy[move][0]
        new_y = y + dxy[move][1]

        if 0 <= new_x <= 2 and 0 <= new_y <= 2:
            new_ma_tran = [row[:] for row in ma_tran]
            new_ma_tran[x][y], new_ma_tran[new_x][new_y] = new_ma_tran[new_x][new_y], new_ma_tran[x][y]
            return new_ma_tran
        
        return ma_tran
    
    def expand(self, goal_matrix = None):

        dxy = {"L": [0, -1], "R": [0, 1], "U": [-1, 0], "D": [1, 0]}
        child_nodes = []

        for i in dxy:
            tap_ma_tran_moi = []    
            #Cho cả nhóm đi cùng một hướng
            for m in self.ma_tran:
                kq = self.simulate_move(m, i, dxy, goal_matrix)
                if kq not in tap_ma_tran_moi:
                    tap_ma_tran_moi.append(kq)

            if tap_ma_tran_moi:
                tmp_BeliefNode = BeliefNode(
                    tap_ma_tran=tap_ma_tran_moi,
                    parent=self,
                    action=i,
                    cost=self.cost + 1
                )
                child_nodes.append(tmp_BeliefNode)
                g.tk_sinh_ra += 1
        return child_nodes
    
    def get_key(self):
        sorted_str = sorted([str(m) for m in self.ma_tran])
        return "".join(sorted_str)

    def __lt__(self, node):
        return self.cost < node.cost
        