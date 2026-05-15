"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: _Suber Ebrahim_
Student ID:   _827410383_

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    TODO
    """
    return """
    - Dijkstra's finds the shortest path to each node independently
      but cannot account for the requirement to visit all relics in a specific sequence.
    - The optimal order of relic collection that minimizes the cumulative fuel cost 
      before heading to the exit is determined.
    - Because the graph is directed and has many stops, we must explore different sequences
      to find the minimum fuel cost path.
    """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Identifies the starting nodes for Dijkstra. 
    Includes the spawn point and all relic locations.
    """
    #creates a set containing the spawn and all nodes in the relics list
    sources_set = {spawn} | set(relics)
    return list(sources_set)


def run_dijkstra(graph, source):
    """
    Finds the minimum fuel cost from the source to every node
    """
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    
    #priority queue stores (distance, node)
    pq = [(0, source)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        #skip if already found a better path
        if current_dist > distances[u]:
            continue
            
        #check edges and relax distances
        for v, weight in graph.get(u, []):
            distance = current_dist + weight
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return distances
    


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Runs Dijkstra from every source node and stores the results
    in a nested dictionary (dist_table).
    """
 
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    
    for s in sources:
        dist_table[s] = run_dijkstra(graph, s)
        
    return dist_table



# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    TODO
    """
    return """
    - For finalized nodes the distance value is the true, absolute shortest path from the source,
      and it will not be updated again.
    - For non finalized nodes The distance value the shortest known path
      from the source using only finalized nodes as intermediate steps.
    - Initialization: Only the source is set to 0 and all others to infinity,
      which is correct since no edges have been explored yet.
    - Maintenance: Because edge weights are nonnegative, the node with the minimum distance
      in the priority queue cannot be reached through any other node with smaller total cost.
    - Termination: When the priority queiFe is empty, the invariant ensures that every 
      reachable node has been finalized with its minimum distance.
    - Connection: The whole search for the relics depends on these costs being the absolute minimum, 
      If the distances from Dijkstra are wrong, the search part won't work right because 
      it will pick a path it thinks is the cheapest when it actually isn't.
    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Part 4 answers as string
    """
    return """
    - Greedy fails: _A greedy strategy always moves to the nearest uncollected relic,
      which ignores how that choice impacts the cost of reaching the remaining relics or the exit._
    - Counter example setup: _Using the spec example, starting at S, the distances to relics are B = 1, C = 2, and D = 2__
    - Greedy Choices: _Greedy picks B first because it is the closest to S. However,
      from B, the paths to C or D might be significantly more expensive down the line._
    - Optimal Choices: _Unlike greedy optimal picks globally cheap choices rather than locally cheap
      meaning it may choose to go to C or D because they might lead to cheaper overall cost later on.._
    - Greedy Loses: _Greedy loses because it makes a "local" decision that results in a "global" fuel penalty,   
      potentially doubling back through expensive edges to finish the mission, or in the case of directed grpah going to deadends._

    - Algorithm Explore:  _The algorithm must explore every possible order of relic collection to identify the sequence that results 
      in the mininmum total fuel cost_


    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
   
    best = [float('inf'), []]
    #using a set for remaining relics
    relics_remaining = set(relics)
    #recursive search.
    _explore(dist_table, spawn, relics_remaining, [], 0, exit_node, best)
    
    return tuple(best)


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    #PRUNING: It is safe to prune and skip because fuel costs are non negative.
    #if more fuel than the best path is already spent algorithm can't find anything better.
    if cost_so_far >= best[0]:
        return
    #base case no relics left
    if len(relics_remaining) == 0:
      
        dist_to_exit = dist_table[current_loc].get(exit_node, float('inf'))
        total_trip_cost = cost_so_far + dist_to_exit
        
        #update best cost
        if total_trip_cost < best[0]:
            best[0] = total_trip_cost
            best[1] = list(relics_visited_order)
        return

    #recursuve case tries all the relics left
    for next_relic in sorted(list(relics_remaining)):
        cost_to_next = dist_table[current_loc].get(next_relic, float('inf'))
        
        
        if cost_to_next != float('inf'):
            relics_remaining.remove(next_relic)
            relics_visited_order.append(next_relic)
            _explore(dist_table, next_relic, relics_remaining, 
                     relics_visited_order, cost_so_far + cost_to_next, 
                     exit_node, best)
            
           #backtracking
            relics_visited_order.pop()
            relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
 
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    
    #printout of code to see progress for part 2
    print(f"\nDEBUG DATA:")
    print(f"Sources mapped: {list(dist_table.keys())}")
    for r in relics:
        cost = dist_table[spawn].get(r, 'Unreachable')
        print(f"Shortest path S -> {r}: {cost}")
    
    return find_optimal_route(dist_table, spawn, relics, exit_node)



# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
