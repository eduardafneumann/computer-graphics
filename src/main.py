import glfw
from OpenGL.GL import *

import window 
import key_event 
import program 
import object 
import texture 
import transformation

window = window.create(600, 600)
glfw.set_key_callback(window, key_event.key_event)
program = program.create()

infos = 5*[object.Info()]

infos[0] = object.load('models/caixa/caixa.obj')
infos[0].primitive = 'triangles'
texture.load(0, 'models/caixa/caixa.jpg')

infos[1] = object.load('models/bench.obj')
infos[1].primitive = 'lines'

loc_transformation = glGetUniformLocation(program, "mat_transformation")
glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glfw.show_window(window)

while not glfw.window_should_close(window):

    glfw.poll_events() 
    glClear(GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)

    if key_event.polygonal_mode==True:
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    if key_event.polygonal_mode==False:
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)

    texture.set_parameters(key_event.object, key_event.gl_linear)

    key_event.check_transforamtion_paramenters()
    mat_transform = transformation.get_transformation( infos[key_event.object].center, 
                                                       infos[key_event.object].max_distance, 
                                                       key_event.offsets, 
                                                       key_event.scale, 
                                                       key_event.angles)
    glUniformMatrix4fv(loc_transformation, 1, GL_TRUE, mat_transform)

    object.draw(program, key_event.object, infos)   

    glfw.swap_buffers(window)

glfw.terminate()




























# centers[0] = [0, 0, 0]
# max_distances[0] = 1
# n_vertices[0] = 3

# vertices = np.zeros(4, [("position", np.float32, 2)])
# vertices['position'] = [
#                             ( 0.0, 0.0), # vertice 0
#                             ( 0.0, 0.5), # vertice 1
#                             ( 0.5, 0.0), # vertice 2
#                             ( 1.0, 1.0) # vertice 0
#                         ]

# buffer = glGenBuffers(1)

# glBindBuffer(GL_ARRAY_BUFFER, buffer)
# glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
# stride = vertices.strides[0]
# offset = ctypes.c_void_p(0)
# loc_vertices = glGetAttribLocation(program, "position")
# glEnableVertexAttribArray(loc_vertices)
# glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)
