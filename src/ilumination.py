from OpenGL.GL import *

class Ilumination:
    ka = 0.5
    kd = 1
    ks = 1
    ns = 5
    
    def __init__(self, program):
        self.program = program
        
    def set_parameters(self, ka, kd, ks, ns):
        loc_ka = glGetUniformLocation(self.program, "ka") 
        glUniform1f(loc_ka, ka)

        loc_kd = glGetUniformLocation(self.program, "kd") 
        glUniform1f(loc_kd, kd)

        loc_ks = glGetUniformLocation(self.program, "ks") 
        glUniform1f(loc_ks, ks)        

        loc_ns = glGetUniformLocation(self.program, "ns") 
        glUniform1f(loc_ns, ns) 
        
    def set_position1(self, position):
        loc_light_pos = glGetUniformLocation(self.program, "lightPos1")
        glUniform3f(loc_light_pos, position[0], position[1], position[2])
        
    def set_position2(self, position):
        loc_light_pos = glGetUniformLocation(self.program, "lightPos2")
        glUniform3f(loc_light_pos, position[0], position[1], position[2])
        
    def activate_light1(self, on):
        loc_active = glGetUniformLocation(self.program, "active1")
        if on==True:
            glUniform1f(loc_active, 1.0) 
        if on==False:
            glUniform1f(loc_active, 0.0) 
        
    def activate_light2(self, on):
        loc_active = glGetUniformLocation(self.program, "active2")
        if on:
            glUniform1f(loc_active, 1.0) 
        else:
            glUniform1f(loc_active, 0.0) 
        
