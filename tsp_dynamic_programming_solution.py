from math import inf

def tsp_dynamic_programming(distances):
    """
    Solves the Traveling Salesman Problem using dynamic programming.
    
    Args:
        distances: 2D matrix where distances[i][j] is the distance from city i to city j
    
    Returns:
        tuple: (optimal_route, minimum_distance)
    """
    n = len(distances)  # Number of cities
    
    # dp[(mask, city)] represents the shortest path that visits all cities in the mask
    # and ends at the specified city
    dp = {}
    
    # Base case: Start at city 0 with only city 0 visited
    dp[(1, 0)] = 0
    
    # Iterate through all possible subsets of cities represented as bitmasks
    for mask in range(1, 1 << n):  # 1 << n equals 2^n
        for current_city in range(n):
            # Skip if current_city is not in the subset represented by mask
            if not (mask & (1 << current_city)):
                continue
                
            # Remove current_city from mask to get the previous state
            prev_mask = mask & ~(1 << current_city)
            
            # Skip the case where prev_mask is empty (only happens when current_city is 0)
            if prev_mask == 0:
                continue
                
            # Find the best previous city to visit before current_city
            for prev_city in range(n):
                # Skip if prev_city is not in prev_mask
                if not (prev_mask & (1 << prev_city)):
                    continue
                    
                # Calculate new distance through prev_city
                new_distance = dp.get((prev_mask, prev_city), inf) + distances[prev_city][current_city]
                
                # Update dp with the minimum distance
                dp[(mask, current_city)] = min(dp.get((mask, current_city), inf), new_distance)
    
    # Calculate the final leg of the journey: return to starting city (0)
    full_mask = (1 << n) - 1  # Bitmask with all cities visited (e.g., 1111...1)
    min_distance = inf
    final_city = -1
    
    # Find the best city to visit last before returning to city 0
    for city in range(1, n):  # Skip city 0 as it's our starting point
        if (full_mask, city) in dp:
            total_distance = dp[(full_mask, city)] + distances[city][0]
            if total_distance < min_distance:
                min_distance = total_distance
                final_city = city
    
    # Reconstruct the optimal route
    route = []
    mask = full_mask
    current_city = final_city
    
    # Work backwards from the final city
    while current_city != -1:
        route.append(current_city)
        
        if current_city == 0:  # We've reached the starting city
            break
            
        # Find the best previous city
        best_prev_city = -1
        best_distance = inf
        next_mask = mask & ~(1 << current_city)  # Remove current city from mask
        
        for prev_city in range(n):
            if not (next_mask & (1 << prev_city)):
                continue
                
            distance = dp.get((next_mask, prev_city), inf) + distances[prev_city][current_city]
            if distance < best_distance:
                best_distance = distance
                best_prev_city = prev_city
        
        mask = next_mask
        current_city = best_prev_city
    
    # Reverse the route to get the correct order (starting from city 0)
    route.reverse()
    
    return route, min_distance


# Adjacency matrix representation of the graph
adjacency_matrix = [
    [0, 12, 10, inf, inf, inf, 12],  # Node 1-start (index 0)
    [12, 0, 8, 12, inf, inf, inf],   # Node 2 (index 1)
    [10, 8, 0, 11, 3, inf, 9],       # Node 3 (index 2)
    [inf, 12, 11, 0, 11, 10, inf],   # Node 4 (index 3)
    [inf, inf, 3, 11, 0, 6, 7],      # Node 5 (index 4)
    [inf, inf, inf, 10, 6, 0, 9],    # Node 6 (index 5)
    [12, inf, 9, inf, 7, 9, 0]       # Node 7 (index 6)
]

route, distance = tsp_dynamic_programming(adjacency_matrix)
print("Dynamic Programming Route List:", [x + 1 for x in route])
print("Path:", " > ".join(str(city + 1) for city in route))
print("Total Distance:", distance)