from PIL import Image, ImageDraw
import heapq
import numpy as np

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
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

def find_shortest_path(start, end, target_color):
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

            if not visited[new_x][new_y] and is_valid(neighbor, image, target_color):
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

    return path[::-1], rotation_count[end[0]][end[1]]  # Return path and total rotations

def is_valid(pixel, image, target_color):
    width, height = image.size
    x, y = pixel
    return 0 <= x < width and 0 <= y < height and image.getpixel((x, y))[0:3] == target_color

def get_neighbors(pixel, current_direction, image):
    x, y = pixel
    directions = [(1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")]
    neighbors = []
    for dx, dy, new_direction in directions:
        neighbor = (x + dx, y + dy)
        if is_valid(neighbor, image, (255, 255, 255)):
            rotation = 1 if new_direction != current_direction else 0
            neighbors.append((neighbor, new_direction, rotation))
    return neighbors

def dijkstra(image, start_pixel, end_pixel, target_color):
    

    path, total_rotations = find_shortest_path(start_pixel, end_pixel, target_color)

    return path, total_rotations

def draw_path(image, path, output_path):
    """Draw the path on the image and save it."""
    image_with_path = image.copy()
    draw = ImageDraw.Draw(image_with_path)
    size = 5
    for x, y in path:
        draw.ellipse((x - size, y - size, x + size, y + size), fill=(255, 255, 0))
    save_image(image_with_path, output_path)
    print(f"Path image saved as {output_path}")

def get_direction(dx, dy):
    if dx > 0: return "right"
    elif dx < 0: return "left"
    elif dy > 0: return "down"
    elif dy < 0: return "up"
    return ""

def describe_path(path):
    description = []
    prev_x, prev_y = path[0]
    current_direction = None
    distance = 0

    for x, y in path[1:]:
        dx = x - prev_x
        dy = y - prev_y
        direction = get_direction(dx, dy)

        if direction != current_direction:
            if current_direction:
                description.append(f"Turn {current_direction} and go ahead {distance} px")
            distance = 0
            current_direction = direction

        distance += abs(dx) + abs(dy)
        prev_x, prev_y = x, y

    if current_direction:
        description.append(f"Turn {current_direction} and go ahead {distance} px")

    return description

def main():
    global image
    input_image_path = "ev.png"
    output_image_path = "map_with_path.png"
    target_color = (255, 255, 255)

    image = load_image(input_image_path)
    start_pixel = find_nearest_waypoint(image, (785, 1007), target_color)
    end_pixel =  find_nearest_waypoint(image, (2186, 763), target_color)

    path, rotations = dijkstra(image, start_pixel, end_pixel, target_color)
    print(f"Total rotations: {rotations}")
    draw_path(image, path, output_image_path)

    output_text_path = "path_description.txt"
    path_description = describe_path(path)
    with open(output_text_path, "w") as text_file:
        text_file.write("\n".join(path_description))
    print(f"Path description saved as {output_text_path}")

if __name__ == "__main__":
    main()