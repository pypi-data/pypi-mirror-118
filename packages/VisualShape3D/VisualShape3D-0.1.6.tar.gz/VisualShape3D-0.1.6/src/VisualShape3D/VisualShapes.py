import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .Utils import Array, Equal,ScalarZero,ScalarEqual,Round,UnitVector, Dot
from .Utils import PolygonNormal, SegmentXPolygon, GetU
from .Utils import PointInSegment, PointInLine, PointInPolygon
from .Utils import AngleBetween, NormalToLine, LineXLine, LineXPlane,CreateCoordinates

from .Shapes import regularPolygon, createShape
from .Shapes import add_col # as arange_col  # add_third_col
from .Shapes import move as change
from .Constant import get_eps,get_sig_figures

from .Rendering import Visible, Point


### 3D View Function of a Geometry 
#
#  Its plotting follows the strategy of pyny3D
#  Liqun He, 2020/10/27
#
class Polygon(Visible):
### Initialization
    """
    A visible 3D polygon.
    It is iterable, and when indexed, it returns the vertices.
    
    The polygon's vertices are a ndarray of 3D points 
          np.array(N, 2 or 3) for (xyz or xy).

    It requires a open loop, the first point != the end point.

    NOTE:: In future, this object can be locked for calculation once,  
    for a rapid rendering.
    """
    verify = True
    def __init__(self, points, **kwargs):
        
        # Input errors
        if len(points) < 3:
            raise ValueError("Polygon must have at least three vertices.")

        if type(points) != np.ndarray:
           points = np.array(points)
                
        # Adapt 2D/3D
        if points.shape[1] == 2:
            # from Shapes import add_col
            points = np.hstack((points, add_col(points.shape[0])*0))

        elif points.shape[1] != 3:
            raise ValueError('VisualGeom.Polygon needs 2 or 3 coords '+\
                             '(columns) at least')

        # Basic processing
        self.vertices = points
        self.p = self.vertices[0]
        self.n = PolygonNormal(self.vertices)
        
        # Optional processing
        self.path = None
        self.parametric = None
        self.shapely = None
        
        # Parameters
        self.locked = False
        self.domain = None
        self.area = None
                

        super().__init__()

    def __str__(self):
        s = ""
        for point in self.vertices:
            if s:
                s += " -> "
            s += str(point)
        return s

    def __hash__(self):
        return hash(tuple(sorted(self.vertices, key=lambda p: p.x)))

    def __iter__(self): return iter(self.vertices)

    def __getitem__(self, key): return self.vertices[key]
        
    def lock(self):
        """
        It locks some polygons for calculation, 
        by using ``self.domain`` and ``self.path`` 

        ***warning***: Unnecessary locks can slow down the calculation.
        """
        if not self.locked:
            self.path = self.get_path()
            self.domain = self.get_domain()
            self.locked = True

    def to_2d(self):
        """
        To calculate the local coordinates of vertices.
        """

        # Create the matrix from global to local systems
        U = self.getU()
        # U = self.matrix()  # in future
        
        # Local coordiantes
        dR = self.vertices - self[0]   # The first vertice as the origin
        r = np.dot(U, dR.T).T
        r[np.isclose(r, 0.0)] = 0.0
        
        # print(r.shape)
        return Polygon(r[:, :2])
        
    def plot2d(self, style = ('wheat', 'yellowgreen', 1)):
        """
        It plots the 2D Polygon
        
        Inputs 
           1)style = color, edge_color, alpha ):
               (1)      color: 'default', matplotlib color for polygon
               (2) edge_color : 'k'     , matplotlib color for edge
        :      (3)       alpha:  1,      pacity, float
        :  2) ret: If True, the function returns the figure, so as to add 
                 more elements to the plot or to modify it.
        
        Output: 
          None or axes(matplotlib axes)
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        (color,edge_color,alpha) = style
        path = self.to_2d().get_path()
        domain = self.to_2d().get_domain()[:, :2]

        if color == 'default': color = 'yellowgreen'

        # Plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.add_patch(patches.PathPatch(path, facecolor=color, lw=1, 
                                       edgecolor=edge_color, alpha=alpha))
        ax.set_xlim(domain[0,0],domain[1,0])
        ax.set_ylim(domain[0,1], domain[1,1])

        return plt,ax

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def seed2pyny(self, seed):
        return Polygon(**seed)

    def get_domain(self):
        """
        :returns: opposite vertices of the bounding prism for this object.
        :       ndarray([min], [max])
        """
        if self.domain is None:
            # Min/max along the column
            return np.array([self.vertices.min(axis=0),  # min (x,y,z)
                             self.vertices.max(axis=0)]) # max (x,y,z)
        return self.domain

    def iplot(self, style, ax, **kwargs):

        plotable3d = self.__get_plotable_data()

        facecolor = self.facecolor  
        edgecolor = self.edgecolor  
        linewidth = self.linewidth  
        alpha     = self.alpha      

        if 'facecolor' in style : facecolor = style['facecolor'] 
        if 'edgecolor' in style : edgecolor = style['edgecolor'] 
        if 'linewidth' in style : linewidth = style['linewidth'] 
        if 'alpha'     in style : alpha     = style['alpha']     

        for polygon in plotable3d:
            polygon.set_facecolor(facecolor)
            polygon.set_edgecolor(edgecolor)
            polygon.set_linewidth(linewidth)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def __get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        # import mpl_toolkits.mplot3d as mplot3d
        # return [mplot3d.art3d.Poly3DCollection([self.vertices])]
        return [Poly3DCollection([self.vertices])]

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict information as required by Polygon's arguments
        For Polygon(points)
        it returns arguments in dicttionary form :
                   {"points": vertices} 
        """
        return {'points': self.vertices}

    def intersect(self,segment) :
        if isinstance(segment, Segment) or isinstance(segment, Polyline):
            P1, P2 = segment.P1.as_array(), segment.P2.as_array()

        else :
            return None

        P = SegmentXPolygon(P1,P2,self.vertices)
        if P is None :
            return None
        else :
            if type(P) is tuple :
                return Point(P)
            elif type(P) is list:
                return [Point(P[0], Point(P[1]))]
        

    def __contains__(self, other):
        if isinstance(other, Point):
            return PointInPolygon(other.coordinates,self.vertices)         # in polygon
           # return abs(other.V * self.n - self.p.V * self.n) < const.get_eps()  # in plane
        else:
            raise NotImplementedError("")
        
        # elif isinstance(other, Line):
        #     return Point(other.sv) in self and self.parallel(other)
        # elif other.class_level > self.class_level:
        #     return other.in_(self)
   # def contains(self, points, edge=True):
 
    #     P = self.to_2d( points )
    #     polygon = self.to_2d().get_path()
    #     return PointInPolygon2D(P[0],P[1],polygon.vertices[:,:2])

        # radius = 1e-10 if edge else -1e-10
        # return self.to_2d().get_path().contains_points(P[:, :2], radius=radius)
       

    def get_parametric(self, check=True, tolerance=0.001):
        """
        Calculates the parametric equation of the plane that contains 
        the polygon. The output has the form np.array([a, b, c, d]) 
        for:

        .. math::
            a*x + b*y + c*z + d = 0
        
        Inputs:
         check : whether or not the vertices are in the plane with *tolerance*.
         tolerance: float
        
        NOTE that this method automatically stores the solution to avoid calculation
                  more than once.
        """
        if self.parametric is None: 
            
            # Plane calculation
            a, b, c = np.cross(self.vertices[2,:]-self.vertices[0,:],
                               self.vertices[1,:]-self.vertices[0,:])
            d = -np.dot(np.array([a, b, c]), self.vertices[2, :])
            self.parametric = np.array([a, b, c, d])
                
            # Point belonging verification
            if check:
                if self.vertices.shape[0] > 3:
                    if np.min(np.abs(self.vertices[3:,0]*a+
                                     self.vertices[3:,1]*b+
                                     self.vertices[3:,2]*c+
                                     d)) > tolerance:
                        raise ValueError('Polygon not plane: \n'+\
                                         str(self.vertices))
        return self.parametric
        
    def get_path(self):
        """
        :returns: matplotlib.path.Path object for the z=0 projection of 
            this polygon.
        """
        if self.path == None:
            from matplotlib import path
            
            return path.Path(self.vertices[:, :2]) # z=0 projection!
        return self.path

    def get_area(self):
        """
        :returns: The area of the polygon.
        """
        if self.area is None:
            self.area = self.to_2d().get_shapely().area
        return self.area

