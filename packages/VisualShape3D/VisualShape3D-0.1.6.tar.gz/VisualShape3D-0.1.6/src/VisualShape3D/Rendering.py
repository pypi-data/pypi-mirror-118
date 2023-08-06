import math
import numpy as np
import matplotlib._color_data as mcd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
import matplotlib.pylab as plt
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D
import mpl_toolkits.mplot3d.art3d as art3d

from .Constant import get_eps,get_sig_figures

'''
    Defintion of classes and functions for Rendering and OpenView
'''
### Help functions
'''
https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/
geometry/spherical-coordinates-and-trigonometric-functions
'''
_clamp = lambda value, minv, maxv: max(min(value, maxv), minv)

'''
    The following works for a vector of unit length, v
'''
def cosTheta(v):
    return v.y 

def sinTheta2(v):
    return max(0,1 - cosTheta*cosTheta )

def sinTheta(v):
    return math.sqrt(sinTheta2)

def cosPhi(v):
    sin_theta = sinTheta(v)
    if sin_theta == 0 :
        return 1
    return _clamp(v.x/sin_theta, -1, 1)

def sinPhi(v):
    sin_theta = sinTheta(v)
    if sin_theta == 0 :
        return 1
    return _clamp(v.y/sin_theta, -1, 1)

'''
    conversion of coordinates
'''
def _Cartesian_2_Spherical_Coordinates(v):  # (x,y,z) ->(theta, phi)
    theta = _clamp(math.acos(v.z),-1,1)
    phi = math.atan2(v.y,v.x) 
    if phi < 0:
        phi = phi + 2* math.pi
        '''
            atan2 returns a value in the range [−π:π], 
            We remap the value in the range [0:2π].
        '''
    return theta,phi

def _Spherical_2_Cartesian_Coordinates(theta, phi):
    return Vector(math.cos(phi) * math.sin(theta), 
                  math.sin(phi) * math.sin(theta), 
                  math.cos(theta))


'''
    for product: vector x matrix4
    float m[12] = [ AXx, AYx, AZx, Tx, 
                    AXy, AYy, AZy, Ty, 
                    AXz, AYz, AZz, Tz] 
'''
def _vM(v, AxX, AxY, AxZ, TX,    #             |AxX  AxY  AxZ |    
           AyX, AyY, AyZ, TY,    #  (v0 v1 v2) |AyX  AyY  AyZ | + (TX TY TZ)
           AzX, AzY, AzZ, TZ ):  #             |AzX  AzY  AzZ |    
    return Vector(
                  v.x * AxX + v.y * AyX + v.z * AzX + TX, 
                  v.x * AxY + v.y * AyY + v.z * AzY + TY, 
                  v.x * AxZ + v.y * AyZ + v.z * AzZ + TZ
                  )

class Visible(object):
### Initialization
    _fig = None
    _ax  = None

    """
    It's base class for custom geometries to be plottable in OpenView.
    
    Global methods defined here:
        `plot`
        `get_centroid`
        `copy`
        `save`
        `restore`
    
    Local methods needed in subclasses:
        `get_instance()`      returns the working object to be plotted
        `iplot()`             for plotting specific data 
        `set_view_domain()`   getting its specific view range
        
    """
    def __init__(self):
        self.backup = None
        self.facecolor ='xkcd:beige'
        self.edgecolor ='olive'
        self.color     ='darkgreen'  # for Point/Segement/Line/Polyline
        self.linewidth = 1
        self.linestyles="solid"
        self.alpha     = 1
        self.marker    ='o'

