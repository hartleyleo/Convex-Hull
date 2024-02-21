import math
import sys
from typing import List
from typing import Tuple

EPSILON = sys.float_info.epsilon
Point = Tuple[int, int]


def y_intercept(p1: Point, p2: Point, x: int) -> float:
    """
    Given two points, p1 and p2, an x coordinate from a vertical line,
    compute and return the the y-intercept of the line segment p1->p2
    with the vertical line passing through x.
    """
    x1, y1 = p1
    x2, y2 = p2
    slope = (y2 - y1) / (x2 - x1)
    return y1 + (x - x1) * slope


def triangle_area(a: Point, b: Point, c: Point) -> float:
    """
    Given three points a,b,c,
    computes and returns the area defined by the triangle a,b,c.
    Note that this area will be negative if a,b,c represents a clockwise sequence,
    positive if it is counter-clockwise,
    and zero if the points are collinear.
    """
    ax, ay = a
    bx, by = b
    cx, cy = c
    return ((cx - bx) * (by - ay) - (bx - ax) * (cy - by)) / 2


def is_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) < -EPSILON


def is_counter_clockwise(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c represents a counter-clockwise sequence
    (subject to floating-point precision)
    """
    return triangle_area(a, b, c) > EPSILON


def collinear(a: Point, b: Point, c: Point) -> bool:
    """
    Given three points a,b,c,
    returns True if and only if a,b,c are collinear
    (subject to floating-point precision)
    """
    return abs(triangle_area(a, b, c)) <= EPSILON


def sort_clockwise(points: List[Point]):
    """
    Sorts `points` by ascending clockwise angle from +x about the centroid,
    breaking ties first by ascending x value and then by ascending y value.

    The order of equal points is not modified

    Note: This function modifies its argument
    """
    # Trivial cases don't need sorting, and this dodges divide-by-zero errors
    if len(points) < 2:
        return

    # Compute the centroid
    centroid_x = sum(p[0] for p in points) / len(points)
    centroid_y = sum(p[1] for p in points) / len(points)

    # Sort by ascending clockwise angle from +x, breaking ties with ^x then ^y
    def sort_key(point: Point):
        angle = math.atan2(point[1] - centroid_y, point[0] - centroid_x)
        normalized_angle = (angle + math.tau) % math.tau
        return (normalized_angle, point[0], point[1])

    # Sort the points
    points.sort(key=sort_key)


# Self implemented functions

def split_in_two(points: List[Point]):
    """
    Split all points into two lists that represent the left and right sub-hull
    
    Because we want to split the hull into two via a middle point, we find the x values of all points, then sorts them into the two lists based off of their x value being < || > the middle most point
    """
    # Set the point lists
    left_points = list()
    right_points = list()
    
    # Set the x value list
    x_values = []
    
    # Populate x value list with all x values
    for [x, y] in points:
        x_values.append(x)
    
    # Find the middle value
    middle_x = sum(x_values) / len(points)
    
    # Filter points to halves based on their x value
    for i in range(len(points)):
        
        # If the x value is less than or equal to the midpoint
        if points[i][0] <= middle_x:
            left_points.append(points[i])
        else :
            right_points.append(points[i])
    
    return left_points, right_points


def combine(left_hull, right_hull):
    # TODO: Implement the function
    return hull

#REFERENCE: https://algorithmtutor.com/Computational-Geometry/Convex-Hull-Algorithms-Graham-Scan/
def base_case_hull(points: List[Point]) -> List[Point]:
    """ Base case of the recursive algorithm.
    """
    # TODO: You need to implement this function.

    #Graham Scan Algo:

    #1. Get a starting point: the lowest y coordinate
    #       If there are two points with the same y value, 
    #       then the point with smaller x coordinate value is considered
    start_point = points[0]

    for point in points[1:]:
        if point[1] < start_point[1] or (point[1] == start_point[1] and point[0] < start_point[0]):
            start_point = point

    #2. Consider the remaining points and sort them by polar angle in counterclockwise order around points[0]. 
        #    If the polar angle of two points is the same, then put the nearest point first
    sorted_points = points[:]
    sorted_points.remove(start_point)
    sort_clockwise(sorted_points)
    
        #2.1 if more than two points are collinear with start_point, keep the farthest
    to_remove = []
    for i in range(len(sorted_points) - 1):
        if collinear(start_point, sorted_points[i], sorted_points[i + 1]):
            to_remove.append(sorted_points[i])

    for point in to_remove:
        sorted_points.remove(point)
    
    #add the two points, P0 and the closest point to P0 with the smallest polar angle
    hull = [start_point, sorted_points[0]]

    #compute the hall with the remaining sorted points
    for point in sorted_points[1:]:
        while len(hull) >= 2 and not is_clockwise(hull[-2], hull[-1], point):
            #if the angle turns clockwise, just remove from hall
            del hull[-1]
        hull.append(point)


    return hull


def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    if len(points) <= 5:
        return base_case_hull(points)
    else:
        left_points, right_points = split_in_two(points)
        
        left_points = compute_hull(left_points)
        right_points = compute_hull(right_points)
        
        return combine(left_points, right_points)