### Functions to manipulate the polygon
    def getU(self):
        return GetU(self.vertices)

    def matrix(self, points = []):  # to replace GetU

        # if points == None :
        #     points = self.vertices
        # The first vertice is the origin of the local system
        #      dR = points - self[0]

        if type(points) != np.ndarray:
            points = np.array(points)

        if not points.size :
            points = self.vertices

        # Create the matrix from local to global systems
        a = points[1]-points[0]
        a = a/np.linalg.norm(a)                # arbitrary first axis
        n = np.cross(a, points[-1] - points[0])
        n = n/np.linalg.norm(n)                # normal axis
        b = -np.cross(a, n)                    # Orthogonal to the others
        U = np.array([a, b, n])
        U[np.isclose(U, 0.0)] = 0.0
    
        return np.mat(U)

class Shape(Polygon):
### Initialization
    def __init__(self, shape=None,W=None,H=None,A=None,B=None,C=None,D=None, **kwargs):

        points = self.createVertices(shape,W,H,A,B,C,D,**kwargs)
        if type(points) is not np.ndarray :
            points = np.array(points)
        super(Shape, self).__init__(np.array(points))

        # from matplotlib import path
        # self.path = path.Path(self.vertices[:, 1:3]) # x=0 projection!

    def createVertices(self,shape,W,H,A,B,C,D, **kwargs):    
        vertices = np.array([])
        P0 = (0.0,0.0,0.0)
        reference_index = 0

        if not shape : return

        self.input_str = ""
        self.shapeName = shape.lower()
        # print(self.shapeName)
        if self.shapeName == 'regularpolygon' :
            n=3
            R=1
            # print(kwargs)
            for key, value in kwargs.items():
                key_str = key.lower()
                if key_str == 'r':
                    R = value
                elif key_str == 'n':
                    n = value
                elif key_str == 'center':
                            # Input errors
                    if len(value) != 3:
                        raise ValueError('Model.Shape needs x,y,z for a regular polygon center')
                    else :
                        P0 = value
                        # print(P0)

            vertices = regularPolygon(n,R,P0)
            input_str = f"'{shape}',n={n},R={R},center={P0}"

        elif self.shapeName == 'polygon' :

            for key, value in kwargs.items():
                key_str = key.lower()
                if key_str == 'vertices':
                    
                    # value = {'vertices':[(0,0),(1,0),(0.6,0.5)]}

                    if type(value) is list:
                        vertices = np.array(value)
                    elif type(value) is np.ndarray :
                        vertices = value
                    else :
                        raise ValueError('Model.Shape needs a list/np.array for a polygon')

                    # Adapt 2D/3D
                    if vertices.shape[1] == 2:
                         vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))

                    P0 = tuple(vertices[reference_index])
                    input_str = f"'{shape}',{kwargs}"

        else :
            vertices = createShape(shape,W,H,A,B,C,D)
            P0 = tuple(vertices[reference_index])
            input_str = f"'{shape}',{W},{H},{A},{B},{C},{D}"
    
        # self.vertices = vertices    # working vertices
        self.P0 = P0         # reference point
        # the state of the polygon
        self.R = vertices   # initial values of vertices
        self.angles = [0.0,0.0]
        self.__input_str = input_str

        return vertices

    def __str__(self):
        return f"{len(self.vertices)} vertices :\n{self.vertices}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__input_str})"

    def __iter__(self): return iter(self.vertices)
    def __getitem__(self, key): return self.vertices[key]

    # change the object from the current position to a next one 
    # in terms of reference point,together with change in both angles
    # These changes in angle are around the global YZ
    def move(self, reference = None, to = (0,0,0), by = (0.0,0.0)):
        alpha = self.angles[0] + by[0]
        beta  = self.angles[1] + by[1]

        if not reference: P0 = self.P0
        else            : P0 = reference
        
        vertices = change(shape = self.R, reference = P0, to = to, by = (alpha, beta) )
        P0 = tuple(self.vertices[0])

        newPolygon = Shape(shape='Polygon',**{'vertices':vertices})
        newPolygon.P0 = P0
        newPolygon.angles = (alpha, beta)

        return newPolygon
 
    def get_instance(self):
        return self

    def get_argument_dict(self):
        return getArguments(self.shapeName)

