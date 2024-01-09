from PIL import Image, ImageDraw
import heapq
import numpy as np

def load_image(image_path):
    """Load an image from the given path."""
    return Image.open(image_path)

def save_image(image, output_path):
    """Save the image to the given path."""
    image.save(output_path)

def find_nearest_waypoint(image, pixel, target_color):
    width, height = image.size
    x, y = pixel
    nearest_waypoint = None
    min_distance = float('inf')

    for i in range(max(width, height)):
        checks = [
            (x, y - i),  # Up
            (x, y + i),  # Down
            (x - i, y),  # Left
            (x + i, y)   # Right
        ]

        for nx, ny in checks:
            if 0 <= nx < width and 0 <= ny < height and image.getpixel((nx, ny))[0:3] == target_color:
                distance = abs(x - nx) + abs(y - ny)  # Manhattan distance
                if distance < min_distance:
                    min_distance = distance
                    nearest_waypoint = (nx, ny)
                    return nearest_waypoint  # Return immediately on finding the nearest waypoint

    return nearest_waypoint


def lee_search(start, end):
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
            if 0 <= nx < width and 0 <= ny < height and grid[nx][ny] == -1 and is_valid_pixel((nx, ny), image, (255, 255, 255)):
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
    return path[::-1], grid[end[0]][end[1]]  # Path and length

def reconstruct_path(end, parent):
    """Reconstruct the path from the end node to the start node."""
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current[0]][current[1]]
    return path[::-1]

def get_neighbors(pixel, current_direction, image):
    """Get all valid neighbors for the given pixel."""
    x, y = pixel
    directions = [(1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")]
    neighbors = []
    for dx, dy, new_direction in directions:
        neighbor = (x + dx, y + dy)
        if is_valid_pixel(neighbor, image, (255, 255, 255)):
            rotation = 1 if new_direction != current_direction else 0
            neighbors.append((neighbor, new_direction, rotation))
    return neighbors

def is_valid_pixel(pixel, image, target_color):
    """Check if a pixel is valid (i.e., matches the target color)."""
    x, y = pixel
    width, height = image.size
    return 0 <= x < width and 0 <= y < height and image.getpixel((x, y))[0:3] == target_color

def manhattan_heuristic(pixel, goal):
    """Calculate the Manhattan distance from a pixel to the goal."""
    return abs(pixel[0] - goal[0]) + abs(pixel[1] - goal[1])

def draw_path(image, path, output_path):
    """Draw the path on the image and save it."""
    image_with_path = image.copy()
    draw = ImageDraw.Draw(image_with_path)
    size = 5
    for x, y in path:
        draw.ellipse((x - size, y - size, x + size, y + size), fill=(255, 255, 0))
    save_image(image_with_path, output_path)
    print(f"Path image saved as {output_path}")

def save_path_description(path, output_path):
    """Save the textual path description to a file."""
    description = describe_path(path)
    with open(output_path, "w") as text_file:
        text_file.write("\n".join(description))
    print(f"Path description saved as {output_path}")

def describe_path(path):
    description = []
    prev_x, prev_y = path[0]
    current_direction = None
    distance = 0

    for x, y in path[1:]:
        dx, dy = x - prev_x, y - prev_y
        new_direction = get_direction(dx, dy)

        if new_direction != current_direction:
            if current_direction:
                description.append(f"Turn {current_direction} and go ahead {distance} px")
            current_direction = new_direction
            distance = 0

        distance += max(abs(dx), abs(dy))
        prev_x, prev_y = x, y

    if current_direction:
        description.append(f"Turn {current_direction} and go ahead {distance} px")

    return description

def get_direction(dx, dy):
    if dx > 0: return "right"
    elif dx < 0: return "left"
    elif dy > 0: return "down"
    elif dy < 0: return "up"
    return ""

def main():
    """Main function to execute the pathfinding algorithm."""
    global image
    input_image_path = "ev.png"
    output_image_path = "map_with_path.png"
    target_color = (255, 255, 255)

    image = load_image(input_image_path)
    start_pixel = find_nearest_waypoint(image, (785, 1007), target_color)
    end_pixel = find_nearest_waypoint(image, (2186, 763), target_color)

    path, rotations = lee_search(start_pixel, end_pixel)
    print(f"Path found with {rotations} rotations")
    draw_path(image, path, output_image_path)

    output_text_path = "path_description.txt"
    save_path_description(path, output_text_path)

if __name__ == "__main__":
    main()
