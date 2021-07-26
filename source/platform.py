import pygame
import generic_object


class Platform(generic_object.Generic_Object):

    def __init__(self, pos_x: float, pos_y: float, default_action: str = "log", sprite: dict = None, speed: float = 0.0, physics_type: str = "static"):
        super().__init__(pos_x, pos_y, sprite, speed, physics_type)
        g = self.global_variable

        g["animation"] = {}
        g["animation"]["default_action"] = default_action

    def update(self, delta_time: float, map: pygame.Surface):
        g = self.global_variable

        self.animate(g["animation"]["default_action"], map, 0, True)
