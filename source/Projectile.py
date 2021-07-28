import random

import pygame
import vector
import Items
import math

class Projectitle(Items.Items):
    def __init__(self, pos_x:float, pos_y:float, origin:vector.Vector2, speed_vector:vector.Vector2, range:float, sprite:dict=None, speed:float=0.0, damage:float=1):
        super().__init__(pos_x, pos_y, sprite, speed)
        glob = self.global_variable
        glob["origin"] = origin
        glob["direction"] = speed_vector
        glob["range"] = range
        glob["move_time_base"] = 0.05
        glob["move_timer"] = 0
        glob["threat_area"] = glob["sprite"].width
        glob["damage"] = damage

    def update(self, delta_time: float, map: pygame.Surface):

        glob = self.global_variable

        if glob["move_timer"] > 0:
            glob["move_timer"] -= delta_time
            glob["frame"] -= 1
            self.animate("fly", map, self.direction(glob["direction"]))
        else:
            glob["move_timer"] = glob["move_time_base"]
            self.animate("fly", map, self.direction(glob["direction"]))

        self.travel(glob["direction"], glob["speed"])
        glob["direction"] += glob["speed"] * self.speed_vector(glob["direction"])

        if self.distance(glob["origin"]) > glob["range"]:
            glob["alive"] = False

        return glob["alive"]

    @property
    def threat_area(self):
        return self.global_variable["threat_area"]

    @property
    def damage(self):
        return self.global_variable["damage"]

    # New Parts
    # def shoot(self, hit, shot, event, screen):
    #
    #     g = self.global_variable
    #
    #     g["K_proj"] = []
    #     g["M_proj"] = []
    #     g["R_proj"] = []
    #
    #
    #
    #     # if g["K_proj"] or g["M_proj"] or g["R_proj"] != hit:
    #     #     g["enemy"]["sprite"] = "defeat"
    #     return None