### the framework for plotting

    @staticmethod
    def text3d(ax, xyz, s, zdir="z", size=None, angle=0, usetex=False, **kwargs):
        """
        Plots the string *s* on the axes *ax*, with position *xyz*, size *size*,
        and rotation angle *angle*. *zdir* gives the axis which is to be treated as
        the third dimension. *usetex* is a boolean indicating whether the string
        should be run through a LaTeX subprocess or not.  Any additional keyword
        arguments are forwarded to `.transform_path`.
    
        Note: zdir affects the interpretation of xyz.
        """
        x, y, z = xyz
        if zdir == "y":
            xy1, z1 = (x, z), y
        elif zdir == "x":
            xy1, z1 = (y, z), x
        else:
            xy1, z1 = (x, y), z
    
        text_path = TextPath((0, 0), s, size=size, usetex=usetex)
        trans = Affine2D().rotate(angle).translate(xy1[0], xy1[1])
    
        p1 = PathPatch(trans.transform_path(text_path), **kwargs)
        ax.add_patch(p1)
        art3d.pathpatch_2d_to_3d(p1, z=z1, zdir=zdir)

    def set_ax(self, ax):
        Visible._ax = ax

    def get_ax(self):
        return Visible._ax

    def clear_off(self):
        self.set_ax(None)

    def draw_origin(self):
        ax = self.get_ax()
        if ax is None :
            return

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        zmin, zmax = ax.get_zlim()

        # set the grid
        x = [xmin, xmin, xmin]
        y = [ymin, ymin, ymin]
        z = [0,0,0]   #[zmin, zmin, zmin]
        
        dx = 0.15*(xmax - xmin)
        dy = 0.15*(ymax - ymin)
        dz = 0.15*(zmax - zmin)

        # set the directiona and sizea of three arrows
        u = [dx,0 ,0 ]
        v = [0 ,dy,0 ]
        w = [0 ,0 ,dz]
        
        ax.quiver(x, y, z, u, v, w)

    def show(self, elev= 10.0, azim = 122.0, hideAxes=False, origin = False):
        ax = self.get_ax()

        if  ax is None :
            return
      
        ax.view_init(elev, azim)

        if hideAxes :
            ax.set_axis_off()

        if origin :
            self.draw_origin()

        plt.show()

        return ax

    def add_plot(self, shape, 
                 style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'},
                 hideAxes=False, **kwargs):

        if not isinstance(shape, Visible):
            return None

        return shape.plot(style = style, ax = self.get_ax(), 
            hideAxes=hideAxes,**kwargs)

    def plot(self, style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'}, ax = None, 
                   hideAxes = False, **kwargs):
        """
        3D visualization with the following parameters, 
        Inputs:
         1) style :
              style = {'facecolor','edgecolor','linewidth','alpha','node','nodemarker','nodecolor'}
              It matters differently for line and polygon 
                = (edge color, line width, alpha) for segement, line, polyline and Ray
                = (face color, edge color, alpha) for polygon
                = ( node, node color, node marker) for point
         2) ax: 
              None : to plot in a new figure
              ax :   to plot in the current "ax" (mplot3d.Axes3D) 

         3) hideAxes : hide axes or not

        Outputs:
              plt, ax
              
        Note :
            plt.show() finally lets all plots visible
        """

        bAddingMode = True     # adding more geometries
        if ax is None:
            if self.get_ax() is None : 
                # it is the very first plot of one alone application
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                self.set_ax(ax)
                bAddingMode = False
            else :          # or it plot in the ax of an GUI app
                pass        

        # fetch the instance of a geometry
        # instance = self.__class__(**self.get_seed())
        instance = self.get_instance()

        if instance is None : # in the case for an instance of Visible itself.
            return  

        # print(f" instance = {type(instance)}")
        # print(f" self = {type(self)}")
        # print(f" ax = {type(ax)}")

        # adjust viewport to hold the instance 
        domain = instance.get_domain()

        bound = np.max(domain[1]-domain[0])
        centroid = instance.get_centroid()
        pos = np.vstack((centroid-bound/2, centroid+bound/2))
        pos[0,2] = domain[0,2]
        pos[1,2] = pos[0,2] + bound
        
        # Overlap the existing plots 
        if bAddingMode :
            old_pos = np.array([ax.get_xbound(),
                                ax.get_ybound(),
                                ax.get_zbound()]).T
            pos = np.dstack((pos, old_pos))
            pos = np.array([np.min(pos[0, :, :], axis=1),
                            np.max(pos[1, :, :], axis=1)])


        # Plot instance
        if 'facecolor' not in style : style['facecolor'] = 'default' 
        if 'edgecolor' not in style : style['edgecolor'] = 'default' 
        if 'linewidth' not in style : style['linewidth'] = 'default' 
        if 'alpha'     not in style : style['alpha']     = 'default' 

        if style['facecolor'] == 'default' : style['facecolor'] = self.facecolor
        if style['edgecolor'] == 'default' : style['edgecolor'] = self.edgecolor
        if style['linewidth'] == 'default' : style['linewidth'] = self.linewidth
        if style['alpha']     == 'default' : style['alpha']     = self.alpha    

        instance.iplot(style = style, ax = ax, **kwargs)

        # Axis limits
        ax.set_xlim3d(left  =pos[0,0], right=pos[1,0])
        ax.set_ylim3d(bottom=pos[0,1], top  =pos[1,1])
        ax.set_zlim3d(bottom=pos[0,2], top  =pos[1,2])

        if hideAxes :
            ax.set_axis_off()
            self.draw_origin()

        else :
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        return ax

    def center_plot3d(self):
        """
        Help function for a derived class to manage cascade representation
        of multiple geometries, by keeping the aspect ratio 
        in a 3D representation.
        
        ax : 
            mplot3d.Axes3D for the management.

        return value: None
        """
        ax = self.get_ax()
        if not ax : return

        # Domain
        domain = self.get_domain()
        bound = np.max(domain[1]-domain[0])
        centroid = self.get_centroid()
        pos = np.vstack((centroid-bound/2, centroid+bound/2))

        # Axis limits
        ax.set_xlim3d(left=pos[0,0], right=pos[1,0])
        ax.set_ylim3d(bottom=pos[0,1], top=pos[1,1])
        ax.set_zlim3d(bottom=pos[0,2], top=pos[1,2])

        return Visible.plt

    def get_centroid(self):
        """
        The centroid refers to the center of the circumscribed
        paralellepiped, not its mass center.
        
        it returns a ndarray of (x, y, z).
        
        """
        return self.get_domain().mean(axis=0)

    def get_domain(self) :

        ax = self.get_ax()
        domain = np.array([ax.get_xbound(), 
                           ax.get_ybound(),
                           ax.get_zbound()])
        return domain.T

