import numpy as np
import math

def get_transformation(center, max_distance, offsets, scale, angles):

    mat_transform  = np.array([     [1.0, 0.0, 0.0, 0.0], 
                                    [0.0, 1.0, 0.0, 0.0], 
                                    [0.0, 0.0, 1.0, 0.0], 
                                    [0.0, 0.0, 0.0, 1.0]
                              ], np.float32)

      # Center the object in window.
    mat_center      = np.array([    [1.0, 0.0, 0.0, -center[0]], 
                                    [0.0, 1.0, 0.0, -center[1]], 
                                    [0.0, 0.0, 1.0, -center[2]], 
                                    [0.0, 0.0, 0.0,        1.0]       
                               ], np.float32)
    
    # Scale the object to the maximum size while it still can be rotated 
    # in all directions and still fitting the screen.
    size = 1/max_distance
    mat_fit_screen  = np.array([    [size,    0.0,    0.0, 0.0], 
                                    [   0.0, size,    0.0, 0.0], 
                                    [   0.0,    0.0, size, 0.0], 
                                    [   0.0,    0.0,    0.0, 1.0]
                               ], np.float32)  

    mat_translation = np.array([    [1.0, 0.0, 0.0, offsets[0]], 
                                    [0.0, 1.0, 0.0, offsets[1]], 
                                    [0.0, 0.0, 1.0, 0.0], 
                                    [0.0, 0.0, 0.0,  1.0]
                               ], np.float32)   

    mat_scale       = np.array([    [scale, 0.0, 0.0, 0.0], 
                                    [0.0, scale, 0.0, 0.0], 
                                    [0.0, 0.0, scale, 0.0], 
                                    [0.0, 0.0, 0.0, 1.0]
                               ], np.float32)   
    
    cx = math.cos(angles[0])
    sx = math.sin(angles[0])
    mat_rotation_x = np.array([     [1.0, 0.0, 0.0, 0.0], 
                                    [0.0,  cx, -sx, 0.0], 
                                    [0.0,  sx,  cx, 0.0], 
                                    [0.0, 0.0, 0.0, 1.0]
                              ], np.float32)

    cy = math.cos(angles[1])
    sy = math.sin(angles[1])
    mat_rotation_y = np.array([     [ cy,  0.0,  sy, 0.0], 
                                    [0.0,  1.0, 0.0, 0.0], 
                                    [-sy,  0.0,  cy, 0.0], 
                                    [0.0,  0.0, 0.0, 1.0]
                              ], np.float32)

    cz = math.cos(angles[2])
    sz = math.sin(angles[2])
    mat_rotation_z = np.array([     [ cz,  -sz, 0.0, 0.0], 
                                    [ sz,   cz, 0.0, 0.0], 
                                    [0.0,  0.0, 1.0, 0.0], 
                                    [0.0,  0.0, 0.0, 1.0]
                              ], np.float32)
    
    mat_transform = np.matmul( mat_center,      mat_transform)
    mat_transform = np.matmul( mat_fit_screen,  mat_transform)
    mat_transform = np.matmul( mat_scale,       mat_transform)
    mat_transform = np.matmul( mat_rotation_x,  mat_transform)
    mat_transform = np.matmul( mat_rotation_y,  mat_transform)
    mat_transform = np.matmul( mat_rotation_z,  mat_transform)
    mat_transform = np.matmul( mat_translation, mat_transform)

    return mat_transform.reshape(1,16)