import heapq
import numpy as np
from utils import *


def dijkstra(start, end, image):
    width, height = image.size
    distance = np.full((width, height), float('inf'))
    rotation_count = np.zeros((width, height), dtype=int)
    visited = np.zeros((width, height), dtype=bool)
    parent = [[None] * height for _ in range(width)]

    distance[start[0]][start[1]] = 0
    start_direction = None  # Define initial direction if needed
    pq = [(0, 0, start, start_direction)]  # Distance, Rotations, Position, Direction

    while pq:
        dist, rotations, current, direction = heapq.heappop(pq)
        x, y = current

        if current == end:
            break

        if visited[x][y]:
            continue

        visited[x][y] = True

        for neighbor, new_direction, rotation in get_neighbors(current, direction, image):
            new_x, new_y = neighbor

            if not visited[new_x][new_y] and is_valid_pixel(neighbor, image):
                new_dist = dist + 1
                total_rotations = rotations + rotation
                if new_dist < distance[new_x][new_y]:
                    distance[new_x][new_y] = new_dist
                    rotation_count[new_x][new_y] = total_rotations
                    parent[new_x][new_y] = current
                    heapq.heappush(pq, (new_dist, total_rotations, neighbor, new_direction))
                elif new_dist == distance[new_x][new_y] and total_rotations < rotation_count[new_x][new_y]:
                    rotation_count[new_x][new_y] = total_rotations
                    parent[new_x][new_y] = current
                    heapq.heappush(pq, (new_dist, total_rotations, neighbor, new_direction))
                    
    # Reconstruct the path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current[0]][current[1]]

    return path[::-1]

def find_path_with_dijkstra(image):
    start = find_nearest_waypoint(image, START_PIXEL, TARGET_COLOR)
    end = find_nearest_waypoint(image, END_PIXEL,  TARGET_COLOR)
    path = dijkstra(start, end, image)
    draw_path(image, path, "dijkstra_solution.png")
    path_description = describe_path(path)
    with open("dijkstra_solution.txt", "w") as text_file:
        text_file.write("\n".join(path_description))