### root methods for any geometry : `copy`, `save`, `restore`
    def copy(self):
        """
        a help function for deepcopy of its entire instance.
        """
        import copy
        return self.__class__(**copy.deepcopy(self.get_seed()))
        
    def save(self):
        """
        It saves a deepcopy of the current state of the instance. 
        restore() will return this copy.
        """
        self.backup = self.copy()
        
    def restore(self):
        """
        it returns last saved version of this object.
        """
        if self.backup is not None:
            return self.backup
        else:
            raise ValueError('No backup previously saved.')

class OpenView(Visible):
### Initialization
    def __init__(self, ax=None):
        super().__init__()
        if self.get_ax() is not None:
            self.clear_off()

        if ax is None :
            # it is the very first plot of one alone application
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
        self.set_ax(ax)

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):
        if ax is None:
            ax = self.get_ax()

        R0 = Origin()
        R0.iplot(style, ax, **kwargs)

    def get_domain(self) :

        ax = self.get_ax()
        domain = np.array([ax.get_xbound(), 
                           ax.get_ybound(),
                           ax.get_zbound()])
        return domain.T

### Functions
    def show(self, elev= 10.0, azim = 122.0, hideAxes=False, origin = False):
        ax = self.get_ax()

        if  ax is None :
            return
      
        ax.view_init(elev, azim)

        if hideAxes :
            ax.set_axis_off()

        if origin :
            R0 = Origin()
            self.add_plot(R0)

        plt.show()

        return ax


class Origin(Visible):
    def __init__(self):
        super().__init__()    
### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):
        if ax is None:
            ax = self.get_ax()

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        zmin, zmax = ax.get_zlim()

        # set the grid
        x = [xmin, xmin, xmin]
        y = [ymin, ymin, ymin]
        z = [zmin, zmin, zmin]
        
        dx = 0.15*(xmax - xmin)
        dy = 0.15*(ymax - ymin)
        dz = 0.15*(zmax - zmin)

        # set the directiona and sizea of three arrows
        u = [dx,0 ,0 ]
        v = [0 ,dy,0 ]
        w = [0 ,0 ,dz]
        
        ax.quiver(x, y, z, u, v, w)
        
        # Manually label the axes
        
        Visible.text3d(ax, (xmin + dx, ymin, zmin), "X-axis", zdir="z", size=.1, usetex=False,
               ec="none", fc="k", **kwargs)
        
        Visible.text3d(ax, (xmin, ymin + dy ,zmin), "Y-axis", zdir="z", size=.1, usetex=False,
               angle=np.pi / 2, ec="none", fc="k",**kwargs)
        
        Visible.text3d(ax, (xmin, ymin, zmin + dz), "Z-axis", zdir="x", size=.1, usetex=False,
               angle=np.pi / 2, ec="none", fc="k", **kwargs)


### Classes for Point, Segment, Line, PolyLine and CurvedConnection, 
#  PolyLine is meant to solar ray tracking.

