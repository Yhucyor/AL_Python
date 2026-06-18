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
from .local.simulated_annealing import simulated_annealing
from .environment_search.unobservable.bfs_belief_state import bfs_belief_state
from .environment_search.partially_observable.dfs_partial_state import dfs_partial_state
from .environment_search.nondeterministic.and_or_graph_search import and_or_graph_search
from .constraint_satisfaction.backtracking_search import backtracking_search
from .constraint_satisfaction.backtracking_search_forward_checking import backtracking_search_forward_checking
from .constraint_satisfaction.min_conflicts import min_conflicts
from .constraint_satisfaction.arc_consistency_3 import arc_consistency_3

ALGORITHM_GROUPS = {
    "Uninformed Search": {
        "Breadth-First Search 1": BFS1,
        "Breadth-First Search 2": BFS2,
        "Depth-First Search": DFS,
        "Iterative Deepening Search": IDS,
        "Uniform Cost Search": UCS
    },
    "Informed Search": {
        "Greedy Best-First Search": Greedy_Search,
        "A* Search": A_Star,
        "Iterative Deepening A*": IDA
    },
    "Local Search": {
        "Simple Hill Climbing": SHC,
        "Steepest-Ascent Hill Climbing": SHC_Highest,
        "Stochastic Hill Climbing": stochastic_hill_climbing,
        "Random-Restart Hill Climbing": random_restart_hill_climbing,
        "Local Beam Search": local_beam_search,
        "Simulated Annealing": simulated_annealing
    },
    "Unobservable Environment": {
        "BFS Belief State": bfs_belief_state
    },
    "Partially Observable Environment": {
        "DFS Partial State": dfs_partial_state
    },
    "NonDeterministic Environment": {
        "And Or Graph Search": and_or_graph_search
    },
    "Contraint_Satisfication": {
        "Backtracking Search": backtracking_search,
        "Backtracking Search Forward Checking": backtracking_search_forward_checking,
        "Arc Consistency 3": arc_consistency_3,
        "Min-Conflicts": min_conflicts
    }
}

ALGORITHM_NAMES = list(ALGORITHM_GROUPS.keys())
