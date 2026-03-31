import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.animation import FuncAnimation
#from IPython.display import HTML
import time
#Networkx tutroial:
#https://www.geeksforgeeks.org/python/networkx-python-software-package-study-complex-networks/
a=time.time()
left=[]
right=[]
on_line=[]
final_set=[]
animation=[]

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

input= read_coordinates_from_file(file_path)
# Source - https://stackoverflow.com/a
# Posted by Michael J. Barber
# Retrieved 2025-11-24, License - CC BY-SA 3.0

input = sorted(input, key=lambda element: (element[0],element[1]))



min=input[0]
max=input[len(input)-1]
x1, y1 = min
x2, y2 = max
final_set.append(min)
final_set.append(max)
#animation.append(final_set.copy())
def pointlocation(p1, p2, p3):
  #Equation gotten from GeeksforGeeks
   orientation = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
   return orientation

for i in range(len(input)):
  if(input[i]!=min and input[i]!=max):
   unkown=input[i]
   locate= pointlocation(min, max, input[i])
   if locate>0:
     left.append(unkown)
   if locate<0:
     right.append(unkown)
   if locate==0:
    on_line.append(unkown)


def furthest_point(input, p1, p2):
  furthest_point= None
  if(p1==p2):
    return 0
  max=0
  perp_distance=math.sqrt((p2[0]-p1[0])**2 +(p2[1]-p1[1])**2)
  for i in input:
    distance = abs(pointlocation(p1, p2, i)) / perp_distance

    if distance > max:
      max = distance
      furthest_point = i

  return furthest_point


def quickhull(input, p1, p2, hull):
  p1pk=[]
  p2pk=[]
  pk = furthest_point(input, p1, p2)
  if pk is None :
    if p1 not in hull:
      hull.append(p1)
    if p2 not in hull:
      idx=hull.index(p1)
      hull.insert(idx+1, p2)
    animation.append(hull.copy())
    return
  if(p1 in hull and p2 in hull):
    loc=hull.index(p1)
    hull.insert(loc+1, pk)
  else:
    hull.append(pk)
  animation.append(hull.copy())


  for i in input:
    if pointlocation(p1, pk, i)>0:
      p1pk.append(i)
    if pointlocation(pk, p2, i)>0:
      p2pk.append(i)


  quickhull(p1pk, p1, pk, hull)
  quickhull(p2pk, pk, p2, hull)



quickhull(left, min, max, final_set)
quickhull(right, max, min, final_set)
#///////////////////////////////////////////
ordered_final=final_set
#//////////////////////////////////////////

fig, ax = plt.subplots(figsize=(8, 8))

graph = nx.Graph()
pos = {}
for p in input:
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

        nx.draw_networkx_nodes(graph, pos, nodelist=hull, node_color='green', node_size=80, ax=ax)

        edges = []
        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]
            edges.append((p1, p2))
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2, ax=ax)


    blue_dot = plt.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=5, label='Original Points')
    green_dot = plt.Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='Hull Points')
    red_line = plt.Line2D([], [], color='red', linestyle='-', linewidth=2, label='Hull Edges')
    ax.legend(handles=[blue_dot, green_dot, red_line], loc='upper left')

ani = FuncAnimation(fig, update, frames=len(animation), interval=100, repeat=False)
from IPython.display import HTML
plt.show()

b=time.time()
e=b-a
print(e)