class Point(Visible):
### Initilization
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.x, self.y, self.z = 0, 0, 0

        self.set_point(*args, **kwargs)
        self.label = None

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return "Point({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        # return self.x == other.x and self.y == other.y and self.z == other.z
        return isinstance(other, type(self)) and self.equal_to(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, c):
        return Point(c * self.x, c * self.y, c * self.z)

    def __mul__(self, c):
        return self.__rmul__(c)

    def __getitem__(self, item):
        """return one of x,y,z"""
        return (self.x, self.y, self.z)[item]

    def __setitem__(self, item, value):
        """set one of x,y,z of a Point"""
        setattr(self, "xyz"[item], value)

    @property
    def coordinates(self):
        return (self.x, self.y, self.z)

    @coordinates.setter
    def coordinates(self, *args):
        self.set_point(*args)

    def set_point(self,*args, **kwargs):
        # print(f" len(args) = {len(args)}")
        # print(f" kwargs = {kwargs}")
        # if len(args) == 3 :
        #     for key, value in kwargs.items():
        #         if key == 'x':
        #             self.x = value
        #         if key == 'y':
        #             self.y = value
        #         if key == 'z':
        #             self.z = value
        #     return

        if len(args) == 1:
            first_input= args[0]
            if type(first_input) is Point :
               P = first_input
               self.x, self.y, self.z = P.x, P.y, P.z

            else :
                coords = first_input
                if len(coords)==3 :
                    self.x, self.y, self.z = coords[0],coords[1],coords[2]
                
                elif len(coords)==2 :
                    self.x, self.y, self.z = coords[0],coords[1],0.0
                
                else:
                    raise ValueError("Point() needs 2 or 3 values")
        
        else :
            # 2 or 3 scalar numbers
            self.x = args[0]
            self.y = args[1]
            if len(args) == 3 :
                self.z = args[2]
            else :
                self.z = 0

    def equal_to(self, that):
        return self.distance_to(that) < get_eps()

    def distance_to(self, that):
        dx = self.x - that.x
        dy = self.y - that.y
        dz = self.z - that.z
        sqrDist = dx * dx + dy * dy  + dz * dz
        return np.sqrt(sqrDist)
        
    def move(self, offset):
        if isinstance(offset,list) or isinstance(offset,tuple) or isinstance(offset,np.array) :
            self.x += offset[0]
            self.y += offset[1]
            self.z += offset[2]
            return Point(self.x,self.y,self.z)
        else:
            raise NotImplementedError("move(offset) : offset must be (dx,dy,dz)")

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):
        # defaul setting
        color  = style['color']  if 'color' in style else self.color  
        marker = style['marker'] if 'marker'in style else self.marker  
        alpha  = style['alpha']  if 'alpha' in style else self.alpha 
        label  = style['label']  if 'label' in style else self.label  

        if ax is None:
            ax = self.get_ax()

        ax.scatter(self.x, self.y, self.z, alpha=alpha, c=color, marker=marker)

        if label is not None :
            dz = 0.1
            text = f"{self.x, self.y, self.z}"

            Visible.text3d(ax, (self.x+dz, self.y, self.z + dz), text, zdir="y", size = 0.2, usetex=False,
                                angle=0, ec="none", fc="k", **kwargs)
            # ax.text(self.x, self.y, self.z, text, zdir=(1, 1, 1))

    def get_domain(self) :
        width = 2

        xlower = self.x - 0.5*width
        xupper = self.x + 0.5*width

        ylower = self.y - 0.5*width
        yupper = self.y + 0.5*width

        zlower = self.z - 0.5*width
        zupper = self.z + 0.5*width


        domain = np.array([(xlower,xupper ), 
                           (ylower,yupper ),
                           (zlower,zupper )])

        return domain.T

### Functions
    def as_list(self):
        return [self.x,self.y,self.z]

    def as_tuple(self):
        return (self.x,self.y,self.z)

    def as_dict(self):
        return {"x":self.x, "y":self.y, "z":self.z}

    def as_array(self):
        return np.array([self.x,self.y,self.z])

