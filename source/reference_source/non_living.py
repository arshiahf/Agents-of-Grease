import generic_object

class Non_Living(generic_object.Generic_Object):

    def __init__(self, pos_x:float, pos_y:float, sprite:dict=None, speed:float=0.0):

        super().__init__(pos_x, pos_y, sprite, speed)
