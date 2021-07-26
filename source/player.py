import character
import pygame
import math


class Player(character.Character):

    def __init__(self, pos_x: float, pos_y: float, current_action: str, sprite: dict = None, speed: float = 0.0, current_face: float = 0.0, base_speed: float = 1.0):

        super().__init__(pos_x, pos_y, current_action,
                         sprite, speed, current_face, base_speed)
        g = self.global_variable

        g["offense"] = {}
        g["offense"]["ketchup_mustard_ammo_max"] = 100
        g["offense"]["ketchup_mustard_ammo"] = g["offense"]["ketchup_mustard_ammo_max"]

    def update(self, delta_time: float, map: pygame.Surface):

        g = self.global_variable

        if (g["position"] - g["movement"]["vector"]).is_zero:
            g["movement"]["speed"] = 0
            g["animation"]["current_action"] = "standGun"
            g["animation"]["current_face"] = 0
        else:
            g["movement"]["speed"] = g["movement"]["base_speed"]
            if g["movement"]["vector_y_adjust"] != 0 and g["animation"]["current_action"] != "hurt":
                g["animation"]["current_action"] = "jumpGun"
            else:
                g["animation"]["current_action"] = "walkNoGun"
            g["animation"]["current_face"] = self.direction(
                g["movement"]["vector"])

        if g["animation"]["timer"] > 0:
            g["animation"]["timer"] -= delta_time
            g["frame"] -= 1
            self.animate(g["animation"]["current_action"],
                         map, g["animation"]["current_face"])
        else:
            g["animation"]["timer"] = g["animation"]["timer_base"]
            self.animate(g["animation"]["current_action"],
                         map, g["animation"]["current_face"])

        self.travel(g["movement"]["vector"], g["movement"]["speed"])
        g["movement"]["vector"] = g["position"].copy()
        g["movement"]["vector"].x += g["movement"]["vector_x_adjust"]
        g["movement"]["vector"].y += g["movement"]["vector_y_adjust"]
        g["movement"]["vector_y_adjust"] += g["movement"]["gravity"]
        if g["movement"]["gravity"] == 0.0 and g["movement"]["vector_y_adjust"] >= 0:
            g["movement"]["vector_y_adjust"] = 0.0

        return g["alive"]

    def get_animation(self):
        return self.global_variable["animation"]["current_action"]

    def jumping(self):
        return self.global_variable["movement"]["vector_y_adjust"] < 0.0
