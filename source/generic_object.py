import pygame
import vector

class Generic_Object:

    def __init__(self, pos_x:float, pos_y:float, sprite:dict=None, speed:float=0.0):

        self.global_variable = {}
        g = self.global_variable

        g["position"] = vector.Vector2(pos_x, pos_y)
        g["speed"] = speed
        g["alive"] = True

        if sprite != None:
            g["sprite"] = sprite
            g["frame"] = -1

    @property
    def pos(self):
        return self.global_variable["position"].copy()

    @pos.setter
    def pos(self, new_vector:vector.Vector2):
        if not issubclass(vector.Vector2, new_vector):
            raise TypeError("Assignable for position must be a Vector2.")
        else:
            self.global_variable["position"] = new_vector.copy()

    def animate(self, animation:str, map:pygame.Surface, direction:float):
        g = self.global_variable
        g["frame"], sprite_location, spritesheet = g["sprite"].call_frame(animation, direction, g["frame"])
        map.blit(spritesheet, g["position"], sprite_location)
