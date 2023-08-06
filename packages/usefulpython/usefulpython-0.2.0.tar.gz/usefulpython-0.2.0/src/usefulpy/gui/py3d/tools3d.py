'''
3d tools

tools for 3d processing

LICENSE PLATAFORMS and INSTALLATION:
This is a section of usefulpy. See usefulpy.__init__ and usefulpy license
file

RELEASE NOTES:
0
 0.0
  Version 0.0.0:
   Tools for processing 3d: will probably be merged into a future 
   mathematics.linear_algebra or .vectors?
'''

### DUNDERS ###
__author__ = 'Augustin Garcia'
__version__ = '0.0.0'

### IMPORTS ###
from ...mathematics import quaternion, i, j, k, isclose
import random

### TOOLS ###
test_pane = ((-3*i-2j-1*k), (-i+2j+1*k), (i-j-2*k))

def random_plane():
    points = []
    for n in range(3):
        a = [0]
        for k in range(3):
            a.append(random.randint(-3, 3))
        points.append(quaternion(*a))
    return tuple(points)

def random_point():
    a = [0]
    for k in range(3):
        a.append(random.randint(-3, 3))
    return quaternion(*a)

def shift_plane(plane):
    a, b, c = plane
    return (a-b).normal(), (a-c).normal()

def versor_from_points(plane):
    a, b = shift_plane(plane)
    return a.cross(b).normal()

def points_6(plane):
    d, f = shift_plane(plane)
    
    q1 = (d-(d.i/f.i)*f).normal()
    q2 = -q1
    q3 = versor_from_points(plane)
    q4 = -q3
    q5 = q1.cross(q3).normal()
    q6 = -q5
    return q1, q2, q3, q4, q5, q6

def equation(plane):
    q1, q2, q3 = plane
    x1, y1, z1 = q1.i, q1.j, q1.k
    x2, y2, z2 = q2.i, q2.j, q2.k
    x3, y3, z3 = q3.i, q3.j, q3.k
      
    a1 = x2 - x1 
    b1 = y2 - y1 
    c1 = z2 - z1 
    a2 = x3 - x1 
    b2 = y3 - y1 
    c2 = z3 - z1 
    a = b1 * c2 - b2 * c1 
    b = a2 * c1 - a1 * c2 
    c = a1 * b2 - b1 * a2 
    d = (- a * x1 - b * y1 - c * z1)
    if c != 0:
        return lambda x, y: -(a*x+b*y+d)/c
    return NotImplemented

def point_at(plane, x, y):
    c = plane[2]
    d, f = shift_plane(*plane)
    if f.i != 0:
        shifty_base = (d-(d.i/f.i)*f)
    if f.j != 0:
        shiftx_base = (d-(d.j/f.j)*f)
    shifty = (1/shifty_base.j)*shifty_base
    shiftx = (1/shiftx_base.i)*shiftx_base
    xs, ys = c.i, c.j
    xshift = x-xs
    yshift = y-ys
    nx = xshift*shiftx
    ny = yshift*shifty
    return c+nx+ny

def is_on_plane(plane, point):
    x, y = point.i, point.j
    new_point = point_at(plane, x, y)
    return isclose(point, new_point)

def _same_side(p1, p2, a, b):
    cp1 = (b-a).cross(p1-a)
    cp2 = (b-a).cross(p2-a)
    return cp1.dot(cp2) >= 0

def PointInTriangle(p, a, b, c):
    if not is_on_plane((a, b, c), p):
        return False
    if not _same_side(p, a, b, c):
        return False
    if not _same_side(p, b, a, c):
        return False
    if not _same_side(p, c, a, b):
        return False
    return True
