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
        attribute vec3 normals;
        
       
        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;        
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(  model * vec4(position, 1.0));
            out_normal = vec3( model *vec4(normals, 1.0));            
        }
        """

        
    fragment_code = """

        vec3 lightColor = vec3(1.0, 1.0, 1.0);
        uniform vec3 lightPos;
        uniform vec3 lightPos2; 
        uniform vec3 viewPos;
        
        uniform float ka;
        uniform float kd;
        uniform float ks;
        uniform float ns;
        
        varying vec2 out_texture;
        varying vec3 out_normal;
        varying vec3 out_fragPos;
        uniform sampler2D samplerTexture;
        
        uniform float active1;
        uniform float active2;
        
        void main(){
            vec3 ambient = ka * lightColor;             
        
            vec3 norm = normalize(out_normal);
            vec3 lightDir = normalize(lightPos - out_fragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = kd * diff * lightColor;
            
            vec3 lightDir2 = normalize(lightPos2 - out_fragPos);
            float diff2 = max(dot(norm, lightDir2), 0.0);
            vec3 diffuse2 = kd * diff2 * lightColor;
            
            vec3 viewDir = normalize(viewPos - out_fragPos);
            vec3 reflectDir = normalize(reflect(-lightDir, norm));
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), ns);
            vec3 specular = ks * spec * lightColor;  
              
            vec3 reflectDir2 = normalize(reflect(-lightDir2, norm));
            float spec2 = pow(max(dot(viewDir, reflectDir2), 0.0), ns);
            vec3 specular2 = ks * spec2 * lightColor;           
            
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + active1*(diffuse + specular) + active2*(diffuse2 + specular2) ),1.0) * texture;
            gl_FragColor = result;
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