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
    left_points = []
    right_points = []
    
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


"""
---------------------------------------------------
            MERGING TWO HULLS FUNCTIONS                     
---------------------------------------------------
"""

def findHullsRightMostPoint(hull: List[Point]) -> Point:
    """
    Function to get the right most point of a list of points
    """
    # Set current right most point to the first index
    rightmost:Point = hull[0]
    
    # Search for a point with a more positive x value
    for i in range(1, len(hull)):
        
        # If the x value is > the current right most point's x
        if (hull[i])[0] > rightmost[0]:
            rightmost = hull[i]
            
    return rightmost

def findHullsLeftMostPoint(hull: List[Point]) -> Point:
    """
    Function to get the left most point of a list of points
    """
    # Set current left most point to the first index
    leftmost:Point = hull[0]
    
    # Search for a point with a more negative x value
    for i in range(1, len(hull)):
        
        # If the x value is < the current left most point's x
        if (hull[i])[0] < leftmost[0]:
            leftmost = hull[i]
            
    return leftmost

def find_top_connector_line_segment(left_hull: List[Point], right_hull: List[Point], left_hull_rightmost_point: Point, right_hull_leftmost_point: Point, midpoint_line: float) -> Tuple[Point, Point]:
    """
    Function to find the top most connecting line segment between two hulls
    """
    # Hold placeholders for the best point in each hull for the best line segment verticies
    best_case_right_hull_point = right_hull_leftmost_point
    best_case_left_hull_point = left_hull_rightmost_point
    
    # Used to hold the current best y-intercept, mainly used for a lightly more efficient
    best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
    
    # Variables to store repeated info
    right_length = len(right_hull)
    left_length = len(left_hull)
    
    # Loop through indecies to find the top most connecting line segment between the two hulls
    # Check if the y-intercepts of the new hull point and the opposing hull's current best case point are less than the current best y-intercept, if so then do work
    while (y_intercept(right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length], best_case_left_hull_point, midpoint_line) < best_case_y_intercept or y_intercept(left_hull[(left_hull.index(best_case_left_hull_point) - 1) % left_length], best_case_right_hull_point, midpoint_line) < best_case_y_intercept):
        
        if (y_intercept(best_case_left_hull_point, right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length], midpoint_line) > best_case_y_intercept):
            # Move to the previous point in the left hull if its y-intercept is lower, consider it the best case
            best_case_left_hull_point = left_hull[(left_hull.index(best_case_left_hull_point) - 1) % left_length]
            best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
            
        else:
            # Move to the next point in the right hull if its y-intercept is lower, consider it the best case
            best_case_right_hull_point = right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length]
            best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
            

    return best_case_left_hull_point, best_case_right_hull_point


def find_bottom_connector_line_segment(left_hull: List[Point], right_hull: List[Point], left_hull_rightmost_point: Point, right_hull_leftmost_point: Point, midpoint_line: float):
    """
    Function to find the bottom most connecting line segment between two hulls
    """
    # Hold placeholders for the best point in each hull for the best line segment verticies
    best_case_right_hull_point = right_hull_leftmost_point
    best_case_left_hull_point = left_hull_rightmost_point
    
    # Used to hold the current best y-intercept, mainly used for a lightly more efficient
    best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
    
    # Variables to store repeated info
    right_length = len(right_hull)
    left_length = len(left_hull)
    
    # Loop through indecies to find the bottom most connecting line segment between the two hulls
    # Check if the y-intercepts of the new hull point and the opposing hull's current best case point are greater than the current best y-intercept, if so then do work
    while (y_intercept(right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length], best_case_left_hull_point, midpoint_line) > best_case_y_intercept or y_intercept(left_hull[(left_hull.index(best_case_left_hull_point) - 1) % left_length], best_case_right_hull_point, midpoint_line) > best_case_y_intercept):
        
        if (y_intercept(best_case_left_hull_point, right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length], midpoint_line) < best_case_y_intercept):
            # Move to the previous point in the left hull if its y-intercept is higher, consider it the best case
            best_case_left_hull_point = left_hull[(left_hull.index(best_case_left_hull_point) - 1) % left_length]
            best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
            
        else:
            # Move to the previous point in the right hull if its y-intercept is higher, consider it the best case
            best_case_right_hull_point = right_hull[(right_hull.index(best_case_right_hull_point) + 1) % right_length]
            best_case_y_intercept = y_intercept(best_case_left_hull_point, best_case_right_hull_point, midpoint_line)
            
    
    return best_case_left_hull_point, best_case_right_hull_point