### More Functions
    def transform_row_major(self, M) : #  P *M  ( 4x4 )
        x = self.x * M[0][0] + self.y * M[1][0] + self.z * M[2][0] + M[3][0]
        y = self.x * M[0][1] + self.y * M[1][1] + self.z * M[2][1] + M[3][1]
        z = self.x * M[0][2] + self.y * M[1][2] + self.z * M[2][2] + M[3][2]
        w = self.x * M[0][3] + self.y * M[1][3] + self.z * M[2][3] + M[3][3] 
        if w != 1 and w != 0 :
            x = self.x / w 
            y = self.y / w 
            z = self.z / w 
        return Point(x,y,z)

    def transform_column_major(self, M) : #  M * P,  M is 4x4
        x = self.x * M[0][0] + self.y * M[0][1] + self.z * M[0][2] + M[0][3]
        y = self.x * M[1][0] + self.y * M[1][1] + self.z * M[1][2] + M[1][3]
        z = self.x * M[2][0] + self.y * M[2][1] + self.z * M[2][2] + M[2][3]
        w = self.x * M[3][0] + self.y * M[3][1] + self.z * M[3][2] + M[3][3] 
        if w != 1 and w != 0 :
            x = self.x / w 
            y = self.y / w 
            z = self.z / w 
        return Point(x,y,z)

    def translate(self, T):
        if type(T) is Point :
            x = self.x + T.x
            y = self.y + T.y
            z = self.z + T.z
        else : # list/tupe/np.array
            if type(T) is int or type(T) is float:  # scalar constant
                x = self.x + T
                y = self.y + T
                z = self.z + T
            elif len(T) == 3 :
                x = self.x + T[0]
                y = self.y + T[1]
                z = self.z + T[2]

            else :
                raise ValueError("Point() needs 1 or 3 values for translation.")
        return Point(x,y,z)

    def rotate_row_major(self, M):
        x = self.x * M[0][0] + self.y * M[1][0] + self.z * M[2][0]
        y = self.x * M[0][1] + self.y * M[1][1] + self.z * M[2][1]
        z = self.x * M[0][2] + self.y * M[1][2] + self.z * M[2][2]
        return Point3D(x,y,z)

class Vector(Visible):
### Initialization
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.x, self.y, self.z = 0.0, 0.0, 0.0
        self._set_vector(*args, **kwargs)

    def _set_vector(self, *args, **kwargs):

        # if len(kwargs) > 0 :
        #     for key, value in kwargs.items():
        #         if key == 'x':
        #             self.x = value
        #         if key == 'y':
        #             self.y = value
        #         if key == 'z':
        #             self.z = value
        #     return


        if len(args) == 1:
            
            first_input= args[0]
            if type(first_input) is Vector :
               V = first_input
               self.x, self.y, self.z = V.x, V.y, V.z

            elif type(first_input) is Point :
               P = first_input
               self.x, self.y, self.z = P.x, P.y, P.z

            else :
                coords = first_input
                if len(coords)==3 :
                    self.x, self.y, self.z = coords[0], coords[1], coords[2]
                
                elif len(coords)==2 :
                    self.x, self.y, self.z = coords[0], coords[1], 0.0
                
                else:
                    raise ValueError("Vector() needs 2 or 3 values")
        
        else :

            # 2 or 3 scalar numbers
            self.x,self.y = args[0],args[1]

            if len(args) == 3 :
                self.z = args[2]
            else :
                self.z = 0

    def __str__(self):
        return f"A vector in the direction of {self.x, self.y, self.z}."

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}({self.x, self.y, self.z})"

    def __eq__(self, v):
        # return self.x == v.x and self.y == v.y and self.z == v.z
        return isinstance(v, type(self)) and self.equal_to(v)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    def __rmul__(self, c):
        if type(c) is int or type(c) is float:
            return Vector(c * self.x, c * self.y, c * self.z)

        elif type(c) is Vector :
            return self.cross(c)

        elif type(c) is Matrix3 :
            M = c.get_m()
            return self.rotate_row_major(M)
        
        elif type(c) is Matrix4 :
            M = c.get_m()
            return self.rotate_row_major(M) + Vector(M[0][3],M[1][3],M[2][3])
        else :
            None

    def __mul__(self, c):
        return self.__rmul__(c)

### type conversion
    def as_list(self):
        return [self.x,self.y,self.z]

    def as_tuple(self):
        return (self.x,self.y,self.z)

    def as_dict(self):
        return {"x":self.x, "y":self.y, "z":self.z}

    def as_array(self):
        return np.array([self.x,self.y,self.z])

### functions

    def length(self):
        x,y,z = self.x, self.y, self.z
        return np.sqrt(x * x + y * y + z * z)

    def normalize(self):
        L = self.length()
        x,y,z = self.x, self.y, self.z
        if L > 0 :
            inv_L = 1/L
            x, y, z = x/inv_L,y/inv_L,z/inv_L
        return Vector(x,y,z)

    def equal_to(self, v):
        return self.distance_to(v) < get_eps()

    def distance_to(self, v):
        dx = self.x - v.x
        dy = self.y - v.y
        dz = self.z - v.z
        return np.sqrt(dx * dx + dy * dy + dz * dz)

