import glm

height = 800
width = 800

aspect = 1

mouse_sensitivity = 1.5

delta = 0.1
delta_angles = 0.1
delta_camera = 0.5
delta_ka = 0.05
        
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
void_ilum_paramenters = [1, 1, 1, 5]

scenario_number_objects = 4
scenario_obj_filenames = [
    'models/skybox/skybox.obj',
    'models/chao/chao.obj',
    'models/casa/casa.obj',
    'models/planta/planta.obj'
]
scenario_texture_filenames = [
    'models/skybox/skybox.jpg',
    'models/chao/chao.jpg',
    'models/casa/casa.jpg',
    'models/planta/planta.jpg'
]
scenario_primitives = [
    'quads',
    'quads',
    'triangles',
    'quads',
]
scenario_offsets = [
    [0, 0, 0],
    [0, -1, 0],
    [10, 0.8, 10],
    [15, -0.55, 10]
]
scenario_scale = [
    100,
    105,
    8,
    1
]
scenario_angles = [
    [0, 0, 0],
    [glm.radians(90), 0, 0],
    [0, 0, 0],
    [glm.radians(-90), glm.radians(-90), 0]
]
scenario_ilum_paramenters = [
    [1, 1, 5],
    [1, 1, 5],
    [1, 1, 5],
    [1, 1, 5]
]