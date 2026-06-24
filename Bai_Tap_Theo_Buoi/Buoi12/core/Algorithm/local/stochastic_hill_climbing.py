import heapq
from core.node import Node
from collections import deque
from core.ulities import solution
from core.ulities import manhattan
from core import globals as g
from random import choice

def stochastic_hill_climbing(problem_ma_trix):
    cur_node = Node(problem_ma_trix)
    cur_node.cost = manhattan(problem_ma_trix)

    while True:
        g.tk_da_duyet += 1
        if cur_node.isGoal():
            return solution(cur_node)
        
        better_neighbors = []
        for child in cur_node.expand():
            child.cost = manhattan(child.ma_tran)
            if child.cost < cur_node.cost:
                better_neighbors.append(child)
        
        if len(better_neighbors) == 0:
            return solution(cur_node)
        else:
            cur_node = choice(better_neighbors)