'''
    The following are triangles collaped into segments, 
    so they are compatible with shading of matplotlib.
'''
class Segment(Visible):  # segment
### Initialization
     # It is set by P1 and P2

    def __init__(self, *points):
        super().__init__()

        # print(f" parameter : {points}")
        # print(f" type      : {type(points)}")
        # print(f" size      : {len(points)}")

        self._p1 = Point(0,0,0)
        self._p2 = Point(0,0,0)

        if len(points) >= 0:
            self._set_segment(*points)

    def _set_segment(self, *points):
        # print(f" parameter : set_segment{points}")
        # print(f"      type :  {type(points)}") 
        # print(f" size      : {len(points)}")
        
        if len(points) == 1:
            # print(f"a list or tuple of (x,y,z)") 
            xyz = points[0]
            if len(xyz) == 2 :
                self._p1 = self.set_point(xyz[0])
                self._p2 = self.set_point(xyz[1])
            
            elif len(xyz) == 1 :
                self._p1 = Point(0,0,0)
                self._p2 = self.set_point(xyz[0])
            
            else:
                raise ValueError("Line segment() needs 1 or 2 points")
        else :
            # print(f"2 or more points: {points[0]},{points[1]}")
            self._p1 = self.set_point(points[0])
            self._p2 = self.set_point(points[1])

    def set_point(self,x):
        # print(x)
        if isinstance(x,Point):
            p = x
        else :
            p = Point(*x)

        return p

    def __str__(self):
        return f"{self.P1} -> {self.P2}"

    def __repr__(self):
        # type: () -> str
        class_name = type(self).__name__
        return f"{class_name}({self.P1}, {self.P2})"

    def __eq__(self, other):
        if isinstance(other,Segment):
            return  other._p1 == self._p1 and self._p2 == other._p2
        else:
            return False

    def __hash__(self):
        return hash(
        round(self.P1[0],get_sig_figures()),
        round(self.P2[1],get_sig_figures()),
        round(self.P1[0] * self.P2[1] - self.P1[1] * self.P2[0], get_sig_figures()))

    def __contains__(self, other):
        """Checks if a point on the line of segment"""
        if isinstance(other, Segment):
            return None 

        P0 = other
        if isinstance(other,Point):
            P0 = other.coordinates

        return PointInSegment(P0,self.P1.as_array(),self.P2.as_array())


    @property
    def P1(self):
        return self._p1
 
    @property
    def P2(self):
        return self._p2

    @P1.setter
    def P1(self, xyz):
        self._p1 = self.set_point(xyz)

    @P2.setter
    def P2(self, xyz):
        self._p2 = self.set_point(xyz)

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):

        color     = style['color']     if 'color'     in style else self.color
        linewidth = style['linewidth'] if 'linewidth' in style else self.linewidth 
        alpha     = style['alpha']     if 'alpha'     in style else self.alpha
        node      = style['node']      if 'node'      in style else 'invisible'
        nodecolor = style['nodecolor'] if 'nodecolor' in style else 'r'
        marker    = style['marker']    if 'marker'    in style else 'o'

        p = self.midpoint()

        xs = self.P1.x, p.x, self.P2.x 
        ys = self.P1.y, p.y, self.P2.y
        zs = self.P1.z, p.z, self.P2.z

        vertices = list(zip(xs,ys,zs))
     
        line = Poly3DCollection([vertices],edgecolors=color,linewidths=linewidth, alpha=alpha)

        if ax is None:
            ax = self.get_ax()

        ax.add_collection3d(line)

        if node == 'visible':
            ax.scatter(self.P1.x, self.P1.y, self.P1.z, alpha=alpha, c=nodecolor, marker=marker)
            ax.scatter(self.P2.x, self.P2.y, self.P2.z, alpha=alpha, c=nodecolor, marker=marker)

    def get_domain(self):
        points = np.array([(self.P1.x,self.P1.y,self.P1.z), 
                           (self.P2.x,self.P2.y,self.P2.z)])
        return np.array([points.min(axis=0),points.max(axis=0)])

