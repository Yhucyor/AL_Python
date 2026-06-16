import heapq
import random

from core.node import Node
from core import globals as g
from core.ulities import solution

def execute_solution(problem_ma_tran, plan_tree):

    da_sinh = g.tk_sinh_ra
    da_duyet = g.tk_da_duyet
    cur_node = Node(problem_ma_tran)
    cur_plan = plan_tree

    while cur_plan:
        action = cur_plan[0]
        states = cur_plan[1]

        child_nodes = cur_node.expand()

        true_node = next((c for c in child_nodes if c.action == action), None)
        if not true_node: 
            break
        #Thêm một số trường hợp để đúng với thuật toán 
        wrong_nodes = [c for c in child_nodes if c.ma_tran != true_node.ma_tran]
        p = random.randint(0, 10)
        if p <= 8 or not wrong_nodes:
            next_node = true_node
        else:
            next_node = random.choice(wrong_nodes)
            next_node.action = f"TRƯỢT ({true_node.action})"

        next_node.parent = cur_node
        cur_node = next_node

        key_ma_tran = str(cur_node.ma_tran)
        cur_plan = states.get(key_ma_tran, [])

    g.tk_sinh_ra = da_sinh
    g.tk_da_duyet = da_duyet
    return solution(cur_node)

def choice_wrong(node, correct_child):
    rnd = random.randint(0, 10)
    p = 8
    if p < rnd:
        child_nodes = node.expand()
        wrong_nodes = [son for son in child_nodes if son.ma_tran != correct_child.ma_tran]

        if wrong_nodes:
            return random.choice(wrong_nodes)
    return None

def and_or_graph_search(problem_ma_tran):
    init_node = Node(problem_ma_tran)
    plan_tree = or_search(init_node, [])

    if plan_tree is False:
        return False
    
    return execute_solution(problem_ma_tran, plan_tree)

def or_search(cur_node, path):
    g.tk_da_duyet += 1 
    if cur_node.isGoal():
        return []
    
    if len(path) > 12:
        return False
    if cur_node.ma_tran in path:
        return False
    
    for child in cur_node.expand():
        result_states = [child]
        wrong_node = choice_wrong(cur_node, child)
        
        if wrong_node is not None:
            #Ajust action to same with child 
            wrong_node.action = f"TRƯỢT ({child.action})"
            result_states.append(wrong_node)
            
        new_path = path + [cur_node.ma_tran]
        plan = and_search(result_states, new_path)
        
        if plan is not False:
            return [child.action, plan]
    return False

def and_search(states, path):
    plans = {}

    for s in states:
        plan_s = or_search(s, path)
        if plan_s is False:
            return False
        
        key_str = str(s.ma_tran)
        plans[key_str] = plan_s
    
    return plans

