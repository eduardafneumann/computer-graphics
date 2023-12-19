import glfw
from OpenGL.GL import *

import window 
import key_event 
import program 
import texture 
import transformation
from ilumination import Ilumination
import constants
from void import Void
from scenario import Scenario

window = window.create(constants.height, constants.width)
glfw.set_key_callback(window, key_event.key_event)
glfw.set_cursor_pos_callback(window, key_event.mouse_event)

program = program.create()

ilum = Ilumination(program)
void = Void(program, ilum, key_event)
scenario = Scenario(program, ilum, key_event)

void.load()
scenario.load()

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)
glfw.show_window(window)

# Main loop.
while not glfw.window_should_close(window):

    glfw.poll_events() 
    glClear(GL_DEPTH_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT) 
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Activate or deactivate texture.
    if key_event.polygonal_mode==True: glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else: glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    ilum.activate_light1(key_event.light1)
    ilum.activate_light2(key_event.light2)
    ilum.set_position1(key_event.light1_pos)
    ilum.set_position2(key_event.light2_pos)

    # Set texture filtering method.
    texture.set_parameters(key_event.object, key_event.gl_linear)
    
    # Set view and projection.
    mat_view = transformation.view(key_event.camera_pos, key_event.camera_front, key_event.camera_up)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    mat_projection = transformation.projection(120, constants.aspect, 0.1, 10000)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    # Draw objects.
    if(not key_event.open_world):
        void.draw()
    else:
        scenario.draw()

    glfw.swap_buffers(window)

glfw.terminate()