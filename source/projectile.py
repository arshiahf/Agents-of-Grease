import pygame
import generic_object
import vector


class Projectile(generic_object.Generic_Object):

    def __init__(self, pos_x: float, pos_y: float, direction_vector: vector.Vector2, projectile_type: str, sprite: dict = None, splat_sprite: dict = None, speed: float = 1.0, physics_type: str = "kinematic"):

        super().__init__(pos_x, pos_y, sprite, speed, physics_type)
        g = self.global_variable

        g["movement"]["direction_vector"] = direction_vector
        g["splatted"] = False
        g["dead"] = False

        g["animation"] = {}
        g["animation"]["timer_base"] = 0.15
        g["animation"]["timer"] = g["animation"]["timer_base"]
        g["projectile_type"] = projectile_type
        if g["projectile_type"] == "ketchup":
            g["animation"]["current_action"] = "ketchupFly"
        elif g["projectile_type"] == "mustard":
            g["animation"]["current_action"] = "mustardFly"
        g["animation"]["current_face"] = self.direction(direction_vector)

        g["collision_box"] = {
            "minus_width": 0,
            "plus_width": self.spr.width * 9 / 10,
            "minus_height": 0,
            "plus_height": self.spr.height
        }

        if splat_sprite is not None:
            g["splat_sprite"] = splat_sprite

    def update(self, delta_time: float, map: pygame.Surface) -> bool:
        g = self.global_variable

        if abs(g["position"].x - g["movement"]["direction_vector"].x) <= 2 * g["movement"]["speed"]:
            if g["movement"]["direction_vector"].x < g["position"].x:
                g["movement"]["direction_vector"].x -= 2 * g["movement"]["speed"]
            else:
                g["movement"]["direction_vector"].x += 2 * g["movement"]["speed"]

        if g["splatted"] and g["frame"] > 0:
            g["dead"] = True

        if g["animation"]["timer"] > 0:
            g["animation"]["timer"] -= delta_time
            g["frame"] -= 1
            self.animate(g["animation"]["current_action"],
                         map, g["animation"]["current_face"])
        else:
            g["animation"]["timer"] = g["animation"]["timer_base"]
            self.animate(g["animation"]["current_action"],
                         map, g["animation"]["current_face"])

        if g["splatted"] and g["sprite"] is not g["splat_sprite"]:
            g["sprite"] = g["splat_sprite"]
            if g["projectile_type"] == "ketchup":
                g["animation"]["current_action"] = "ketchupSplat"
            elif g["projectile_type"] == "mustard":
                g["animation"]["current_action"] = "mustardSplat"
            g["frame"] = 0

        if not g["splatted"]:
            self.travel(g["movement"]["direction_vector"],
                        g["movement"]["speed"])

        return g["dead"]

    def splat(self):
        self.global_variable["splatted"] = True

    def is_splatted(self):
        return self.global_variable["splatted"]
