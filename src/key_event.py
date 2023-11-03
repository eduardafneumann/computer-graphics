import glfw

polygonal_mode = True
gl_linear = False
object = 0
offsets = [0, 0]
scale = 1
angles = [0, 0, 0]

def check_transforamtion_paramenters():
    global scale, offsets

    if scale > 1 : scale = 1
    if scale < 0 : scale = 0

    max =  1 - scale
    min = -1 + scale
    if (offsets[0] > max): offsets[0] = max
    if (offsets[0] < min): offsets[0] = min
    if (offsets[1] > max): offsets[1] = max
    if (offsets[1] < min): offsets[1] = min

def key_event(window,key,scancode,action,mods):
    global polygonal_mode, gl_linear, object, offsets, scale, angles

    delta = 0.1
    delta_angles = 0.1
        
    if key == 68: offsets[0] += delta # d
    if key == 65: offsets[0] -= delta # a
    if key == 87: offsets[1] += delta # w
    if key == 83: offsets[1] -= delta # s

    if key == 88: scale -= delta # x
    if key == 90: scale += delta # z
        
    if key == 265: angles[0] += delta_angles # up
    if key == 264: angles[0] -= delta_angles # down
    if key == 262: angles[1] += delta_angles # right
    if key == 263: angles[1] -= delta_angles # left
    if key == 77: angles[2] += delta_angles # m
    if key == 78: angles[2] -= delta_angles # n

    if (key == 80 and action == glfw.PRESS):
        polygonal_mode = not polygonal_mode

    if (key == 86 and action == glfw.PRESS):
        gl_linear = not gl_linear

    reset = False
    if (key == 49 or key == 97): object = 0; reset = True
    if (key == 50 or key == 98): object = 1; reset = True
    if (key == 51 or key == 99): object = 2; reset = True
    if (key == 52 or key == 100): object = 3; reset = True
    if (key == 53 or key == 101): object = 4; reset = True

    if reset:
        polygonal_mode = True
        gl_linear = False
        offsets = [0, 0]
        scale = 1
        angles = [0, 0, 0]