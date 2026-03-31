import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from functools import cmp_to_key

def dist_sq(p1, p2):
    """Calculates the squared distance between two points."""
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def orientation(p, q, r):
    """
    Finds the orientation of an ordered triplet (p, q, r).
    Returns:
      0 --> p, q and r are collinear
      1 --> Clockwise (right turn)
      2 --> Counterclockwise (left turn)
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - \
          (q[0] - p[0]) * (r[1] - q[1])

    if val == 0: return 0  # Collinear
    return 1 if val > 0 else 2 # Clockwise or Counterclockwise

# Global variable to store the anchor point
p0 = None
animation_frames = []  # Stores (points, hull, current_i)

def store_frame(points, hull, current_i=None):
    animation_frames.append((points.copy(), hull.copy(), current_i))

# This compare() function (using a global anchor point p0 to sort by polar angle)
# follows the technique used in the GeeksforGeeks Graham Scan implementation:
# https://www.geeksforgeeks.org/convex-hull-algorithm-in-python/
def compare(p1, p2):
    """
    Comparison function for sorting points by polar angle with respect to p0.
    Used by functools.cmp_to_key.
    """
    global p0
    o = orientation(p0, p1, p2)

    if o == 0:
        # Collinear: Closer point comes first
        if dist_sq(p0, p2) >= dist_sq(p0, p1):
            return -1 # p1 comes first
        else:
            return 1  # p2 comes first
    elif o == 2:
        return -1 # Counterclockwise
    else:
        return 1  # Clockwise

def plot_step(points, hull, title, p0=None, current_i=None):
    """Plots the current state of the points and the convex hull."""
    plt.figure(figsize=(8, 6))

    # Plot all points
    X = [p[0] for p in points]
    Y = [p[1] for p in points]
    plt.plot(X, Y, 'o', label='All Points', color='blue')

    # Plot the hull
    if len(hull) >= 2:
        hull_x = [p[0] for p in hull]
        hull_y = [p[1] for p in hull]

        # Close the loop
        hull_x.append(hull[0][0])
        hull_y.append(hull[0][1])

        # Plot the hull edges
        plt.plot(hull_x, hull_y, 'r-', linewidth=2, label='Convex Hull (Current)')
        # Plot the hull points
        plt.plot(hull_x[:-1], hull_y[:-1], 'ro', markersize=8, label='Hull Points')

    # Highlight the anchor point
    if p0 is not None:
        plt.plot(p0[0], p0[1], 's', markersize=10, color='green', label='Anchor P0')

    # Highlight the point being processed
    if current_i is not None:
        plt.plot(points[current_i][0], points[current_i][1], 'X', markersize=12, color='orange', label='Current Point P_i')

    plt.title(title)
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()

# Visualization inspired by:
# AlgoVisuals. “Graham Scan convex hull visualization in Python.” YouTube, uploaded by AlgoVisuals, DD MMM YYYY, https://www.youtube.com/watch?v=IV-gD8VGVr4
def graham_scan(input_points):
    """Main function to run the Graham Scan algorithm and visualize steps."""
    global p0

    N = len(input_points)
    if N < 3:
        # not possible to find convex hull
        plot_step(input_points, input_points, f"Step 0: Convex Hull for {N} point(s)")
        return input_points

    # Find the bottom-most point. In case of a tie, the left-most point.
    p0_idx = min(range(N), key=lambda i: (input_points[i][1], input_points[i][0]))
    p0 = input_points[p0_idx]

    # Swap P0 to the first position
    input_points[0], input_points[p0_idx] = input_points[p0_idx], input_points[0]

    print("Step 1: Finding the Anchor Point (P0)")
    store_frame(input_points, [p0])

    # The list to sort is all points EXCEPT p0
    sorted_points = input_points[1:]
    sorted_points.sort(key=cmp_to_key(compare))

    # The final sorted list (p0 followed by the rest)
    points = [p0] + sorted_points

    print("\nStep 2: Sorting Points by Polar Angle from P0")
    # Plotting the sorted order before the scan
    store_frame(points, [p0, points[1], points[2]])

    # Initialize the hull with the first three points
    # (P0, the first sorted point P1, and the second sorted point P2)
    # The rest of the points are scanned.
    hull = [points[0], points[1], points[2]]

    print("\nStep 3: Initializing the Hull (P0, P1, P2)")
    store_frame(points, hull)

    # Scan the remaining points
    for i in range(3, N):
        current_point = points[i]

        print(f"\nScanning Point P{i} ({current_point}). Current Hull Size: {len(hull)}")

        # Keep removing the last point from the hull as long as the orientation formed is not a left turn
        while len(hull) > 1 and orientation(hull[-2], hull[-1], current_point) != 2:
            removed_point = hull.pop()
            print(f"  -> Right turn detected or collinear. Removing {removed_point} from hull.")
            # Optional: Plot step where a point is removed
            store_frame(points, hull, current_i=i)

        # Add the current point to the hull
        hull.append(current_point)
        print(f"  -> Left turn. Adding P{i} ({current_point}) to hull.")
        store_frame(points, hull, current_i=i)

    print("\nStep 4: Final Convex Hull")
    store_frame(points, hull)

    return hull

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

# Convert to a list of tuples
points_list = [list(p) for p in read_coordinates_from_file(file_path)]

# Run the algorithm and display the steps
final_hull = graham_scan(points_list)
fig, ax = plt.subplots(figsize=(8, 6))

def update(frame_idx):
    ax.clear()
    points, hull, current_i = animation_frames[frame_idx]

    # All points
    X = [p[0] for p in points]
    Y = [p[1] for p in points]
    ax.plot(X, Y, 'o', color='blue', markersize=5, label='All Points')

    # Hull edges
    if len(hull) >= 2:
        hx = [p[0] for p in hull] + [hull[0][0]]
        hy = [p[1] for p in hull] + [hull[0][1]]
        ax.plot(hx, hy, 'r-', linewidth=2, label='Hull Edges')
        ax.plot([p[0] for p in hull], [p[1] for p in hull], 'ro', markersize=8, label='Hull Points')

    # Anchor P0
    ax.plot(p0[0], p0[1], 's', color='green', markersize=10, label='Anchor P0')

    # Current scanning point
    if current_i is not None:
        ax.plot(points[current_i][0], points[current_i][1], 'X', color='orange', markersize=12, label='Current P_i')

    ax.set_title(f"Graham Scan Step {frame_idx+1}")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.grid(True)
    ax.legend(loc='upper left')

ani = FuncAnimation(fig, update, frames=len(animation_frames), interval=200, repeat=False)
plt.show()

print(f"Original Points: {points_list}")
print(f"Final Convex Hull Points: {final_hull}")