### Functions
    def midpoint(self):
        P = self._p1 + self._p2
        return 0.5*P

    def length(self):
        d = self._p2 - self._p1
        d = np.array([d.x,d.y,d.z]) 
        return np.sqrt(d.dot(d))

    def direction(self):
        v = self.P2 - self.P1
        v = np.array(v.coordinates)
        return UnitVector(v)

    def shortest_distance_to(self, line3d):
        if not isinstance(line3d, type(self)):
            return None
        L1 = self.direction()
        L2 =line3d.direction()
        x,y,z = CreateCoordinates(L1,L2)
        U  = np.vstack((x,y,z))
        U  = np.mat(U)
        R0 = self.P1.as_array()
        P = line3d.P1.as_array()
        R = U@(P - R0)

        return R[2]

    def perpendicular_line_to(self, point3d):
        if not isinstance(point3d, Point):
            return None

        L  = self.direction()
        P  = self.P1.as_array()
        P0 = Point.as_array()
        L,R = NormalToLine(P0,P,L)

        return L,R


class Polyline(Visible):
### Initialization
    def __init__(self, *points):
        super().__init__()

        vertices = self._init_vertices(*points)

        self.vertices = vertices     # a 2D list of shape Nx3, each line for [x,y,z]
        self.lines = []              # a list of Line() created by two Point()

        # create segments
        if len(self.vertices)> 1:
            v1 = self.vertices[0]
            for v2 in self.vertices[1:]:
                line = Segment(v1,v2)
                self.lines.append(line)
                v1 = v2        

    def __str__(self):
        s = f"There are nodes of {len(self.vertices)}.\n"
        s += str(self.vertices[0])
        for point in self.vertices[0:-1]:
            if s:
                s += " -> "
            s += str(point)

        return s

    def __repr__(self):
        return f"self.__class__.__name__({self.vertices})"

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, item):
        """return one of lines"""
        return self.lines[item]

    def __setitem__(self, item, value):
        """set one of Line """
        setattr(self, "lines"[item], value)
        # print(f"item : {item}, value : {value}")

    def __hash__(self):
        return hash(tuple(sorted(self.vertices, key=lambda p: p.x)))

    def _init_vertices(self, *args):
        if len(args) == 0 :
            return []
        
        if len(args) == 1 :
            first = args[0]
            return self.set_points(*first)
        else:
            return self.set_points(*args)

    def set_points(self, *args):
        vertices = []  # np.array([], dtype=object)
        for each in args:
            if type(each) is list or  type(each) is tuple:
                vertices.append(Point(each))

            elif type(each) is np.ndarray :
                vertices.append(Point(each))
    
            elif type(each) is Point :
                vertices.append(each)

        return vertices

    @property
    def P1(self):
        return self.vertices[0]
 
    @property
    def P2(self):
        return self.vertices[-1]

    @P1.setter
    def P1(self, xyz):
        self.vertices[0] = xyz

    @P2.setter
    def P2(self, xyz):
        self.vertices[-1] = xyz

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def get_domain(self):
        """
        :returns: opposite corners of the bounding prism for this object.
        :       ndarray([min], [max])
        """
        # Min/max along the column
        m = len(self.vertices)
        vertices = np.zeros((m,3))
        for i in range(m):
            vertices[i] = self.vertices[i].as_list()

        return np.array([vertices.min(axis=0),  # min (x,y,z)
                         vertices.max(axis=0)]) # max (x,y,z)

    def iplot(self, style, ax,**kwargs):
        # style = {'node':'invisible','edgecolor':'default', ...}
        #                 'visible'               'gradient'
        # for 'gradient' 
        default_colors = ['darkgoldenrod', 'goldenrod','gold','khaki','darkkhahi','olive','oilvedrab','darkolivedrab','beige']
        colors = []

        bColors = 0 
        if style.get('color') == 'gradient' :
            bColors = 1

        if 'colors' in style :
            bColors = 2
            colors = style['colors']

        i=0
        for line in self.lines:

            if bColors == 1 :
                style['color'] = default_colors[i]
                i += 1
                i = i % len(default_colors)

            elif bColors == 2 :
                style['color'] = colors[i]
                i += 1
                i = i % len(colors)

            line.iplot(style, ax,**kwargs)

