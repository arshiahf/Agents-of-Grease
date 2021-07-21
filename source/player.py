import character
import pygame
import math

class Player(character.Character):

    def __init__(self, pos_x:float, pos_y:float, current_action:str, sprite:dict=None, speed:float=0.0, current_face:float=0.0, base_speed:float=1.0):

        super().__init__(pos_x, pos_y, current_action, sprite, speed, current_face, base_speed)
        g = self.global_variable

        g["offense"] = {}
        g["offense"]["ketchup_mustard_ammo_max"] = 100
        g["offense"]["ketchup_mustard_ammo"] = g["offense"]["ketchup_mustard_ammo_max"]

    def update(self, delta_time:float, map:pygame.Surface):

        g = self.global_variable

        if g["animation"]["timer"] > 0:
            g["animation"]["timer"] -= delta_time
            g["frame"] -= 1
            self.animate(g["animation"]["current_action"], map, g["animation"]["current_face"])
        else:
            g["animation"]["timer"] = g["animation"]["timer_base"]
            self.animate(g["animation"]["current_action"], map, g["animation"]["current_face"])
