# Convex-Hull
Authored by [Leon Hartley](https://github.com/hartleyleo) & [Brennan Rivera](https://github.com/omw2code)

This code was created as part of an assignment for [URI CSC 440](https://www.coursicle.com/uri/courses/CSC/440/) where we found the [Convex Hull](https://mathworld.wolfram.com/ConvexHull.html) of a set of points in a 2D grid. 

NOTE: The draw_hull.py file was supplied, and in the convex_hull.py file the functions, y_intercept, triangle_area, is_clockwise, is_counter_clockwise, collinear, and sort_clockwise were also all supplied by our professor, [Noah Daniels](https://web.uri.edu/cs/meet/noah-daniels/).

## ❓ Problem
We would like to find the Convex Hull of a set of given points on a 2D grid. The convex hull is the outtermost set of points that contain all other points inside of it. When a line segment has all other points on the side facing the origin, then this line segment is on the hull.

## 🚀 Usage
1. Have a valid Python installation installed on device.
2. Clone code locally.
3. Run the `draw_hull.py` file.
4. Draw any set of points desired, and then hit run!

## 📖 Methodology
We want to get the Convex Hull of a set of points by using a Divide and Conquer approach. This means that we will recursively traverse the set of points and compute said hull.

The method we used:
1. Load in all points and sort them to be clockwise.
2. The algorithm starts with a base case check. If the number of points is small enough (typically <= 5), the call switches and runs a naive algorithm, we use we Andrews Algorithm here.
3. If the number of points exceeds the threshold set for the base case, the algorithm splits the set of points into two halves, left and right.
4. The recursive calls will ensure there are a large set of multiple small hulls that we now have to combine.
5. To combine the hulls we find the rightmost point of the left hull and the leftmost point of the right hull. Then, it determines the top and bottom connector tangent line segments between the two hulls to merge them. This gets the combined hull of both smaller hulls. 
6. The combined hull is then sorted in clockwise order and processed to remove any duplicate points.
7. The algorithm will run this all the way up to the main hull and display the computed hull.
