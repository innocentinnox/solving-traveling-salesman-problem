from math import inf, pi, sin, cos, sqrt, exp
import random

# The adjacency matrix from the problem
adjacency_matrix = [
    [0, 12, 10, inf, inf, inf, 12],  # Node 1-start (index 0)
    [12, 0, 8, 12, inf, inf, inf],   # Node 2 (index 1)
    [10, 8, 0, 11, 3, inf, 9],       # Node 3 (index 2)
    [inf, 12, 11, 0, 11, 10, inf],   # Node 4 (index 3)
    [inf, inf, 3, 11, 0, 6, 7],      # Node 5 (index 4)
    [inf, inf, inf, 10, 6, 0, 9],    # Node 6 (index 5)
    [12, inf, 9, inf, 7, 9, 0]       # Node 7 (index 6)
]

def convert_to_coordinates(adj_matrix):
    """
    Convert an adjacency matrix to 2D coordinates using a simplified approach.
    This creates a valid spatial representation that preserves distances as much as possible.
    """
    n = len(adj_matrix)
    # Create a simple circular layout
    coords = []
    for i in range(n):
        angle = 2 * pi * i / n
        coords.append([cos(angle), sin(angle)])
    
    # Refine the coordinates using a simple force-directed approach
    for _ in range(100):
        for i in range(n):
            for j in range(i+1, n):
                # Calculate target distance (normalized)
                if adj_matrix[i][j] == inf:
                    target_dist = 2.0  # Large distance for disconnected cities
                else:
                    target_dist = adj_matrix[i][j] / 12.0  # Normalize by max distance
                
                # Calculate current distance
                dx = coords[j][0] - coords[i][0]
                dy = coords[j][1] - coords[i][1]
                current_dist = sqrt(dx*dx + dy*dy)
                
                if current_dist > 0:
                    # Calculate force (attraction/repulsion)
                    force = (target_dist - current_dist) / current_dist
                    
                    # Apply force
                    factor = 0.1 * force
                    coords[i][0] -= dx * factor
                    coords[i][1] -= dy * factor
                    coords[j][0] += dx * factor
                    coords[j][1] += dy * factor
    
    return coords

class SOM_TSP:
    def __init__(self, city_coordinates, n_neurons=None, learning_rate=0.8):
        """
        Initialize SOM for TSP
        
        Args:
            city_coordinates: 2D array of city coordinates
            n_neurons: Number of neurons in the ring (default: 2.5 * number of cities)
            learning_rate: Initial learning rate
        """
        self.city_coordinates = city_coordinates
        self.n_cities = len(city_coordinates)
        
        if n_neurons is None:
            self.n_neurons = int(2.5 * self.n_cities)
        else:
            self.n_neurons = n_neurons
        
        # Initialize neurons in a small circle
        self.neuron_coordinates = []
        
        # Calculate center of the cities
        center_x = sum(city[0] for city in city_coordinates) / self.n_cities
        center_y = sum(city[1] for city in city_coordinates) / self.n_cities
        
        # Calculate radius (half the average range)
        max_x = max(city[0] for city in city_coordinates)
        min_x = min(city[0] for city in city_coordinates)
        max_y = max(city[1] for city in city_coordinates)
        min_y = min(city[1] for city in city_coordinates)
        r = 0.5 * ((max_x - min_x) + (max_y - min_y)) / 4
        
        # Create neurons in a circle
        for i in range(self.n_neurons):
            angle = 2 * pi * i / self.n_neurons
            x = center_x + r * cos(angle)
            y = center_y + r * sin(angle)
            self.neuron_coordinates.append([x, y])
        
        self.learning_rate = learning_rate
        self.n_iterations = 100 * self.n_cities
        
    def get_winner(self, city_idx):
        """Find the neuron closest to the given city"""
        city = self.city_coordinates[city_idx]
        min_dist = float('inf')
        winner = 0
        
        for i, neuron in enumerate(self.neuron_coordinates):
            # Calculate squared Euclidean distance
            dist = (neuron[0] - city[0])**2 + (neuron[1] - city[1])**2
            if dist < min_dist:
                min_dist = dist
                winner = i
                
        return winner
        
    def get_neighborhood(self, winner, iteration):
        """Calculate the neighborhood function for each neuron"""
        # Neighborhood radius decreases over time
        radius = self.n_neurons / 2 * (1 - iteration / self.n_iterations)
        if radius < 1:
            radius = 1
            
        # Calculate distance from winner (in the ring)
        neighborhood = []
        for i in range(self.n_neurons):
            # Calculate ring distance (shortest path around the ring)
            dist = min(
                abs(i - winner),
                self.n_neurons - abs(i - winner)
            )
            
            # Gaussian neighborhood function
            influence = exp(-(dist**2) / (2 * (radius**2)))
            neighborhood.append(influence)
            
        return neighborhood
        
    def train(self):
        """Train the SOM"""
        for iteration in range(self.n_iterations):
            # Anneal learning rate
            current_lr = self.learning_rate * (1 - iteration / self.n_iterations)
            
            # Select a random city
            city_idx = random.randint(0, self.n_cities - 1)
            
            # Find the winner neuron
            winner = self.get_winner(city_idx)
            
            # Get neighborhood function
            neighborhood = self.get_neighborhood(winner, iteration)
            
            # Update neurons
            for i in range(self.n_neurons):
                # Influence of the neighborhood
                influence = neighborhood[i] * current_lr
                
                # Update neuron position
                dx = self.city_coordinates[city_idx][0] - self.neuron_coordinates[i][0]
                dy = self.city_coordinates[city_idx][1] - self.neuron_coordinates[i][1]
                self.neuron_coordinates[i][0] += influence * dx
                self.neuron_coordinates[i][1] += influence * dy
                
    def get_route(self):
        """Get the route from trained SOM"""
        route = []
        for city_idx in range(self.n_cities):
            winner = self.get_winner(city_idx)
            route.append((city_idx, winner))
            
        # Sort by winner indices to get the route
        route.sort(key=lambda x: x[1])
        
        # Extract city indices
        city_route = [x[0] for x in route]
        
        # Ensure the route starts and ends at city 0
        if 0 in city_route:
            start_idx = city_route.index(0)
            city_route = city_route[start_idx:] + city_route[:start_idx]
        else:
            # If somehow city 0 is not in the route (shouldn't happen), add it at the beginning
            city_route = [0] + city_route
        
        # Add city 0 at the end for the complete tour
        city_route.append(0)
        
        return city_route
        
    def calculate_distance(self, route):
        """Calculate the total distance of a route"""
        distance = 0
        for i in range(len(route) - 1):
            from_city = route[i]
            to_city = route[i + 1]
            
            # Use the original adjacency matrix for distances
            if adjacency_matrix[from_city][to_city] == inf:
                # If there's no direct connection, this is not a valid route
                return inf
            distance += adjacency_matrix[from_city][to_city]
            
        return distance

# Create city coordinates from adjacency matrix
city_coordinates = convert_to_coordinates(adjacency_matrix)

# Initialize and train SOM
som = SOM_TSP(city_coordinates)
som.train()

# Get the route
route = som.get_route()
route_distance = som.calculate_distance(route)

# Display the route and distance
print(f"SOM Route: {[city+1 for city in route]}")
print("Path:", " > ".join(str(city + 1) for city in route))
print(f"SOM Route Distance: {route_distance}")