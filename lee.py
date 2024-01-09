from utils import *

def lee_search(start, end, image):
    """Perform Lee algorithm for pathfinding."""
    width, height = image.size
    grid = np.full((width, height), -1)  # Initialize grid with -1
    queue = [start]
    grid[start[0]][start[1]] = 0  # Distance from start to start is 0

    # Wave propagation
    while queue:
        x, y = queue.pop(0)

        if (x, y) == end:
            break

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:  # 4-connected grid
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[nx][ny] == -1 and is_valid_pixel((nx, ny), image):
                grid[nx][ny] = grid[x][y] + 1
                queue.append((nx, ny))

    # Reconstruct path from end to start
    path = []
    current = end
    if grid[end[0]][end[1]] == -1:  # Check if the path is reachable
        return None, -1  # Path not found

    while current != start:
        path.append(current)
        x, y = current
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and grid[nx][ny] == grid[x][y] - 1:
                current = (nx, ny)
                break

    path.append(start)
    return path[::-1]  # Path


def find_path_with_lee(image):
    """Find path with Lee algorithm."""
    start = find_nearest_waypoint(image, START_PIXEL, TARGET_COLOR)
    end = find_nearest_waypoint(image, END_PIXEL,  TARGET_COLOR)

    path = lee_search(start, end, image)
    draw_path(image, path, "lee_solution.png")
    path_description = describe_path(path)
    with open("lee_solution.txt", "w") as text_file:
        text_file.write("\n".join(path_description))
