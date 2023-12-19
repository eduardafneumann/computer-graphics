import texture
import object
import transformation
from OpenGL.GL import *
import constants

class Scenario:
    infos = constants.scenario_number_objects*[object.Info()]
    
    def __init__(self, program, ilum, key_event):
        self.program = program
        self.ilum = ilum
        self.key_event = key_event
        
    def load(self):    
        for i in range(constants.scenario_number_objects):
            self.infos[i] = object.load(constants.scenario_obj_filenames[i])
            self.infos[i].primitive = constants.scenario_primitives[i]
            texture.load(i+constants.void_number_objects, constants.scenario_texture_filenames[i])          
        
    def draw(self):
        self.key_event.keep_camera_in_wolrd_bound()
        
        loc_model = glGetUniformLocation(self.program, "model")
        
        for i in range(constants.scenario_number_objects):
            model = transformation.model(self.infos[i].center, 
                                         self.infos[i].max_distance, 
                                         constants.scenario_offsets[i], 
                                         constants.scenario_scale[i], 
                                         constants.scenario_angles[i])
            glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
            
            param = constants.scenario_ilum_paramenters[i]
            self.ilum.set_parameters(self.key_event.ka, param[0], param[1], param[2])
            object.draw(self.program, i+constants.void_number_objects, self.infos[i])  