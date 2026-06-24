from core.node import Node

class Puzzle_CSP:
    def __init__(self, start_matrix, max_depth):
        #Node bắt đầu và giới hạn 
        self.start_node = Node(start_matrix)
        self.max_depth = max_depth

    def is_complete(self, assignment):
        if not assignment:
            return False
        last = max(assignment.keys())
        #Trạng thái cuối có trùng với ma trận hay không 
        return assignment[last].isGoal()
    
    #Lựa chọn biến tiếp theo cần gán giá trị 
    def select_unassigned_var(self, assignment):
        if not assignment:
            return 0
        last = max(assignment.keys())

        if last + 1 <= self.max_depth:
            return last + 1
        
    def domain_values(self, var, assignment):
        if var == 0:
            return [self.start_node]
        
        prev_node = assignment[var - 1]
        return prev_node.expand()
    
    #Kiểm tran ràn buộc 
    def is_consistent(self, var, value, assignment):
        cur_ma_tran = value.ma_tran 
        for s, node  in assignment.items():
            if s < var and node.ma_tran == cur_ma_tran:
                return False
        return True 
    
    def forward_check(self, var, value, assignment):
        if var + 1 > self.max_depth:
            return True
        
        fur_domain = value.expand()

        valid_fur_domain = 0
        for fur_node in fur_domain:
            is_dup = False
            for _, past_node  in assignment.items():
                if past_node.ma_tran == fur_node.ma_tran:
                    is_dup = True
                    break
                    
            if not is_dup:
                valid_fur_domain += 1

        if valid_fur_domain == 0:
            return False
        
        return True 