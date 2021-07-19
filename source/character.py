import generic_object

class Character(generic_object.Generic_Object):

    def __init__(self, pos_x:float, pos_y:float, current_action:str, sprite:dict=None, speed:float=0.0):

        super().__init__(pos_x, pos_y, sprite, speed)

        g = self.global_variable
        g["current_action"] = current_action

    def update(self, delta_time:float, map:pygame.Surface):

        g = self.global_variable

        return None
