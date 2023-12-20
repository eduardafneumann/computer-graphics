import glm

height = 800
width = 800

aspect = 1

mouse_sensitivity = 1

delta = 0.5
delta_angles = 0.1
delta_camera = 0.1
delta_ka = 0.05
delta_sun = 0.7

initial_camera_pos = [1, 0, 0]
initial_camera_front = [-1, 0, 0]
initial_camera_up = [0, 1, 0]

default_light1_active = True
default_light2_active = False

default_object = 0
default_offsets = [0, 0, 0]
default_scale = 1
default_angles = [0, 0, 0]
default_polygonal_mode = False
default_gl_linear = False
default_open_world = False
default_draw_sun = False
        
void_number_objects = 5
void_obj_filenames = [
    'models/tartaruga/tartaruga.obj',
    'models/casa/casa.obj',
    'models/planta/planta.obj',
    'models/estatua/estatua.obj',
    'models/touro/touro.obj'
]
void_texture_filenames = [
    'models/tartaruga/tartaruga.jpg',
    'models/casa/casa.jpg',
    'models/planta/planta.jpg',
    'models/estatua/estatua.jpg',
    'models/touro/touro.jpg'
]
void_primitives = [
    'quads',
    'triangles',
    'quads',
    'quads',
    'quads'
]
void_ilum_paramenters = [1, 0.5, 0.5, 3]
void_light_pos = [
    [1, -4, 0],
    [0, 5, 5]
]

scenario_number_objects = 11
scenario_obj_filenames = [
    'models/skybox/skybox.obj',
    'models/chao/chao.obj',
    'models/casa/casa.obj',
    'models/planta/planta.obj',
    'models/tartaruga/tartaruga.obj',
    'models/comoda/comoda.obj',
    'models/lumi/lumi.obj',
    'models/sol/sol.obj',
    'models/cactu/cactu.obj',
    'models/estatua/estatua.obj', 
    'models/cama/cama.obj', 
]
scenario_texture_filenames = [
    'models/skybox/skybox.jpg',
    'models/chao/chao.jpg',
    'models/casa/casa.jpg',
    'models/planta/planta.jpg',
    'models/tartaruga/tartaruga.jpg',
    'models/comoda/comoda.tga',
    'models/lumi/lumi.jpg',
    'models/sol/sol.jpg',
    'models/cactu/cactu.jpg', 
    'models/estatua/estatua.jpg', 
    'models/cama/cama.png', 
]
scenario_primitives = [
    'quads',
    'quads',
    'triangles',
    'quads',
    'quads',
    'quads',
    'quads',
    'quads',
    'quads',
    'quads',
    'quads'
]
scenario_offsets = [
    [0, 0, 0],
    [0, -1, 0],
    [10, 0.8, 10],
    [15, -0.55, 10],
    [-10, -0.5, 0],
    [8.5, -0.5, 11],
    [8.3, 0.4, 11],
    [0, 0, 0],
    [5, 1, 0],
    [5.5, 0, 9.5],
    [14, -0.3, 12],
]
scenario_scale = [
    100,
    100,
    8,
    1,
    1,
    1,
    0.4,
    1,
    3,
    1.2,
    2,
]
scenario_angles = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [glm.radians(-90), glm.radians(-90), 0],
    [glm.radians(90), 0, glm.radians(180)],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, glm.radians(90), glm.radians(90)],
    [glm.radians(-90), glm.radians(-70), 0],
    [0, glm.radians(-90), 0],
]
scenario_ilum_paramenters = [
    [0, 0, 1],
    [0.8, 0.5, 30],
    [2, 0.9, 30],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
    [0.9, 0.5, 5],
]
scenario_light_pos = [-17, 50, -35]
turtle_delta = 0.01
