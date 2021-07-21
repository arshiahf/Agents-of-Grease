import generic_object
import math

class Character(generic_object.Generic_Object):

    def __init__(self, pos_x:float, pos_y:float, current_action:str, sprite:dict=None, speed:float=0.0, current_face:float=0.0, base_speed:float=1.0):

        super().__init__(pos_x, pos_y, sprite, speed)

        g = self.global_variable
        g["animation"] = {}
        g["animation"]["current_action"] = current_action
        g["animation"]["timer_base"] = 0.25
        g["animation"]["timer"] = 0
        g["animation"]["current_face"] = current_face

        g["movement"]["base_speed"] = base_speed
        g["movement"]["vector"] = g["position"].copy()
        g["movement"]["vector_x_adjust"] = 0
        g["movement"]["vector_y_adjust"] = 0
        g["movement"]["jump_strength"] = 1.0