def combine(left_hull: List[Point], right_hull: List[Point]) -> List[Point]:
    """
    Function to combine two hulls together by using the two finger walking algorithm
    """   
    # Find right most point of left hull
    left_hull_rightmost_point = findHullsRightMostPoint(left_hull)
    
    # Find left most point of right hull
    right_hull_leftmost_point = findHullsLeftMostPoint(right_hull)
    
    # Get the line to find highest and lowest y-intercept with
    midpoint_line = (left_hull_rightmost_point[0] + right_hull_leftmost_point[0]) / 2
    
    # Clockwise sort both hulls to ensure points are walked correctly
    sort_clockwise(left_hull)
    sort_clockwise(right_hull)
    
    # Find top and bottom connector line segments
    top_left_point, top_right_point = find_top_connector_line_segment(left_hull, right_hull, left_hull_rightmost_point, right_hull_leftmost_point, midpoint_line)
    bottom_left_point, bottom_right_point = find_bottom_connector_line_segment(left_hull, right_hull, left_hull_rightmost_point, right_hull_leftmost_point, midpoint_line)
    
    # Merge the hulls via
    
    # Create empty hull list
    combined_hull = []
    
    # 1. Adding the lower left point to the hull, then adding all points afterwords until it hits the top left point
    index = left_hull.index(bottom_left_point)
    while left_hull[index] is not top_left_point:
        combined_hull.append(left_hull[index])
        index = (index + 1) % len(left_hull)
    
    # 2. Append the top left and then top right point in order
    combined_hull.append(top_left_point)
    combined_hull.append(top_right_point)
    
    # 3. Loop again adding all points in the right hull from the top right point to the bottom right point
    index = right_hull.index(top_right_point)
    while right_hull[index] is not bottom_right_point:
        combined_hull.append(right_hull[index])
        index = (index + 1) % len(right_hull)
    
    # 4. Add the bottom right point and the bottom left point to the hull
    combined_hull.append(bottom_right_point)
    combined_hull.append(bottom_left_point)
    
    return combined_hull 

# REFERENCE: https://algorithmtutor.com/Computational-Geometry/Convex-Hull-Algorithms-Graham-Scan/
def base_case_hull(points: List[Point]) -> List[Point]:
    """ 
    Base case of the recursive algorithm.
    """
    # BASE base case, any combination of <= 3 points will just be the actual hull
    if len(points) <= 3:
        return points
    else:
        # Naive algorithm 

        # Graham Scan Algo:
        
        # 1. Get a starting point: the lowest y coordinate
        #  If there are two points with the same y value, 
        #  then the point with smaller x coordinate value is considered
        start_point = points[0]

        for point in points[1:]:
            if point[1] < start_point[1] or (point[1] == start_point[1] and point[0] < start_point[0]):
                start_point = point

        # 2. Consider the remaining points and sort them by polar angle in counterclockwise order around points[0]. 
        #  If the polar angle of two points is the same, then put the nearest point first
        sorted_points = points[:]
        sorted_points.remove(start_point)
        sort_clockwise(sorted_points)
        
        # 2.1 if more than two points are collinear with start_point, keep the farthest
        to_remove = []
        for i in range(len(sorted_points) - 1):
            if collinear(start_point, sorted_points[i], sorted_points[i + 1]):
                to_remove.append(sorted_points[i])

        for point in to_remove:
            sorted_points.remove(point)
        
        # Add the two points, P0 and the closest point to P0 with the smallest polar angle
        hull = [start_point, sorted_points[0]]

        # Compute the hull with the remaining sorted points
        for point in sorted_points[1:]:
            while len(hull) >= 2 and not is_clockwise(hull[-2], hull[-1], point):
                # If the angle turns clockwise, just remove from hull
                del hull[-1]
            hull.append(point)

        sort_clockwise(hull)
        return hull


def compute_hull(points: List[Point]) -> List[Point]:
    """
    Given a list of points, computes the convex hull around those points
    and returns only the points that are on the hull.
    """
    # Checks the length to see if it can just be brute forced or not
    if len(points) <= 5:
        return base_case_hull(points)
    else:
        
        # Split the points into two halves
        left_points, right_points = split_in_two(points)
        
        # Compute the hull of the left and right half's points
        left_hull = compute_hull(left_points)
        right_hull = compute_hull(right_points)
        
        # Combine the two hulls
        return combine(left_hull, right_hull)