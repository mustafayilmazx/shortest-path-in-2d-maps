from dijkstra import find_path_with_dijkstra
from utils import load_image
from a_star import find_path_with_a_star
from lee import find_path_with_lee

image = load_image("ev.png")
find_path_with_dijkstra(image)
find_path_with_a_star(image)
find_path_with_lee(image)