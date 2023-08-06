# MilkyWay
MilkyWay is an open source API for Robotics Path Planning

## Example of using the lib:

```python
# Import the main classes
from milkyway import Waypoint, Spline

# Create all Waypoint 
a = Waypoint(0, 0, angle=0,k=2)
b = Waypoint(1, 1, points=20, der2=0)
c = Waypoint(1, 2, angle=90)

# Make them into a spline
spline = Spline(a, b ,c)

# Plot them
spline.plot()
```

Easy!

## Main classes in MilkyWay:
MilkyWay lets you use two main classes:
  - `Waypoint` - A class representing a point in 2D space with some more info
  - `Spline` - A class representing a path between Waypoints

### Waypoints:
Waypoints are the base for every trajectory, you can create them like so:
```python
point = Waypoint(1, 0, angle=90, points=20, der2=0, k=2)
```
The arguments for a Waypoints are the following:
  - We specify location (1, 0).
  - You can specify the angle with the `angle` parameter. 
    - In degrees.
    - If you don't specify, MilkyWay will auto configure the angle to a continuous one.
  - You can specify the sample points for the following trajectory (Until the next Waypoint) with the `points` parameter.
  - You can specify the second derivative (advanced, don't touch or put 0) for better control of the spline, with the `der2` parameter.
  - You can specify the "curviness" of the parametric function with the `k` parameter.

### Spline:
Splines are the "glue" for Waypoints, Spline is an easy to use class:
```python
spline = Spline(point1, point2, point2, ...)
```

The parameters for the Spline are the Waypoints, the class does the rest.

&nbsp;&nbsp;

Some function you might use:

`get_linear_points` Will return all points between all Waypoints.
```python
spline.get_linear_points()
```
&nbsp;
The `plot` functions lets you view the spline, the `scatter` parameters sets the point scattering
```python
spline.plot(scatter=False)
```

