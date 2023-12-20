import texture
import object
import transformation
from OpenGL.GL import *
import constants
import glm
import numpy as np

class Scenario:
    infos = constants.scenario_number_objects*[object.Info()]
    turtle_offset = constants.scenario_offsets[4]
    turtle_angles = constants.scenario_angles[4]
    turning = False
    delta = constants.turtle_delta
    max_steps = 10/delta
    signal = 1
    steps = 0
    
    def __init__(self, program, ilum, key_event):
        self.program = program
        self.ilum = ilum
        self.key_event = key_event
        
    def load(self):    
        for i in range(constants.scenario_number_objects):
            self.infos[i] = object.load(constants.scenario_obj_filenames[i])
            self.infos[i].primitive = constants.scenario_primitives[i]
            texture.load(i+constants.void_number_objects, constants.scenario_texture_filenames[i])
        
    def move_turtle(self):
        if(not self.turning):
            self.turtle_offset[2] -= self.signal * self.delta
            self.steps += 1
            if(self.steps >= self.max_steps):
                self.turning = True
                self.steps=0
                self.signal *= -1
        else:
            self.turtle_angles[1] -= self.signal * glm.radians(30*self.delta)
            if(-self.signal*self.turtle_angles[1] >= 
                glm.radians(90) - self.signal*glm.radians(90)):
                self.turning = False
                self.turtle_angles[1] = glm.radians(90) - self.signal*glm.radians(90)
            
        return transformation.model(self.infos[4].center, 
                                    self.infos[4].max_distance, 
                                    self.turtle_offset, 
                                    constants.scenario_scale[4], 
                                    self.turtle_angles)
        
    def move_light():
        pass
        
    def draw(self):
        self.key_event.keep_camera_in_wolrd_bound()
        
        loc_model = glGetUniformLocation(self.program, "model")
        
        for i in range(constants.scenario_number_objects):
            if(i==7 and not self.key_event.draw_sun):
                continue
            
            if(i==4):
                model = self.move_turtle()
            elif(i==7):
                model = transformation.model(self.infos[i].center, 
                                         self.infos[i].max_distance, 
                                         self.key_event.light1_pos, 
                                         constants.scenario_scale[i], 
                                         constants.scenario_angles[i])
            else:
                model = transformation.model(self.infos[i].center, 
                                         self.infos[i].max_distance, 
                                         constants.scenario_offsets[i], 
                                         constants.scenario_scale[i], 
                                         constants.scenario_angles[i])
                
            glUniformMatrix4fv(loc_model, 1, GL_TRUE, model)
            
            param = constants.scenario_ilum_paramenters[i]
            self.ilum.set_parameters(self.key_event.ka, param[0], param[1], param[2])
            
            object.draw(self.program, i+constants.void_number_objects, self.infos[i])  