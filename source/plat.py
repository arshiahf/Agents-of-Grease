import pygame
import generic_object


class Platform(generic_object.Generic_Object):

    def __init__(self, pos_x: float, pos_y: float, default_action: str = "log", sprite: dict = None, speed: float = 0.0, physics_type: str = "static"):
        super().__init__(pos_x, pos_y, sprite, speed, physics_type)
        g = self.global_variable

        g["animation"] = {}
        g["animation"]["default_action"] = default_action
        g["animation"]["timer_base"] = 0.25
        g["animation"]["timer"] = g["animation"]["timer_base"]

        g["collision_box"] = {
            "minus_width": 0,
            "plus_width": self.spr.width * 9 / 10,
            "minus_height": self.spr.height * 1 / 8,
            "plus_height": self.spr.height * 1 / 2
        }

    def update(self, delta_time: float, map: pygame.Surface):
        g = self.global_variable

        if g["animation"]["timer"] > 0:
            g["animation"]["timer"] -= delta_time
            g["frame"] -= 1
            self.animate(g["animation"]["default_action"],
                         map, 0)
        else:
            g["animation"]["timer"] = g["animation"]["timer_base"]
            self.animate(g["animation"]["default_action"], map, 0)
