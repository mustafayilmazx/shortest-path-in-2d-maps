from PIL import Image, ImageDraw
import heapq
import math
import numpy as np

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    image.save(output_path)

# we will find nearest waypoint to the given pixel
# first go to up find white pixel and define it as waypoint, also define its distance
# make same thing for down, left and right pixels but if distance is smaller than previous one
# return nearest waypoint's coordinates and distance
def find_nearest_waypoint(image, pixel, target_color):
    width, height = image.size
    x, y = pixel
    distance = float('inf')
    nearest_waypoint = None

    for i in range(y):
        if image.getpixel((x, y - i))[0:3] == target_color:
            if i < distance:
                distance = i
                nearest_waypoint = (x, y - i)
            break

    for i in range(height - y):
        if image.getpixel((x, y + i))[0:3] == target_color:
            if i < distance:
                distance = i
                nearest_waypoint = (x, y + i)
            break

    for i in range(x):
        if image.getpixel((x - i, y))[0:3] == target_color:
            if i < distance:
                distance = i
                nearest_waypoint = (x - i, y)
            break

    for i in range(width - x):
        if image.getpixel((x + i, y))[0:3] == target_color:
            if i < distance:
                distance = i
                nearest_waypoint = (x + i, y)
            break

    return nearest_waypoint

def find_shortest_path(start, end, is_valid, get_neighbors):
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

        for neighbor, new_direction, rotation in get_neighbors(current, direction):
            new_x, new_y = neighbor

            if not visited[new_x][new_y] and is_valid(neighbor):
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

def dijkstra(image, start_pixel, end_pixel, target_color):
    width, height = image.size

    def is_valid(pixel):
        x, y = pixel
        return 0 <= x < width and 0 <= y < height and image.getpixel((x, y))[0:3] == target_color

    def get_neighbors(pixel, current_direction):
        x, y = pixel
        directions = [(1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")]
        neighbors = []
        for dx, dy, new_direction in directions:
            neighbor = (x + dx, y + dy)
            if is_valid(neighbor):
                rotation = 1 if new_direction != current_direction else 0
                neighbors.append((neighbor, new_direction, rotation))
        return neighbors

    path, total_rotations = find_shortest_path(start_pixel, end_pixel, is_valid, get_neighbors)

    image_with_path = image.copy()
    draw = ImageDraw.Draw(image_with_path)
    for x, y in path:
        # we will draw waypoints as circles
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 255, 0))  # Paint the path yellow.

    return image_with_path, path, total_rotations

def describe_path(path):
    description = []
    prev_x, prev_y = path[0]
    current_direction = None
    distance = 0

    for x, y in path[1:]:
        dx = x - prev_x
        dy = y - prev_y

        if dx > 0:
            direction = "right"
        elif dx < 0:
            direction = "left"
        else:
            direction = ""

        if dy > 0:
            direction = "down"
        elif dy < 0:
            direction = "up"

        if direction != current_direction:
            if current_direction:
                description.append(f"Turn {current_direction} and go ahead {distance} px")
            if direction:
                distance = max(abs(dx), abs(dy))
            else:
                distance = 0
            current_direction = direction
        else:
            distance += max(abs(dx), abs(dy))

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

    result_image, path, rotations = dijkstra(image, start_pixel, end_pixel, target_color)
    save_image(result_image, output_image_path)
    print(f"Path image saved as {output_image_path}")
    print(f"Total rotations: {rotations}")

    output_text_path = "path_description.txt"
    path_description = describe_path(path)
    with open(output_text_path, "w") as text_file:
        text_file.write("\n".join(path_description))
    print(f"Path description saved as {output_text_path}")

if __name__ == "__main__":
    main()
