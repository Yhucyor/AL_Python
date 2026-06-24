import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core.ulities import manhattan
from core import globals as g
from random import choice

def random_restart_hill_climbing(problem_ma_tran):
    MAX_RESTART = 100
    for _ in range(MAX_RESTART):
        cur_node = Node(problem_ma_tran)
        cur_node.cost = manhattan(problem_ma_tran)
        while(True):
            g.tk_da_duyet += 1
            if cur_node.isGoal():
                return solution(cur_node)
            
            better_neighbors = []
            for child in cur_node.expand():
                child.cost = manhattan(child.ma_tran)
                if child.cost < cur_node.cost:
                    better_neighbors.append(child)
            if len(better_neighbors) == 0:
                break
            else:
                next_node = choice(better_neighbors)
                cur_node = next_node
    return False
