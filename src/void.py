import texture
import object
import transformation
from OpenGL.GL import *
import constants

class Void:
    infos = constants.void_number_objects*[object.Info()]
    
    def __init__(self, program, ilum, key_event):
        self.program = program
        self.ilum = ilum
        self.key_event = key_event

    def load(self):
        for i in range(constants.void_number_objects):    
            self.infos[i] = object.load(constants.void_obj_filenames[i])
            self.infos[i].primitive = constants.void_primitives[i]
            texture.load(i, constants.void_texture_filenames[i])

    def draw(self):
        # self.key_event.check_transforamtion_paramenters()
        
        mat_transform = transformation.model(self.infos[self.key_event.object].center, 
                                             self.infos[self.key_event.object].max_distance, 
                                             self.key_event.offsets, self.key_event.scale, self.key_event.angles)
        loc_model = glGetUniformLocation(self.program, "model")
        glUniformMatrix4fv(loc_model, 1, GL_TRUE, mat_transform)
        
        param = constants.void_ilum_paramenters
        self.ilum.set_parameters(param[0], param[1], param[2], param[3])
        
        object.draw(self.program, self.key_event.object, self.infos[self.key_event.object])   