# Module to handle algebra of 2D vectors, 
# works with numpy array valued coordinates for vectorized operations

import numpy as np
import matplotlib.pyplot as plt

class vec:
    # Class constructor
    def __init__(self,x,y):
        self.x = x
        self.y = y
    # String representation
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"
    
    # plotting 
    def plotArrow(self,shift,color="black"):
        target = self + shift
        plt.annotate("",xy=(self.x,self.y),xytext=(target.x,target.y),
                     arrowprops=dict(arrowstyle="<-",color=color))
        
    # Algebra    
    __array_priority__ = 15. # Required to avoid numpy __mul__ to take over. 
    # u+v
    def __add__(u,v):
        if isinstance(v,vec):
            return vec(u.x+v.x,u.y+v.y)
        else:
            return vec(u.x + v,u.y + v)
    # v+u
    def __radd__(u,v):
        return vec(u.x+v,u.y+v)
    # -u
    def __neg__(self):
        return vec(-self.x,-self.y)
    # u-v
    def __sub__(u,v):
        if isinstance(v,vec):
            return vec(u.x-v.x,u.y-v.y)
        else:
            return vec(u.x-v,u.y-v)
    # v-u
    def __rsub__(u,v):
        return vec(v-u.x,v-u.y)
    # u*lam
    def __mul__(self,lam):
        return vec(lam*self.x,lam*self.y)
    #lam*u
    def __rmul__(self,lam):
        return vec(lam*(self.x),lam*(self.y))
    # u/lam
    def __truediv__(self,lam):
        return vec(self.x/lam,self.y/lam)
    # End class vec. 
    
    
# ============ Other functions =================== #
    
# Dot product
def dot(u,v):
    return u.x*v.x + u.y*v.y
# Euclidean norm
def norm(u):
    return np.sqrt(dot(u,u))


# =========== Unit test ================== #
def test():
    x = np.array([1.,2.])
    y = np.array([3.,4.])
    c = np.array([5.,6.])
    u = vec(x,y)
    print(u+c,c+u,-u,u-c,c-u,u*c,c*u,u/c,dot(u,-u),norm(u))
    