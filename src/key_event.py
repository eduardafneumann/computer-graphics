import constants
import glfw, glm, math

open_world = True
polygonal_mode = False
gl_linear = False


object = 0
offsets = [0, 0]
scale = 1
angles = [0, 0, 0]

camera_pos = [1, 0, 0]
camera_front = [-1, 0, 0]
camera_up = [0, 1, 0]

ka = 1
light1 = False
light2 = False
light1_pos = [1, 1, 1]
light2_pos = [1, 0, 1]


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
    global open_world, polygonal_mode, gl_linear
    global object, offsets, scale, angles
    global camera_pos, camera_front, camera_up
    global light1_pos, light2_pos, light1, light2, ka

    
        
    # if key == 68: offsets[0] += delta # d
    # if key == 65: offsets[0] -= delta # a
    # if key == 87: offsets[1] += delta # w
    # if key == 83: offsets[1] -= delta # s

    if key == 88: scale -= constants.delta # x
    if key == 90: scale += constants.delta # z
        
    if key == 265: angles[0] += constants.delta_angles # up
    if key == 264: angles[0] -= constants.delta_angles # down
    if key == 262: angles[1] += constants.delta_angles # right
    if key == 263: angles[1] -= constants.delta_angles # left
    if key ==  77: angles[2] += constants.delta_angles # m
    if key ==  78: angles[2] -= constants.delta_angles # n
    
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
    
    if key == 82: light1_pos[0] += constants.delta # r
    if key == 70: light1_pos[0] -= constants.delta # f
    if key == 84: light1_pos[1] += constants.delta # t
    if key == 71: light1_pos[1] -= constants.delta # g
    if key == 89: light1_pos[2] += constants.delta # y
    if key == 72: light1_pos[2] -= constants.delta # h
    
    if key == 85: light2_pos[0] += constants.delta # u
    if key == 74: light2_pos[0] -= constants.delta # j
    if key == 83: light2_pos[1] += constants.delta # i
    if key == 75: light2_pos[1] -= constants.delta # k
    if key == 79: light2_pos[2] += constants.delta # o
    if key == 76: light2_pos[2] -= constants.delta # l
    
    if key == 48: ka += constants.delta_ka # 0
    if key == 57: ka -= constants.delta_ka # 9
    
    if (key == 81 and action == glfw.PRESS): # q
        light1 = not light1
        
    if (key == 69 and action == glfw.PRESS): # e
        light2 = not light2
    
    # if key == 84: # t
    #     camera_pos = [p + f * constants.delta_camera for p, f in zip(camera_pos, camera_front)]
    
    # if key == 71: # g
    #     camera_pos = [p - f * constants.delta_camera for p, f in zip(camera_pos, camera_front)]
    
    # if key == 70: # f
    #     nor = glm.normalize(glm.cross(camera_front, camera_up))
    #     camera_pos = [p - n * constants.delta_camera for p, n in zip(camera_pos, nor)]
        
    # if key == 72: # h
    #     nor = glm.normalize(glm.cross(camera_front, camera_up))
    #     camera_pos = [p + n * constants.delta_camera for p, n in zip(camera_pos, nor)]


    if (key == 67 and action == glfw.PRESS): # c
        open_world = not open_world
        
    if (key == 80 and action == glfw.PRESS): # p
        polygonal_mode = not polygonal_mode

    if (key == 86 and action == glfw.PRESS): # v
        gl_linear = not gl_linear
        
    
        
    # Changing object.
    reset = False
    if (key == 49 or key == 97)  and object != 0 : object = 0; reset = True
    if (key == 50 or key == 98)  and object != 1 : object = 1; reset = True
    if (key == 51 or key == 99)  and object != 2 : object = 2; reset = True
    if (key == 52 or key == 100) and object != 3 : object = 3; reset = True
    if (key == 53 or key == 101) and object != 4 : object = 4; reset = True

    # Resets the configuration when objects change.
    if reset:
        polygonal_mode = False
        gl_linear = False
        offsets = [0, 0]
        scale = 1
        angles = [0, 0, 0]
        
        
      
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
