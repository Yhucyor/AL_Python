import heapq
from random import choice
import math
import random 

from core.node import Node
from core.ulities import solution
from core.ulities import manhattan
from core import globals as g

#Define value of:
To = 1500
a = 0.95
Tmin = 500
def simulated_annealing(problem_ma_tran):
    cur_node = Node(problem_ma_tran)
    cur_node.cost = manhattan(cur_node.ma_tran)
    g.tk_da_duyet += 1

    T = To
    while T > Tmin:
        if cur_node.isGoal():
            return solution(cur_node)
        
        neighbor_nodes = cur_node.expand()
        if len(neighbor_nodes) == 0:
            break
        next_node = choice(neighbor_nodes)
        next_node.cost = manhattan(next_node.ma_tran)
        g.tk_da_duyet += 1

        delta = next_node.cost - cur_node.cost

        if delta < 0:
            cur_node = next_node
        else:
            p = math.exp(-delta/T)
            if random.random() < p:
                cur_node = next_node
        T = a*T

    return solution(cur_node)