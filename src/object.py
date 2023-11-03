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

def send_coords_to_gpu(program, coords, type):
    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, coords.nbytes, coords, GL_STATIC_DRAW)
    stride = coords.strides[0]
    offset = ctypes.c_void_p(0)
    
    if type == 'vertice' :
        loc = glGetAttribLocation(program, "position")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)
    elif type == 'texture' :
        loc = glGetAttribLocation(program, "texture_coord")
        glEnableVertexAttribArray(loc)
        glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
    else:
        print('Invalid coordinates type.')

def get_info(vertices, textures):
    center = np.array([sum(coord) for coord in zip(*vertices['position'])])/len(vertices)
    distances = [math.sqrt(v[0]**2 + v[1]**2 + v[2]**2) for v in vertices["position"]]
    max_distance = max(distances)
    n_vertices = len(vertices['position'])
    
    # n_texture_coords = len(textures['position'])
    # return center, max_distance, n_vertices, n_texture_coords
    
    return center, max_distance, n_vertices


def load(program, object_filename):
    
    # Get vertices and texture coordinates
    model = load_model_from_file(object_filename)
    vertices, textures = get_coords_from_model(model)

    # Send vertices and texture coordinates to GPU
    send_coords_to_gpu(program, vertices, 'vertice')
    send_coords_to_gpu(program, textures, 'texture')
    
    return get_info(vertices, textures)

def draw(object, n_vertices, texture, type):
    first_vertice = 0
    for i in range(object):
        first_vertice += n_vertices[i]

    if texture:
        glBindTexture(GL_TEXTURE_2D, object)
    
    glBindVertexArray(object)
    
    if type == 'line':
        glDrawArrays(GL_LINES, first_vertice, n_vertices[object])
    if type == 'triangle':
        glDrawArrays(GL_TRIANGLES, first_vertice, n_vertices[object])