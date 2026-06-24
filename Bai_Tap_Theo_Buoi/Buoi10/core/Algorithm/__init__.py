from .uninformed.bfs1 import BFS1
from .uninformed.bfs2 import BFS2
from .uninformed.dfs import DFS
from .informed.gs import Greedy_Search 
from .uninformed.ids import IDS
from .uninformed.ucs import UCS
from .informed.a_star import A_Star
from .informed.ida import IDA
from .local.simple_hill_climbing import SHC
from .local.simple_hill_climbing_highest import SHC_Highest
from .local.local_beam_search import local_beam_search
from .local.random_restart_hill_climbing import random_restart_hill_climbing
from .local.stochastic_hill_climbing import stochastic_hill_climbing

ALGORITHM_SOLVERS = {
    "Breadth-First Search 1": BFS1, 
    "Breadth-First Search 2": BFS2, 
    "Depth-First Search": DFS, 
    "Iterative Deepening Search": IDS, 
    "Uniform Cost Search": UCS, 
    "Greedy Best-First Search": Greedy_Search, 
    "A* Search": A_Star, 
    "Iterative Deepening A*": IDA, 
    "Simple Hill Climbing": SHC, 
    "Steepest-Ascent Hill Climbing": SHC_Highest,
    "Stochastic Hill Climbing": stochastic_hill_climbing, 
    "Random-Restart Hill Climbing": random_restart_hill_climbing, 
    "Local Beam Search": local_beam_search
}

ALGORITHM_NAMES = list(ALGORITHM_SOLVERS.keys())