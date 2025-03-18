# Traveling Salesman Problem (TSP) - Dynamic Programming Pseudocode

```pseudocode
FUNCTION tsp_dynamic_programming(distances):
  // distances is a 2D matrix where distances[i][j] is the distance from city i to city j
  n = number of cities (size of distances)

  // dp is a map (or dictionary) to store the shortest path information
  // Key: (mask, last_city)
  // Value: minimum distance to visit all cities in the mask and end at last_city
  dp = empty map

  // Base case: Starting at city 0, having visited only city 0
  mask_initial = 1  // Binary 00...01 (only the first city visited)
  dp[(mask_initial, 0)] = 0

  // Iterate through all possible subsets of cities (represented by bitmasks)
  FOR mask FROM 1 TO (2^n - 1):
    FOR current_city FROM 0 TO (n - 1):
      // If the current_city is NOT in the current subset (mask)
      IF (mask AND (1 << current_city)) IS NOT zero:
        // Create a mask without the current_city
        previous_mask = mask XOR (1 << current_city)

        // If the previous mask is empty (meaning current_city is the only city, skip as it's the base case)
        IF previous_mask IS zero AND current_city IS NOT 0:
          CONTINUE

        // Iterate through all possible previous cities in the previous subset
        FOR previous_city FROM 0 TO (n - 1):
          // If the previous_city IS in the previous subset (previous_mask)
          IF (previous_mask AND (1 << previous_city)) IS NOT zero:
            // Calculate the new distance to reach current_city from previous_city
            distance_to_previous = dp.get((previous_mask, previous_city), infinity)
            new_distance = distance_to_previous + distances[previous_city][current_city]

            // Update the minimum distance to reach current_city with the current mask
            current_min_distance = dp.get((mask, current_city), infinity)
            dp[(mask, current_city)] = MIN(current_min_distance, new_distance)

  // After visiting all cities, need to return to the starting city (city 0)
  full_mask = (2^n) - 1 // Binary 11...1 (all cities visited)
  min_total_distance = infinity
  last_city_before_return = -1

  // Find the best last city to visit before returning to city 0
  FOR last_city FROM 1 TO (n - 1): // Start from 1 as the tour ends at a different city before returning
    IF (full_mask, last_city) IS in dp:
      distance_to_start = distances[last_city][0]
      total_distance = dp[(full_mask, last_city)] + distance_to_start
      IF total_distance < min_total_distance:
        min_total_distance = total_distance
        last_city_before_return = last_city

  // Reconstruct the optimal route by backtracking
  optimal_route = empty list
  current_mask = full_mask
  current_city = last_city_before_return

  // Work backwards from the last city
  WHILE current_city IS NOT -1:
    ADD current_city TO optimal_route

    IF current_city IS 0:
      BREAK

    best_previous_city = -1
    min_distance_to_current = infinity
    next_mask = current_mask XOR (1 << current_city) // Remove current city from mask

    // Find the previous city that led to the current minimum distance
    FOR previous_city FROM 0 TO (n - 1):
      IF (next_mask AND (1 << previous_city)) IS NOT zero:
        distance_from_previous = distances[previous_city][current_city]
        distance_to_previous_state = dp.get((next_mask, previous_city), infinity)
        total_distance = distance_to_previous_state + distance_from_previous
        IF total_distance < min_distance_to_current:
          min_distance_to_current = total_distance
          best_previous_city = previous_city

    current_mask = next_mask
    current_city = best_previous_city

  // Reverse the route to get the correct order (starting from city 0)
  REVERSE optimal_route

  RETURN optimal_route, min_total_distance
  ```

# Pseudocode for SOM-Based TSP
```pseudocode
FUNCTION convert_to_coordinates(adjacency_matrix):
  n = number of cities (size of adjacency_matrix)
  coords = empty list of coordinates

  // Create a simple circular layout for initial coordinates
  FOR i FROM 0 TO (n - 1):
    angle = 2 * PI * i / n
    ADD [COS(angle), SIN(angle)] TO coords

  // Refine coordinates using a simple force-directed approach
  FOR _ FROM 1 TO 100:
    FOR i FROM 0 TO (n - 1):
      FOR j FROM (i + 1) TO (n - 1):
        // Calculate target distance (normalized)
        IF adjacency_matrix[i][j] IS infinity:
          target_dist = 2.0 // Large distance for disconnected cities
        ELSE:
          target_dist = adjacency_matrix[i][j] / 12.0 // Normalize by max distance

        // Calculate current distance between city i and city j
        dx = coords[j][0] - coords[i][0]
        dy = coords[j][1] - coords[i][1]
        current_dist = SQRT(dx*dx + dy*dy)

        IF current_dist > 0:
          // Calculate force (attraction/repulsion)
          force = (target_dist - current_dist) / current_dist

        // Apply force to adjust coordinates
          factor = 0.1 * force
          coords[i][0] = coords[i][0] - dx * factor
          coords[i][1] = coords[i][1] - dy * factor
          coords[j][0] = coords[j][0] + dx * factor
          coords[j][1] = coords[j][1] + dy * factor

  RETURN coords
  ```