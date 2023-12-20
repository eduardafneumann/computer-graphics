import constants
import glfw, glm, math

open_world = constants.default_open_world

draw_sun = constants.default_draw_sun

polygonal_mode = constants.default_polygonal_mode
gl_linear = constants.default_gl_linear 

object = constants.default_object
offsets = constants.default_offsets
scale = constants.default_scale
angles = constants.default_angles

camera_pos = constants.initial_camera_pos
camera_front = constants.initial_camera_front
camera_up = constants.initial_camera_up

ka = 1
light1_active = constants.default_light1_active
light2_active = constants.default_light2_active
light1_pos = constants.void_light_pos[0]
light2_pos = constants.void_light_pos[1]


def check_transforamtion_paramenters():
    global scale, offsets

    # So that the object fit the window and don't scale with negative factors.
    if scale > 1 : scale = 1
    if scale < 0 : scale = 0

    # Since the object starts with maximum possible size while still fitting in the window, 
    # with scale (between 0 and 1), offsets are possible.
    max =  1 - scale
    min = -1 + scale
    if (offsets[0] > max): offsets[0] = max
    if (offsets[0] < min): offsets[0] = min
    if (offsets[1] > max): offsets[1] = max
    if (offsets[1] < min): offsets[1] = min
    
def keep_camera_in_wolrd_bound():
    global camera_pos
    
    if camera_pos[1] < 0: camera_pos[1]=0
    if camera_pos[1] > 50: camera_pos[1]=50
    if camera_pos[0] < -50: camera_pos[0]=-50
    if camera_pos[0] > 50: camera_pos[0]=50
    if camera_pos[2] < -50: camera_pos[2]=-50
    if camera_pos[2] > 50: camera_pos[2]=50

def key_event(window,key,scancode,action,mods):
    global open_world, polygonal_mode, gl_linear, draw_sun
    global object, offsets, scale, angles
    global camera_pos, camera_front, camera_up
    global light1_pos, light2_pos, light1_active, light2_active, ka

    # ===== Void exclusive operations =====
    if(not open_world):
        # Scale
        if key == 88: scale -= constants.delta # x
        if key == 90: scale += constants.delta # z
            
        # Rotation
        if key == 265: angles[0] += constants.delta_angles # up
        if key == 264: angles[0] -= constants.delta_angles # down
        if key == 262: angles[1] += constants.delta_angles # right
        if key == 263: angles[1] -= constants.delta_angles # left
        if key ==  77: angles[2] += constants.delta_angles # m
        if key ==  78: angles[2] -= constants.delta_angles # n
        
        # Light activation
        if (key == 81 and action == glfw.PRESS): # q
            light1_active = not light1_active
        if (key == 69 and action == glfw.PRESS): # e
            light2_active = not light2_active
        
        # Change object
        reset = False
        if (key == 49 or key == 97)  and object != 0 : object = 0; reset = True
        if (key == 50 or key == 98)  and object != 1 : object = 1; reset = True
        if (key == 51 or key == 99)  and object != 2 : object = 2; reset = True
        if (key == 52 or key == 100) and object != 3 : object = 3; reset = True
        if (key == 53 or key == 101) and object != 4 : object = 4; reset = True
        if reset:
            polygonal_mode = constants.default_polygonal_mode
            gl_linear = constants.default_gl_linear
            offsets = constants.default_offsets
            scale = constants.default_scale
            angles = constants.default_angles
        
    # ===== Scenario exclusive operations =====
    if(open_world):
        # Change ambient ilumination
        if key == 73: ka += constants.delta_ka # i
        if key == 75: ka -= constants.delta_ka # k
        
        if key == 82: light1_pos[0] += constants.delta_sun # r
        if key == 70: light1_pos[0] -= constants.delta_sun # f
        if key == 84: light1_pos[1] += constants.delta_sun # t
        if key == 71: light1_pos[1] -= constants.delta_sun # g
        if key == 89: light1_pos[2] += constants.delta_sun # y
        if key == 72: light1_pos[2] -= constants.delta_sun # h
        
        if (key == 66 and action == glfw.PRESS): # b
            draw_sun = not draw_sun
        
    # ===== Common operations =====
    # Change camera position
    if key == 68: # d
        nor = glm.normalize(glm.cross(camera_front, camera_up))
        camera_pos = [p + n * constants.delta_camera for p, n in zip(camera_pos, nor)]
    if key == 65: # a
        nor = glm.normalize(glm.cross(camera_front, camera_up))
        camera_pos = [p - n * constants.delta_camera for p, n in zip(camera_pos, nor)]
    if key == 87: # w
        camera_pos = [p + f * constants.delta_camera for p, f in zip(camera_pos, camera_front)]
    if key == 83: # s
        camera_pos = [p - f * constants.delta_camera for p, f in zip(camera_pos, camera_front)]
    
    # Change between void and scenario
    if (key == 67 and action == glfw.PRESS): # c
        open_world = not open_world
        camera_pos = constants.initial_camera_pos
        camera_front = constants.initial_camera_front
        camera_up = constants.initial_camera_up
        if(open_world):
            light1_pos = constants.scenario_light_pos
            light1_active = True
            light2_active = False
        else:
            light1_pos = constants.void_light_pos[0]
            light2_pos = constants.void_light_pos[1]
    
    # Show polygonal mode
    if (key == 80 and action == glfw.PRESS): # p
        polygonal_mode = not polygonal_mode

    # Change texture rendering
    if (key == 86 and action == glfw.PRESS): # v
        gl_linear = not gl_linear

    
    
    
    

    

        
    
        
    
        

        
        
      
first_mouse = True
yaw = -90.0 
pitch = 0.0
xcenter =  constants.width/2
ycenter =  constants.height/2

def mouse_event(window, xpos, ypos):
    global first_mouse, camera_front, yaw, pitch, xcenter, ycenter
    if first_mouse:
        xcenter = xpos
        ycenter = ypos
        first_mouse = False

    xoffset = xpos - xcenter
    yoffset = ycenter - ypos
    xcenter = xpos
    ycenter = ypos

    xoffset *= constants.mouse_sensitivity
    yoffset *= constants.mouse_sensitivity

    yaw += xoffset
    pitch += yoffset
    
    if pitch >= 90.0: pitch = 90.0
    if pitch <= -90.0: pitch = -90.0

    front = glm.vec3()
    front.x = math.cos(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    front.y = math.sin(glm.radians(pitch))
    front.z = math.sin(glm.radians(yaw)) * math.cos(glm.radians(pitch))
    camera_front = glm.normalize(front)