### Funcions
    def broken_at(self,v):
        if v is None:
            return None
        
        V = v
        if not isinstance(v,Point):
            V = Point(v)

        if len(self.vertices) == 1:
            self.append(V)
            return 2

        elif len(self.vertices) >= 2:
            if self.P1 == V :
                return None
            
            i = 0
            for L in self.lines :
                if V in L:
                    if V == L.P2 :
                        return None 
                    
                    self.insert_at(i+1,V)
                    return i+1
                i += 1

            return None

    def append(self, v):
        v1 = self.vertices[-1]
        v2 = v
        self.vertices.append(v)
        self.lines.append(Segment(v1,v2))

    def insert_at(self,i,v):

        if not isinstance(v,Point):
            v = Point(v)

        if i >= len(self.vertices):
            self.append(v)

        elif i == 0 :
            self.vertices.insert(0,v)
            v0 = self.vertices[0]
            v1 = self.vertices[1]
            self.lines.insert(0, Segment(v0,v1))

        else:
            v0 = self.vertices[i-1]
            v1 = v
            v2 = self.vertices[i]
            
            # print(f" v0's type is {type(v0)}")
            # print(f" v1's type is {type(v1)}")
            # print(f" v2's type is {type(v2)}")

            self.vertices.insert(i,v)

            self.lines.pop(i-1)
            self.lines.insert(i-1, Segment(v0,v1))
            self.lines.insert(i,Segment(v1,v2))

    def intersect(self, poly):
        if isinstance(poly,Polygon):
            return polygon.intersect(self)
        else:
            return None


### help functions for curves connecting two straight segments
def makeArray(u):
    if type(u) is list or type(u) is tuple :
        v = Array(u)
    elif type(u) is Point:
        v = u.as_array()
    else :
        v = u 
    return v

