import generic_object
import vector
import sprite

class Items(generic_object.Generic_Object):
    def __init__(self, pos_x:float, pos_y:float, sprite:dict=None, speed:float=0.0):
        super().__init__(pos_x, pos_y, sprite, speed)

# New Parts
    def ammo_packets(self, pos_x, pos_y, sprite):
        self.global_variable = {}
        g = self.global_variable
        g["position"] = vector.Vector2(pos_x, pos_y)
        g["refill"] = 30
        g["spawn"] = {}
        g["pickup"] = "False"

        if Items.__class__() != None:
            generic_object.Generic_Object.__init__()
            if Items.ammo_packets() > 0:
                g["ammo_packets"] = sprite
                g["frame"] = -1

                if g["pickup"] != "True":
                    g["spawn"] != 0


class Rocket:
    def __init__(self):
        self.position = {}
        self.pickup = "False"

    def pickle_jar(self, pos_x, pos_y, sprite):
        self.global_variable = {}
        g = self.global_variable
        g["position"] = vector.Vector2(pos_x, pos_y)
        g["spawn"] = {}

        if Items.__class__() != None:
            generic_object.Generic_Object.__init__()
            if Items.pickle_jar() != 1:
                g["pickle_jar"] = sprite
                g["frame"] = -1

    def update(self, grab, cur_x, cur_y, new_x, new_y):
        g = self.global_variable

        if g["pickle_jar"] != g["grab"]:
            self.pickup = "True"
            self.pickup = grab

        if cur_x and cur_y != 0:
            self.spawn = new_x, new_y