### operations
    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        x,y,z = self.x, self.y, self.z
        return Vector(y * v.z - z * v.y, z * v.x - x * v.z, x * v.y - y * v.x)

    def rotate_row_major(self,M):   #  vector * M
        x = self.x * M[0][0] + self.y * M[1][0] + self.z * M[2][0] 
        y = self.x * M[0][1] + self.y * M[1][1] + self.z * M[2][1] 
        z = self.x * M[0][2] + self.y * M[1][2] + self.z * M[2][2] 
        return Vector(x,y,z)

    def rotate_column_major(self,M):  # M * vector
        x = self.x * M[0][0] + self.y * M[0][1] + self.z * M[0][2] 
        y = self.x * M[1][0] + self.y * M[1][1] + self.z * M[1][2] 
        z = self.x * M[2][0] + self.y * M[2][1] + self.z * M[2][2] 
        return Vector(x,y,z)

class Matrix3(Visible):
    '''
      https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry/matrices
    '''
    def __init__(self, *args):
        super().__init__()
        # initialize with the identity matrix of 4x4 
        self.m = np.array([[1,0,0],[0,1,0],[0,0,1]])
        if len(args) > 0 :
            self.set_matrix(*args)

    def __str__(self):
        return f"matrix is \n{self.m[0,:]}\n{self.m[1,:]}\n{self.m[2,:]}"

    def __repr__(self):
        name = self.__class__.__name__
        return f"{name}({self.m})"

    def __rmul__(self, c):
        if type(c) is int or type(c) is float:
            return Matrix3(c * self.m)

        elif type(c) is Vector :
            return Vector(self.m @ c.as_array())
            # transpose m to meet with the need of _vM()
            # return _vM(c,m[0][0], m[1][0], m[2][0],0,
            #              m[0][1], m[1][1], m[2][1],0,
            #              m[0][2], m[1][2], m[2][2],0)

        elif type(c) is np.ndarray and len(c) >= 3 :
            v = c[0:3]
            return Vector(self.m @ v)
            # transpose m to meet with the need of _vM()
            # return _vM(v,m[0][0], m[1][0], m[2][0], 0,
            #              m[0][1], m[1][1], m[2][1], 0,
            #              m[0][2], m[1][2], m[2][2], 0 )

        elif type(c) is type(self):
            A = c.get_m()
            B = self.get_m()
            return self.__class__(A @ B)

    def __mul__(self, c):
        return self.__rmul__(c)

    def set_matrix(self, *args):
        import copy
        if len(args) == 1:   #   Matrix(M)
            
            first_input= args[0]
            if type(first_input) is self.__class__ :
                self.m = copy.deepcopy(first_input.m)

            else : #  Matrix([[1,2,3],[5,6,7],[9,10,11]])  
                self.set_m(*first_input)
        
        else :  #  Matrix([1,2,3],[5,6,7],[9,10,11])
            self.set_m(*args)

    def set_m(self,*args):
        m = len(args) 
        for i in range(m) :
            n = len(args[i])
            for j in range(n):
                x = args[i][j]
                if type(x) is not str:
                    self.m[i,j] = x 

    def get_m(self):
        m,n = np.shape(self.m)
        M = np.eye(m)
        for i in range(m):
            for j in range(m):
                M[i][j] = self.m[i][j]
        return M

    def transpose(self):
        return np.transpose(self.m)

    def inverse(self):
        return np.linalg.inv(self.m)

class Matrix4(Matrix3):
    '''
      https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry/matrices
    '''
    def __init__(self, *args):
        super().__init__()
        # initialize with the identity matrix of 4x4 
        self.m = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
        self.set_matrix(*args)

    def set_matrix(self, *args):
        import copy
        if len(args) == 1:   #   args = (M,) ( Matrix(M) )

            # What does it mean by M ?
            first_input= args[0]
            if type(first_input) is Matrix4 :
                self.m = copy.deepcopy(first_input.m)

            elif type(first_input) is Matrix3 :
                self.m[0:3,0:3] = first_input.get_m()

            else : #  Matrix([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])  
                self.set_m(*first_input)
        
        else :  #  Matrix([1,2,3],[4,5,6],[7,8,9],[10,11,12])
            self.set_m(*args)

    def add_translation(self, Tx=0,Ty=0,Tz=0):
        self.m[0][3] = Tx
        self.m[1][3] = Ty
        self.m[2][3] = Tz
        return self


    def __str__(self):
        return f"the resultant matrix is \n{self.m[0,:]}\n{self.m[1,:]}\n{self.m[2,:]}\n{self.m[3,:]}"

    def __repr__(self):
        name = self.__class__.name
        return f"{name}({self.m})"

    def __rmul__(self, c):
        m = self.m
        if type(c) is int or type(c) is float:
            return Matrix4(c * m)

        elif type(c) is Vector :
            return _vM(c,m[0][0], m[1][0], m[2][0], m[0][3],
                         m[0][1], m[1][1], m[2][1], m[1][3],
                         m[0][2], m[1][2], m[2][2], m[2][3] )

        elif type(c) is np.ndarray and len(c) >= 3 :
            v = Vector(c[0],c[1],c[2])
            return _vM(v,m[0][0], m[1][0], m[2][0], m[0][3],
                         m[0][1], m[1][1], m[2][1], m[1][3],
                         m[0][2], m[1][2], m[2][2], m[2][3] )

