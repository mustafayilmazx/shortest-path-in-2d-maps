from utils import *

def a_star_search(start, end, image):
    """Perform A* search algorithm."""
    width, height = image.size
    g_cost = np.full((width, height), float('inf'))
    f_cost = np.full((width, height), float('inf'))
    rotation_count = np.zeros((width, height), dtype=int)
    visited = np.zeros((width, height), dtype=bool)
    parent = [[None] * height for _ in range(width)]

    g_cost[start[0]][start[1]] = 0
    f_cost[start[0]][start[1]] = manhattan_heuristic(start, end)
    pq = [(f_cost[start[0]][start[1]], start, None)]  # f-cost, Position, Direction

    while pq:
        _, current, direction = heapq.heappop(pq)
        if process_node(image, current, end, direction, visited, g_cost, rotation_count, f_cost, parent, pq):
            break

    return reconstruct_path(end, parent)

def process_node(image, current, end, direction, visited, g_cost, rotation_count, f_cost, parent, pq):
    """Process a single node in the A* search algorithm."""
    x, y = current
    if current == end:
        return True

    if visited[x][y]:
        return False

    visited[x][y] = True

    for neighbor, new_direction, rotation in get_neighbors(current, direction, image):
        new_x, new_y = neighbor
        tentative_g_cost = g_cost[x][y] + 1
        total_rotations = rotation_count[x][y] + rotation

        if tentative_g_cost < g_cost[new_x][new_y]:
            parent[new_x][new_y] = current
            g_cost[new_x][new_y] = tentative_g_cost
            rotation_count[new_x][new_y] = total_rotations
            f_cost[new_x][new_y] = tentative_g_cost + manhattan_heuristic(neighbor, end)
            heapq.heappush(pq, (f_cost[new_x][new_y], neighbor, new_direction))
    
    return False

def reconstruct_path(end, parent):
    """Reconstruct the path from the end node to the start node."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current[0]][current[1]]
    return path[::-1]

def manhattan_heuristic(pixel, goal):
    """Calculate the Manhattan distance from a pixel to the goal."""
    return abs(pixel[0] - goal[0]) + abs(pixel[1] - goal[1])

def find_path_with_a_star(image):
    """Find the shortest path using A* search."""
    start = find_nearest_waypoint(image, START_PIXEL, TARGET_COLOR)
    end = find_nearest_waypoint(image, END_PIXEL,  TARGET_COLOR)
    path = a_star_search(start, end, image)
    draw_path(image, path, "a_star_solution.png")
    path_description = describe_path(path)
    with open("a_star_solution.txt", "w") as text_file:
        text_file.write("\n".join(path_description))