def dividing_S_curve(center1,r1, n, start_angle, end_angle, center2,r2, m, start_angle1, end_angle1):
    X1,Y1 = dividing_arc(center1,r1, n, start_angle1, end_angle1)
    X2,Y2 = dividing_arc(center2,r2, m, start_angle2, end_angle2)

    if not ScalarEqual(X1[-1],X2[0]) and ScalarEqual(Y1[-1],Y2[0]):
        raise ValueError
  
    X = np.hstack(X1,X2[1:])
    Y = np.hstack(Y1,Y2[1:])

def dividing_arc(center,r, n, start_angle, end_angle):
    theta0,dTheta = start_angle, (end_angle - start_angle)/n
    Theta = [theta0 + i*dTheta for i in range(0,n+1)]
    angles = Array(Theta)
    X = center[0] + r * np.cos(angles)
    Y = center[1] + r * np.sin(angles)
    return X,Y

class CurvedConnection(Polyline):
    rmin = 0.5 
    # dimenionless, the blobal setting for minimal radius of curve
    # One can change it to adapt an application in its meaning

    def __init__(self, P1, L1, P2, L2, segments = 10):
        # n - arc is divided by n parts of lines
        self.n  = segments

        # print(f" In __init__() before makeArray() ")
        # print(f" P1 is of {type(P1)}, shape {np.shape(P1)}, {P1} ")
        # print(f" L1 is of {type(L1)}, shape {np.shape(L1)}, {L1} ")
        # print(f" P2 is of {type(P2)}, shape {np.shape(P2)}, {P2} ")
        # print(f" L2 is of {type(L2)}, shape {np.shape(L2)}, {L2} ")

        P1 = makeArray(P1)
        L1 = makeArray(L1)
        P2 = makeArray(P2)
        L2 = makeArray(L2)

        # print(f" In __init__() after before makeArray()")
        # print(f" P1 is of {type(P1)}, shape {np.shape(P1)}, {P1}")
        # print(f" L1 is of {type(L1)}, shape {np.shape(L1)}, {L1}")
        # print(f" P2 is of {type(P2)}, shape {np.shape(P2)}, {P2}")
        # print(f" L2 is of {type(L2)}, shape {np.shape(L2)}, {L2}")

        self.local_coordinate(P1,L1,P2,L2)
        points = self.get_nodes()
        super().__init__(*points)

    def local_coordinate(self,P1,L1,P2,L2):
        P1 = Array(P1)
        L1 = UnitVector(Array(L1))
        P2 = Array(P2)
        L2 = UnitVector(Array(L2))
        x,y,z = CreateCoordinates(L1,L2)
        U = np.vstack((x,y,z))

        # print(f" Input (P1,L1,P2,L2)")
        # print(f"    P1 is {P1}, L1 is {L1} ")
        # print(f"    P2 is {P2}, L2 is {L2} ")
        # print(f"    U = \n{U}")
        # print(f"    U@(P2-P2) = {U@(Array(P2)-Array(P1))}")

        self.r1 = [0,0,0]

        # print(f" R0 is {R0}, R0.T is {R0.T} ")

        R1 =  Array([0,0,0])
        R2 =  Round(U@(P2 - P1)) 
        Direction1 = Round(U@L1)
        Direction2 = Round(U@L2) 

        self.d = np.abs(R2[2])
        R2  = R2 * Array([1,1,0])

        # print(f" In local_coordinate(P1,L1,P2,L2)")
        # print(f" P1 becomes {R1}, L1 becomes {Direction1} ")
        # print(f" P2 becomes {R2}, L2 becomes {Direction2} ")
        # print(f" Their sortest distance is {self.d}")

        self.r2 = R2.tolist() 

        # print(f" P2 projects on XY plane is {self.r2,} of {type(self.r2)}")

        R  = LineXLine(R1,Direction1,R2,Direction2)

        # print(f" Their intersection point is of {type(R)}, shape {np.shape(R)},{R} ")

        if type(R) is str:
            return 'The two lines are skrew'

        self.r  = R

        self.R0 = Array([P1.tolist()]).T
        self.U  = U
        self.L1 = Direction1
        self.L2 = Direction2

    def global_coordinate(self, vertices):  
        # vertices are 2D ones, 
        #          [[x0,y0,0], [x1,y1,0],...]
        r = np.array(vertices).T
        U = np.asmatrix(self.U).I   # inverse matrix
        U = np.asarray(U)

        # print(f" In global_coordinate(vertices)")
        # print(f" U  is of {type(U)} \n{U} ")
        # print(f" r  is of {type(r)},\n{r }")
        # print(f" R0 is of {type(self.R0)},\n{self.R0}")

        # print(f" U is of shape {np.shape(U)}.")
        # print(f" r is of shape {np.shape(r)}.")
        # print(f" r.T is of shape {np.shape(r.T)}.")
        # print(f" R0 is of shape {np.shape(self.R0)}.")

        R = U@r + self.R0      #  (3,N)
        return R.T     # (N,3)

    def get_nodes(self) :
        X,Y = self.get_nodes_2d()
        
        if X is None :
            return None 

        Z = [0] * len(X)
        vertices = list(zip(X,Y,Z))
        points = self.global_coordinate(vertices)

        return points

    def get_nodes_2d(self):
        angle_rad, deg = AngleBetween(self.L1,self.L2)   # 0 < angle < pi 
        self.angle = angle_rad

        if ScalarZero(deg):
            if Dot(L1,L2) < 0 :
                return self.straight_angle()
            else :
                return self.acute_angle()

        elif ScalarEqual(deg, 90.0):
            return self.right_angle()

        elif 90 < deg and deg < 180 :
            return self.obtuse_angle() 

        elif 0 < deg and deg < 90 :
            if Dot(self.L1,self.L2) < 0 :
                return self.reflex_angle()

            elif Dot(self.L1,self.L2) > 0 :
                return self.acute_angle()

        return None, None

    def get_rmin(self):
        return self.__class__.rmin

    def set_rmin(self,value):
        self.__class__.rmin = value

    def acute_angle(self):
        # return a S-shaped connection
        x = self.r[0]
        x2,y2 = self.r2[0], self.r2[1]

        alpha = self.angle
        r_min = self.get_rmin()

        r = 0
        if (x2<=0 and y2>0) or (x2>0 and y2<0):
            w = np.abs(x)
            d = w*np.sin(alpha)
            r = d/(1 - np.cos(alpha))

        if r < r_min :
            r = r_min
    
        if y2 >= 0 :
            c0 = (0,r)
            start_angle, end_angle = -np.pi/2, alpha + np.pi/2

        else :
            c0 = (0,-r)
            start_angle, end_angle = np.pi/2, alpha - np.pi/2 
   
        return dividing_arc(c0, r, self.n, start_angle, end_angle)

    def right_angle(self):
        x = self.r[0]
        x2,y2 = self.r2[0], self.r2[1]
        
        r_min = self.get_rmin()
        angle = np.pi * 0.5

        r = 0
        if x2>=0 and y2>=0 :
            if ScalarEqual(x2,y2) :
                r = 0.5*y2
            elif x2 > y2 :
                r = 0.5*y2
            else :
                r = 0.5*x2

        if r < r_min :
            r = r_min

        c0 = (0,r)
        start_angle, end_angle = -np.pi/2, 0

        return dividing_arc(c0, r, self.n, start_angle, end_angle)

    def obtuse_angle(self):
        # print(f" In obtuse_angle")
        # print(f" r  = {self.r} of {type(self.r)}")
        # print(f" r2 = {self.r2} of {type(self.r2)}")

        x  = self.r[0]
        y2 = self.r2[1]
        alpha = np.pi - self.angle
        r_min = self.get_rmin()

        w = r_min/np.tan(0.5*alpha)

        # print(f" x = {x} of {type(x)}")
        # print(f" w = {w} of {type(w)}")

        if x <= w :  
            # intersection happens abnormal
            r = r_min
        else :
            w = x
            r  = w *np.tan(0.5*alpha)

        if r < r_min :
            r = r_min
        
        if y2 <= 0 :
            c0 = (0,-r)
            start_angle, end_angle = self.angle - np.pi/2, -np.pi/2
        else :
            c0 = (0, r)
            start_angle, end_angle = -np.pi/2, self.angle - np.pi/2

        return dividing_arc(c0, r, self.n, start_angle, end_angle)

    def straight_angle(self):

        y2 = self.r2[1]
        r_min = self.get_rmin()

        r  = 0.5* np.abs(y2)
        if r < r_min :
            # intersection happens abnormal
            r = r_min

        if y2 >= 0 :
            c0 = (0, r)
            start_angle, end_angle = -np.pi/2, np.pi/2
        else :
            c0 = (0, -r)
            start_angle, end_angle = np.pi/2, -np.pi/2

        return dividing_arc(c0, r, self.n, start_angle, end_angle)

    def reflex_angle(self):
        x, y  = self.r[0],self.r[1]
        alpha = self.angle
        r_min = self.get_rmin()

        d_min = r_min*(1 + np.cos(alpha))
        wc = d_min/np.sin(alpha)
        xc = np.abs(x)

        if xc <= wc :
            # intersection happens abnormal
            r = r_min

        else:
            w = xc
            d = w*np.sin(alpha)
            r = d/(1 + np.cos(alpha))

        if y2 > y :
            c0 = ( 0,r)
            start_angle, end_angle = -np.pi/2, alpha + np.pi/2

        else:
            c0 = ( 0, -r )
            start_angle, end_angle =  np.pi/2, alpha + np.pi/2

        return dividing_arc(c0,r, self.n, start_angle, end_angle)

