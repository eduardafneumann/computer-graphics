from OpenGL.GL import *

def create_shader(program, code, type):

    if type == 'vertex' :
        shader   = glCreateShader(GL_VERTEX_SHADER)
    elif type == 'fragment' :
        shader = glCreateShader(GL_FRAGMENT_SHADER)
    else: 
        print("Invalid shader type.")

    glShaderSource(shader, code)    
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(error)
        raise RuntimeError("Compilation error in {type} shader")
    
    glAttachShader(program, shader)

def create():
    
    program  = glCreateProgram()

    vertex_code = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        varying vec2 out_texture;
        uniform mat4 mat_transformation;    
        
        void main(){
            gl_Position = mat_transformation * vec4(position,1.0);
            out_texture = vec2(texture_coord);
        }
        """

    fragment_code = """
        uniform vec4 color;
        varying vec2 out_texture;
        uniform sampler2D samplerTexture;
        
        void main(){
            vec4 texture = texture2D(samplerTexture, out_texture);
            gl_FragColor = texture;
        }
        """

    create_shader(program, vertex_code, 'vertex')
    create_shader(program, fragment_code, 'fragment')
    
    
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    glUseProgram(program)

    return program