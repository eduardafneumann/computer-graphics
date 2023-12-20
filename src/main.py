import glfw
from OpenGL.GL import *

import window 
import user_interaction 
import program 
import texture 
import transformation
from ilumination import Ilumination
import constants
from void import Void
from scenario import Scenario
from camera import Camera

window = window.create(constants.height, constants.width)
glfw.set_key_callback(window, user_interaction.key_event)
glfw.set_cursor_pos_callback(window, user_interaction.mouse_event)

program = program.create()

ilum = Ilumination(program)
void = Void(program, ilum, user_interaction)
scenario = Scenario(program, ilum, user_interaction)
camera = Camera(program)

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
    if user_interaction.polygonal_mode==True: glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    else: glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    
    ilum.activate_light1(user_interaction.light1_active)
    ilum.activate_light2(user_interaction.light2_active)
    ilum.set_position1(user_interaction.light1_pos)
    ilum.set_position2(user_interaction.light2_pos)

    # Set texture filtering method.
    texture.set_parameters(user_interaction.object, user_interaction.gl_linear)
    
    camera.set_position(user_interaction.camera_pos)
    
    # Set view and projection.
    mat_view = transformation.view(user_interaction.camera_pos, user_interaction.camera_front, user_interaction.camera_up)
    loc_view = glGetUniformLocation(program, "view")
    glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)
    mat_projection = transformation.projection(120, constants.aspect, 0.1, 10000)
    loc_projection = glGetUniformLocation(program, "projection")
    glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)

    # Draw objects.
    if(not user_interaction.open_world):
        void.draw()
    else:
        scenario.draw()

    glfw.swap_buffers(window)

glfw.terminate()