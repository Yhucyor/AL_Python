import heapq
from core.node import Node
from core.ulities import solution
from core.ulities import manhattan
from core import globals as g

#Trong random sample help to choice k elements ramdomly
from random import sample 

def local_beam_search(problem_ma_trix):
    #Select the number of elements k 
    k = 3 
    init_node = Node(problem_ma_trix)
    init_node.cost = manhattan(problem_ma_trix)

    neighbor_nodes = init_node.expand()
    cur_nodes = sample(neighbor_nodes, min(k, len(neighbor_nodes)))
    g.tk_da_duyet += 1
    for node in cur_nodes:
        node.cost = manhattan(node.ma_tran)

    while True:
        neighbor_nodes = []
        for node in cur_nodes:
            g.tk_da_duyet += 1
            for child in node.expand():
                child.cost = manhattan(child.ma_tran)
                neighbor_nodes.append(child)
        if len(neighbor_nodes) == 0:
            #Return the best current state
            best_node = min(cur_nodes)
            return solution(best_node)
        for node in neighbor_nodes:
            if node.isGoal():
                return solution(node)
        #Select the beam if not found 
        cur_nodes = heapq.nsmallest(k, neighbor_nodes)
        