# class Line(Visible):
#     ''' 
#         It is the infinite Segment.
#         A collapsed triangle for the purpose of line shading in matplotlib.
#     '''
# ### Initialization
#     def __init__(self, P, L):
        
#         if type(P) is not Point :
#             P = Point(P)

#         if type(L) is not Point:
#             L = Point(L)

#         L = UnitVector(L.as_array())
#         P = P.as_array()

#         self.P = Point(P)
#         self.L = Vector(L)

#     def __str__(self):
#         return f"A line across {self.P} in the direction of {self.L}."

#     def __repr__(self):
#         class_name = type(self).__name__
#         return f"{class_name}({self.P,self.L})"

### iplot()
    def get_instance(self): return self 

    def iplot(self, style, ax, **kwargs):

        color     = style['color']     if 'color'     in style else self.color
        linewidth = style['linewidth'] if 'linewidth' in style else self.linewidth 
        alpha     = style['alpha']     if 'alpha'     in style else self.alpha
        node      = style['node']      if 'node'      in style else 'invisible'
        nodecolor = style['nodecolor'] if 'nodecolor' in style else 'r'
        marker    = style['marker']    if 'marker'    in style else 'o'

        vertices = self.get_vertices(ax)
     
        line = Poly3DCollection([vertices],edgecolors=color,linewidths=linewidth, alpha=alpha)

        ax.add_collection3d(line)

        if node == 'visible':
            ax.scatter(self.P.x, self.P.y, self.P.z, alpha=alpha, c=nodecolor, marker=marker)

    def get_vertices(self,ax):
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        zmin, zmax = ax.get_zlim()

        x1,x2 = xmin, xmax
        y1,y2 = ymin, ymax
        z1,z2 = zmin, zmax

        perpendicular_to_x = self.L.x == 0
        perpendicular_to_y = self.L.y == 0
        perpendicular_to_z = self.L.z == 0
        if perpendicular_to_x :
            x1, x2 = self.P.x, self.P.x

        if perpendicular_to_y :
            y1, y2 = self.P.y, self.P.y

        if perpendicular_to_z :
            z1, z2 = self.P.z, self.P.z

        parallel_to_x = perpendicular_to_y and perpendicular_to_z
        parallel_to_y = perpendicular_to_x and perpendicular_to_z
        parallel_to_z = perpendicular_to_x and perpendicular_to_y
        
        if parallel_to_x or parallel_to_y or parallel_to_z :
            pass
        else :
            if perpendicular_to_x or perpendicular_to_y: 
                # intersection with floor and ceiling planes
                floor_R0 = (0,0,zmin)
                floor_n  = (0,0,1)
                R1 = LineXPlane(self.P.as_array(), self.L.as_array, floor_R0, floor_n)
                ceil_R0 = (0,0,zmax)
                ceil_n  = (0,0,-1)
                R2 = LineXPlane(self.P.as_array(), self.L.as_array, ceil_R0, ceil__n) 

            elif perpendicular_to_z : 
                # intersection with floor and ceiling planes
                front_R0 = (0,ymin,0)
                front_n  = (0,1,0)
                R1 = LineXPlane(self.P.as_array(), self.L.as_array, front_R0, front_n)
                rear_R0 = (0,ymax,0)
                rear_n  = (0,-1,0)
                R2 = LineXPlane(self.P.as_array(), self.L.as_array, rear_R0, rear_n)   

            else :
                floor_R0 = (0,0,zmin)
                floor_n  = (0,0,1)
                R1 = LineXPlane(self.P.as_array(), self.L.as_array, floor_R0, floor_n)
                ceil_R0 = (0,0,zmax)
                ceil_n  = (0,0,-1)
                R2 = LineXPlane(self.P.as_array(), self.L.as_array, ceil_R0, ceil__n) 

        x1,y1,z1 = R1 
        x2,y2,z2 = R2
        x3,y3,z3 = tuple(0.5*(u+v) for u, v in zip(R1, R2))

        xs = x1, x2, x3
        ys = y1, y2, y3
        zs = z1, z2, z3
        
        vertices = list(zip(xs, ys, zs))

        return vertices


