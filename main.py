from dijkstra import find_path_with_dijkstra
from utils import load_image
from a_star import find_path_with_a_star
from lee import find_path_with_lee
import time
image = load_image("ev.png")

start = time.time()
find_path_with_dijkstra(image)
end = time.time()
print("Dijkstra: ", end - start)

start = time.time()
find_path_with_a_star(image)
end = time.time()
print("A*: ", end - start)

start = time.time()
find_path_with_lee(image)
end = time.time()
print("Lee: ", end - start)