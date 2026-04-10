# Functions extracted / slighlty adapted from pyFreeFem toolbox by Olivier Devauchelle
# https://github.com/odevauchelle/pyFreeFem

import numpy as np

def array1D_to_str( a ) :
    return ' '.join( [ str(a) for a in a ] )


def savemesh( mesh, filename ) :
    '''
    Saves mesh in FreeFem++ format in a .msh file.
    '''

    file = open(filename,'w')
    
    mesh_str = ''

    # nv, nt, 0 
    mesh_str += array1D_to_str( [ len( mesh.x), len( mesh.triangles ), 0] ) + '\n'

    # vertices
    for node_index in range( len( mesh.x ) ) :
        mesh_str += array1D_to_str( [  mesh.x[node_index], mesh.y[node_index], 0 ] ) + '\n'

    # triangles
    for tri_index, triangle in enumerate( mesh.triangles ) :
        mesh_str += array1D_to_str( np.array( triangle ) + 1 ) + ' ' + str( 0 ) + '\n'

    file.seek(0)
    file.truncate()
    file.write( mesh_str )
    file.close()

def savevector( vector, filename ) :
    '''
    Saves a vector (array) in FreeFem++ format in a .ffv file.
    '''
    file = open(filename,'w')
    file.seek(0)
    file.truncate()
    file.write(str(len(vector))+'\n')
    file.write( '\n'.join( [ str(value) for value in vector ] ) + '\n' )
    file.close()