### Test functions
def test_matrix4():

    m1 =  Matrix4([1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16])
    print(m1)

    m2 =  Matrix4([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
    print(m2)
    
    m3 =  Matrix4(m2)
    print(m3)

    m4 =  Matrix4([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
    print(m4)

    m5 =  Matrix4([[1,2,3],[5,6],[9]])
    print(m5)

    m6 =  Matrix4([[1,2,3],[5,6],[9]])
    print(m6)

    b = 'x'
    m7 =  Matrix4([[b,1,2,3],[5,b,6],[b,b,b,9]])
    print(m7)

def test_matrix3():

    m1 =  Matrix3([1,2,3],[5,6,7],[9,10,11])
    print(m1)

    m2 =  Matrix3([[1,2,3],[5,6,7],[9,10,11]])
    print(m2)
    
    m3 =  Matrix3(m2)
    print(m3)

    m4 =  Matrix3([[1,2,3],[5,6,7]])
    print(m4)

    m5 =  Matrix3([[1,2],[5]])
    print(m5)

    b = 'x'
    m7 =  Matrix3([[b,2,3],[5,b,6]])
    print(m7)

def test_vector():
    v = Vector(1,2,3)
    print(v)

    v = Vector([4,5,6])
    print(v)

    v = Vector((1,2,3))
    print(v)

    print(Vector(v))

    v = Vector(x=3,y=5,z=9)
    print(v)

def test_matrix3_x_vector():
    m = Matrix3([1,2,3],[5,6,7],[9,10,11])
    v1 = Vector(1,2,3)
    print(m)
    # print(m.transpose())
    print(v1)
    v2 = m * v1
    print(v2)
    v3 = v1 * m
    print(v3)

    m2 = m * m 
    print(m2)

def test_matrix4_X_vector():
    m1 = Matrix3([1,2,3],[5,6,7],[9,10,11])
    v1 = Vector(1,2,3)
    print(m1)
    print(v1)
    m2 = Matrix4(m1)
    print(m2)
    v2 = m2 * v1
    print(v2)

    m2.add_translation(1,2,3)
    v3 = m2 * v1
    print(v3)

def test_slicing():
    m1 = np.eye(4)
    print(m1)
    print(m1[0:3,0:3])
    m2 = Matrix3([1,2,3],[4,5,6],[7,8,9])
    print(m2)
    m1[0:3,0:3] = m2.get_m()
    print(m1)

    args = ([1,2,3],[4,5,6],[7,8,9],[10,11,12])
    shape = np.shape(args)

    print( shape == (4,3))

def testPoints1():
    P = Point(0.5,0.5,0.5)
    ax = P.plot(style={'color':'r','marker':'o','alpha':0.5})
    P = Point(0.5,0.7,0.5)
    P.plot(ax=ax)
    P.show()

def testPoints2():
    P = Point(0.5,0.5,0.5)
    ax = P.plot(style={'color':'r','marker':'o','alpha':0.5})
    print(P.ax)
    P1 = Point(0.5,0.7,0.5)
    P.add_plot(P1)
    P.show()

def testPoints3():
    P = Point(0.5,0.5)
    P[2]=0.6
    print(P[0],P[1],P[2])

def testSegment():
    P1 = Point(0.2,0.1,0.1)
    P2 = Point(0.8,0.5,0.8)
    L  = Segment(P1,P2)
    print(L)
    L.plot()
    L.show()

def testSegment2():
    P1 = Point(0.2,0.1,0.1)
    P2 = Point(0.8,0.5,0.8)
    L  = Segment(P1,P2)
    L.plot(style={'color':'r'})
    L.show()

# def testRay1():
#     P0 = Point(0.2,0.1,0.1)
#     L  = [0.8,0.5,0.8]
#     ray  = Ray(P0,L)
#     ax   = ray.plot()
#     # print(ax)
#     ray.show()

# def testRay2():
#     P0 = Point(0.2,0.1,0.1)
#     L  = [0.8,0.5,0.8]
#     ray = Ray(P0,L)
#     ax = ray.plot()
#     ray.show()


def main():
    test_matrix4_X_vector()
    # testPoints1()
    # testPoints2()
    # testPoints3()
    # testSegment()
    # testLine2()
    # testRay1()
    # testRay2()

if __name__ == '__main__':
    main()