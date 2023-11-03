from OpenGL.GL import *
import numpy as np
import math

def load_model_from_file(filename):
    vertices = []
    texture_coords = []
    faces = []
    material = None

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            vertices.append(values[1:4])

        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
            
        elif values[0] == 'f':
            face = []
            face_texture = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)
            faces.append((face, face_texture, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    return model

def get_coords_from_model(model):
    
    vertices_list = []    
    textures_coord_list = []
    
    for face in model['faces']:
        for vertice_id in face[0]:
            vertices_list.append( model['vertices'][vertice_id-1] )
        for texture_id in face[1]:
            textures_coord_list.append( model['texture'][texture_id-1] )
    
    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list
    textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])
    textures['position'] = textures_coord_list

    return vertices, textures

def get_info(vertices):
    center = np.array([sum(coord) for coord in zip(*vertices['position'])])/len(vertices)
    distances = [math.sqrt(v[0]**2 + v[1]**2 + v[2]**2) for v in vertices["position"]]
    max_distance = max(distances)
    n_vertices = len(vertices['position'])
    
    return center, max_distance, n_vertices

def send_texture_coords_to_gpu(coords):
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)

    stride = coords.strides[0]
    offset = ctypes.c_void_p(0)

    config = [2, GL_FLOAT, False, stride, offset]
    
    # loc = glGetAttribLocation(program, "texture_coord")
    # glEnableVertexAttribArray(loc)
    # glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)

    return vbo, config

def send_vertices_to_gpu(vertices):
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    config = [3, GL_FLOAT, False, stride, offset]

    return vbo, config

class Info:
    center = [0, 0, 0]
    max_distance = 0
    n_vertices = 0
    vertice_vbo = 0
    texture_vbo = 0
    vertice_config = []
    texture_config = []
    primitive = 'triangles'

def load(object_filename):
    info = Info()

    model = load_model_from_file(object_filename)
    vertices, textures = get_coords_from_model(model)

    info.vertice_vbo, info.vertice_config = send_vertices_to_gpu(vertices)
    info.texture_vbo, info.texture_config = send_texture_coords_to_gpu(textures)

    info.center, info.max_distance, info.n_vertices = get_info(vertices)

    return info

def draw(program, object, infos):
    first_vertice = 0
    for i in range(object):
        first_vertice += infos[i].n_vertices

    glBindTexture(GL_TEXTURE_2D, object)

    glBindBuffer(GL_ARRAY_BUFFER, infos[object].texture_vbo)
    loc_texture = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc_texture)
    glVertexAttribPointer(loc_texture, 
                          infos[object].texture_config[0], 
                          infos[object].texture_config[1], 
                          infos[object].texture_config[2], 
                          infos[object].texture_config[3], 
                          infos[object].texture_config[4])
    
    glBindBuffer(GL_ARRAY_BUFFER, infos[object].vertice_vbo)
    loc_position = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_position)
    glVertexAttribPointer(loc_position, 
                          infos[object].vertice_config[0], 
                          infos[object].vertice_config[1], 
                          infos[object].vertice_config[2], 
                          infos[object].vertice_config[3], 
                          infos[object].vertice_config[4])
    
    if infos[object].primitive == 'triangles' :
        glDrawArrays(GL_TRIANGLES, first_vertice, infos[object].n_vertices)
    if infos[object].primitive == 'lines' :
        glDrawArrays(GL_LINES, first_vertice, infos[object].n_vertices)