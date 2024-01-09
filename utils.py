TARGET_COLOR = (255, 255, 255)
IMAGE_PATH = "ev.png"
OUTPUT_PNG = "ev.png"
START_PIXEL = (785, 1007)
END_PIXEL = (2186, 763)

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

def draw_path(image, path, output_path):
    """Draw the path on the image and save it."""
    image_with_path = image.copy()
    draw = ImageDraw.Draw(image_with_path)
    size = 5
    for x, y in path:
        draw.ellipse((x - size, y - size, x + size, y + size), fill=(255, 255, 0))
    save_image(image_with_path, output_path)
    print(f"Path image saved as {output_path}")

def is_valid_pixel(pixel, image):
    """Check if a pixel is valid (i.e., matches the target color)."""
    x, y = pixel
    width, height = image.size
    return 0 <= x < width and 0 <= y < height and image.getpixel((x, y))[0:3] == TARGET_COLOR

def get_neighbors(pixel, current_direction, image):
    x, y = pixel
    directions = [(1, 0, "right"), (-1, 0, "left"), (0, 1, "down"), (0, -1, "up")]
    neighbors = []
    for dx, dy, new_direction in directions:
        neighbor = (x + dx, y + dy)
        if is_valid_pixel(neighbor, image):
            rotation = 1 if new_direction != current_direction else 0
            neighbors.append((neighbor, new_direction, rotation))
    return neighbors