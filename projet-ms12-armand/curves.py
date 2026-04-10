# Module to handle convex parametric curves. 
import numpy as np
import matplotlib.pyplot as plt

# To handle algebra of 2D vectors. 
from vec2d import * 



# Note : The parametrization 
# must be with the direct orientation 
class curve:
    #Class constructor.
    def __init__(self,x,y,dx,dy,ddx,ddy,a,b):
        self.x=x
        self.y=y
        self.dx=dx
        self.dy=dy
        self.ddx=ddx
        self.ddy=ddy
        self.a = a
        self.b = b
    
    # Plot the curve
    def plot(self,nsamples=1000):
        t = np.linspace(self.a,self.b,nsamples)
        plt.plot(self.x(t),self.y(t))
    
    # Plot T(t0) and N(t0) (tangent and normal)
    def plotTN(self,t0):
        self.M(t0).plotArrow(self.T(t0),color="red")
        self.M(t0).plotArrow(self.N(t0),color="blue")
        self.M(t0).plotArrow(self.Cvec(t0),color="green")
    
    # M(t) : point on the curve for parameter t. 
    def M(self,t):
        return vec(self.x(t),self.y(t))
    # dM/dt 
    def dM(self,t):
        return vec(self.dx(t),self.dy(t))
    # d^2M / dt^2
    def d2M(self,t):
        return vec(self.ddx(t),self.ddy(t))
    # tangent vector
    def T(self,t):
        return self.dM(t)/norm(self.dM(t))
    # Normal vector
    def N(self,t):
        Tt = self.T(t)
        return vec(Tt.y,-Tt.x)
    # curvature vector
    def Cvec(self,t):
        return (self.d2M(t) - self.T(t)*dot(self.T(t),self.d2M(t)))/norm(self.dM(t))**2
    # curvature
    def C(self,t):
        return norm(self.Cvec(t))
    

# Some special curves


def ellipse(a,b):
    def x(t):
        return a*np.cos(t)
    def dx(t):
        return -a*np.sin(t)
    def d2x(t):
        return -a*np.cos(t)

    def y(t):
        return b*np.sin(t)
    def dy(t):
        return b*np.cos(t)
    def d2y(t):
        return -b*np.sin(t) 
    return curve(x,y,dx,dy,d2x,d2y,0,2*np.pi)

def circle(r=1):
    return ellipse(r,r)

def roundedPolygon(nsides):
    n = nsides-1
    def x(t):
        return np.cos(t)-1/n**2*np.cos(n*t)
    def dx(t):
        return -np.sin(t) + 1/n*np.sin(n*t)
    def d2x(t):
        return -np.cos(t) + np.cos(n*t)
    
    def y(t):
        return np.sin(t) + 1/n**2*np.sin(n*t)
    def dy(t):
        return np.cos(t) + 1/n*np.cos(n*t)
    def d2y(t):
        return -np.sin(t) - np.sin(n*t)
    return curve(x,y,dx,dy,d2x,d2y,0,2*np.pi)

def roundedTriangle():
    return roundedPolygon(3)

def roundedSquare():
    return roundedPolygon(4)


# E = roundedPolygon(5)
# E.plot()
# plt.axis("equal")
# plt.show()


