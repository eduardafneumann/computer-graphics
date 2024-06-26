from OpenGL.GL import *
import numpy as np
import math

class Info:
    center = [0, 0, 0]
    max_distance = 0
    n_vertices = 0
    vertice_vbo = 0
    texture_vbo = 0
    normals_vbo = 0
    vertice_config = []
    texture_config = []
    normals_config = []
    primitive = 'triangles'
    
def load_model_from_file(filename):
    vertices = []
    normals = []
    texture_coords = []
    faces = []
    material = None

    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue

        if values[0] == 'v':
            vertices.append(values[1:4])
            
        if values[0] == 'vn':
            normals.append(values[1:4])

        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
            
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)
            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals
    return model

def get_coords_from_model(model):
    
    vertices_list = []    
    textures_coord_list = []
    normals_list = []
    
    for face in model['faces']:
        for vertice_id in face[0]:
            vertices_list.append( model['vertices'][vertice_id-1] )
        for texture_id in face[1]:
            textures_coord_list.append( model['texture'][texture_id-1] )
        for normal_id in face[2]:
            normals_list.append( model['normals'][normal_id-1] )
    
    vertices = np.zeros(len(vertices_list), [("position", np.float32, 3)])
    vertices['position'] = vertices_list
    textures = np.zeros(len(textures_coord_list), [("position", np.float32, 2)])
    textures['position'] = textures_coord_list
    normals = np.zeros(len(normals_list), [("position", np.float32, 3)])
    normals['position'] = normals_list

    return vertices, textures, normals

def get_info(vertices):
    center = np.array([sum(coord) for coord in zip(*vertices['position'])])/len(vertices)
    distances = [math.sqrt((v[0] - center[0])**2 + 
                           (v[1] - center[1])**2 + 
                           (v[2] - center[2])**2) for v in vertices["position"]]
    max_distance = max(distances) # Max euclidian distance of vertices to the center.
    n_vertices = len(vertices['position'])
    
    return center, max_distance, n_vertices

def send_coords_to_gpu(coords, static : bool):
    # Get a buffer and send coordinates.
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    if(static):
        glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)
    else:
        glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_DYNAMIC_DRAW)

    # Used to configurate the shader when displaying the object.
    stride = coords.strides[0]
    offset = ctypes.c_void_p(0)
    dimension = len(coords[0][0])
    config = [dimension, GL_FLOAT, False, stride, offset]

    return vbo, config

def load(object_filename):
    info = Info()

    model = load_model_from_file(object_filename)
    vertices, textures, normals = get_coords_from_model(model)

    info.vertice_vbo, info.vertice_config = send_coords_to_gpu(vertices, False)
    info.texture_vbo, info.texture_config = send_coords_to_gpu(textures, False)
    info.normals_vbo, info.normals_config = send_coords_to_gpu(normals, True)

    info.center, info.max_distance, info.n_vertices = get_info(vertices)

    return info

def draw(program, texture_idx, info):

    # Select texture.
    glBindTexture(GL_TEXTURE_2D, texture_idx)

    # Select and configure texture coordinates.
    glBindBuffer(GL_ARRAY_BUFFER, info.texture_vbo)
    loc_texture = glGetAttribLocation(program, "texture_coord")
    glEnableVertexAttribArray(loc_texture)
    glVertexAttribPointer(loc_texture, 
                          info.texture_config[0], 
                          info.texture_config[1], 
                          info.texture_config[2], 
                          info.texture_config[3], 
                          info.texture_config[4])
    
    # Select and configure object coordinates.
    glBindBuffer(GL_ARRAY_BUFFER, info.vertice_vbo)
    loc_position = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc_position)
    glVertexAttribPointer(loc_position, 
                          info.vertice_config[0], 
                          info.vertice_config[1], 
                          info.vertice_config[2], 
                          info.vertice_config[3], 
                          info.vertice_config[4])
    
    glBindBuffer(GL_ARRAY_BUFFER, info.normals_vbo)
    loc_normals = glGetAttribLocation(program, "normals")
    glEnableVertexAttribArray(loc_normals)
    glVertexAttribPointer(loc_normals, 
                          info.normals_config[0], 
                          info.normals_config[1], 
                          info.normals_config[2], 
                          info.normals_config[3], 
                          info.normals_config[4])

    if info.primitive == 'triangles' :
        glDrawArrays(GL_TRIANGLES, 0, info.n_vertices)
    elif info.primitive == 'lines' :
        glDrawArrays(GL_LINES, 0, info.n_vertices)
    elif info.primitive == 'quads' :
        glDrawArrays(GL_QUADS, 0, info.n_vertices)
    else:
        glDrawArrays(GL_LINE_LOOP, 0, info.n_vertices)
        print("Invalid primitive, the object is not being displayed.")