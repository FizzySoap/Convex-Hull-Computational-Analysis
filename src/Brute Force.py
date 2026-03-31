
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.animation import FuncAnimation
#from IPython.display import HTML

import re
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "data_points.txt")
def read_coordinates_from_file(file_path):
    points_data = []
    try:
        with open(file_path, 'r') as f:
            content = f.read()

            # Find all (number, number) patterns using regex
            # and convert them to float tuples
            pattern = re.compile(r'\(([\d\.]+),\s*([\d\.]+)\)')
            matches = pattern.findall(content)

            for match in matches:
                x = float(match[0])
                y = float(match[1])
                points_data.append((x, y))

        return points_data

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []

points=read_coordinates_from_file(file_path)

def sort_mess(points):
  cx = sum(p[0] for i in points) / len(points)
  cy = sum(p[1] for p in points) / len(points)
  return sorted(points, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
def orientation(A, B, C):
  (x1, y1) = A
  (x2, y2) = B
  (x3, y3) = C
  return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

def brute_force_hull(points):
  animation=[]
  hull_points=set()
  hulledges = []
  n = len(points)
  for i in range(n):
    for j in range(n):
      if i == j:
        continue

      A = points[i]
      B = points[j]

      left = False
      right = False

      is_hull_edge = True

      for k in range(n):
        if k == i or k == j:
          continue

        C = points[k]
        val = orientation(A, B, C)

        if val > 0:
          left = True
        elif val < 0:
          right = True


        if left and right:
          is_hull_edge = False
          break


      if is_hull_edge:
        hulledges.append((A, B))
        hull_points.add(A)
        hull_points.add(B)
        animation.append(list(hull_points))

  return hulledges , animation

edge,animation = brute_force_hull(points)


fig, ax = plt.subplots(figsize=(8, 8))

graph = nx.Graph()
pos = {}
for p in points:
    graph.add_node(p)
    pos[p] = p

def update(frame_idx):
    ax.clear()
    ax.set_title(f'Convex Hull – Step {frame_idx + 1}')
    ax.set_xlabel('X-coordinate')
    ax.set_ylabel('Y-coordinate')
    ax.grid(True)

    nx.draw_networkx_nodes(graph, pos, node_color='blue', node_size=30, ax=ax)


    hull = animation[frame_idx]
    if len(hull) > 1:
      sorted_hull = sort_mess(hull)

      nx.draw_networkx_nodes(graph, pos, nodelist=hull, node_color='green', node_size=80, ax=ax)

      edges = []
      for i in range(len(sorted_hull)):
          p1 = sorted_hull[i]
          p2 = sorted_hull[(i + 1) % len(hull)]
          edges.append((p1, p2))
      nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2, ax=ax)


    blue_dot = plt.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=5, label='Original Points')
    green_dot = plt.Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='Hull Points')
    red_line = plt.Line2D([], [], color='red', linestyle='-', linewidth=2, label='Hull Edges')
    ax.legend(handles=[blue_dot, green_dot, red_line], loc='upper left')

ani = FuncAnimation(fig, update, frames=len(animation), interval=100, repeat=False)
#HTML(ani.to_jshtml())
plt.show()
