from OpenGL.GL import *

class Camera:
    def __init__(self, program):
        self.program = program
        
    def set_position(self, position):
        loc_view_pos = glGetUniformLocation(self.program, "viewPos")
        glUniform3f(loc_view_pos, position[0], position[1], position[2]) 