# end of class 

### test functions

def testPolygon1():
    x = [0.5,0.3,0.6,0.9,0.1]
    y = [0.1,0.9,0.3,0.4,0.8]
    z = [0.7,0.3,0.1,0.9,0.6]
    points = list(zip(x,y,z))
    poly = Polygon(points)
    poly.plot()
    poly.show()

def testPolygon2():
    x = [0.5,0.3,0.6,0.9,0.1]
    y = [0.1,0.9,0.3,0.4,0.8]
    z = [0.7,0.3,0.1,0.9,0.6]
    points = list(zip(x,y,z))
    poly = Polygon(points)
    poly.plot()
    poly.show()

def testPolyLine():
    pl = Polyline((0.5,0.3,0.6),(0.1,0.9,0.3),(0.7,0.3,0.9))
    pl.broken_at((0.1,0.9,0.6))
    pl.insert_at(1,(0.3,0.6,0.9))
    pl.plot()
    pl.show()

def testPolyLine():
    pl = Polyline((0.5,0.3,0.6),(0.1,0.9,0.3),(0.7,0.3,0.9))
    pl.broken_at((0.1,0.9,0.6))
    pl.insert_at(1,(0.3,0.6,0.9))
    pl.plot(style = {'colors':['darkorange','orange','gold','wheat'],'node':'visible'})
    pl.show(azim=110, elev=19)

