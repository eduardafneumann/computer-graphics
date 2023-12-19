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

    
    vertex_code_alt = """
        attribute vec3 position;
        attribute vec2 texture_coord;
        attribute vec3 normals;
        
        // these are send to the fragment shader
        varying vec2 out_texture;
        varying vec3 out_fragPos;
        varying vec3 out_normal;
                
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;  
        
        varying vec4 changed_normals;
        
        void main(){
            gl_Position = projection * view * model * vec4(position,1.0);
            out_texture = vec2(texture_coord);
            out_fragPos = vec3(position);
            changed_normals = model * vec4(normals,1.0);
            out_normal = vec3(changed_normals[0], changed_normals[1], changed_normals[2]);
        }
        """
        
    fragment_code_alt = """
        vec3 lightColor = vec3(1.0, 1.0, 1.0);
        uniform vec3 lightPos1;
        uniform vec3 lightPos2;
        uniform vec3 viewPos;
        
        uniform float active1;
        uniform float active2;
        
        
        uniform float ka;
        uniform float kd;
        uniform float ks;
        uniform float ns;
        
        // recebido do vertex shader
        varying vec2 out_texture; 
        varying vec3 out_normal;
        varying vec3 out_fragPos;
        
        uniform sampler2D samplerTexture;    
        
        void main(){
            vec3 ambient = ka * lightColor;             
        
            vec3 norm = normalize(out_normal);
            vec3 lightDir1 = normalize(lightPos1 - out_fragPos);
            vec3 lightDir2 = normalize(lightPos2 - out_fragPos);
            float diff1 = max(dot(norm, lightDir1), 0.0);
            float diff2 = max(dot(norm, lightDir2), 0.0);
            vec3 diffuse1 = kd * diff1 * lightColor;
            vec3 diffuse2 = kd * diff2 * lightColor;
            
            vec3 viewDir = normalize(viewPos - out_fragPos);
            vec3 reflectDir1 = normalize(reflect(-lightDir1, norm));
            vec3 reflectDir2 = normalize(reflect(-lightDir2, norm));
            float spec1 = pow(max(dot(viewDir, reflectDir1), 0.0), ns);
            float spec2 = pow(max(dot(viewDir, reflectDir2), 0.0), ns);
            vec3 specular1 = ks * spec1 * lightColor; 
            vec3 specular2 = ks * spec2 * lightColor;             
            
            vec4 texture = texture2D(samplerTexture, out_texture);
            vec4 result = vec4((ambient + active1*(diffuse1 + specular1) + active2*(diffuse2 + specular2) ),1.0) * texture;
            gl_FragColor = result;
        }
        """
        
    create_shader(program, vertex_code_alt, 'vertex')
    create_shader(program, fragment_code_alt, 'fragment')
    
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
        
    glUseProgram(program)

    return program