def testAllShapes():
    W,H,A,B,C,D = 2.0,1.5, 1.0, 0.6, 0.2, 0.3
    shape1 = Shape('rectangle',W,H,A,B,C,D)
    shape2 = Shape('triangle' ,W,H,A,B,C,D)
    shape3 = Shape('fourSided',W,H,A,B,C,D)
    shape4 = Shape('fiveSided',W,H,A,B,C,D)
    shape5 = Shape('rectangleWithHole',W,H,A,B,C,D)

    shape1.plot(hideAxes=True)

    shape2 = shape2.move(to = (1,0,0))
    shape3 = shape3.move(to = (2,0,0))
    shape4 = shape4.move(to = (3,0,0))
    shape5 = shape5.move(to = (4,0,0))
    
    line = Polyline((0,1,0.5),(5,1,0.5))

    P2 = shape2.intersect(line)
    P3 = shape3.intersect(line)
    P4 = shape4.intersect(line)
    P5 = shape5.intersect(line)

    # print(P2,P3,P4,P5)
    
    line.broken_at(P2)
    line.broken_at(P3)
    line.broken_at(P4)
    line.broken_at(P5)

    # print(line)

    shape1.add_plot(shape2)
    shape1.add_plot(shape3)
    shape1.add_plot(shape4)
    shape1.add_plot(shape5)
    shape1.add_plot(line,style={'node':'visible','color':'gradient'})
    shape1.show(azim=-88, elev=7)

def ShapeXPolyline():
    W,H,A,B,C,D = 2.0,1.5, 1.0, 0.9, 0.5, 0.5
    shape = Shape('fourSided',W,H,A,B,C,D)

    shape = shape.move(to = (3,0,0))
    line = Polyline((1,1,0.5),(5,1,0.5))

    P = shape.intersect(line)

    line.broken_at(P)

    # print(line)
    shape.plot(hideAxes=True)
    shape.add_plot(line,style={'node':'visible','edgecolor':'gradient'})
    shape.show(azim=144, elev=-38)
 
def draw_logo():

    W,H = 2.0,1.5
    shape = Shape('rectangle',W,H)
    shape = shape.move(to = (2,0,0), by = (45,30))
    
    line = Polyline((0,0,0),(3,1.,2))
    P = shape.intersect(line)
    line.broken_at(P)
    
    shape.plot(hideAxes=True)
    shape.add_plot(line,style={'color':'b','node':'visible','edgecolor':'gradient'})
    shape.show(azim=-20, elev=3)

def main():


    # testPolygon1()
    # testPolygon2()
    # testPolyLine()
    testAllShapes()
    # ShapeXPolyline()
    # draw_logo()

if __name__ == '__main__':
    main()
