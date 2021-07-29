import character
import pygame
import random
import generic_object


class Player(character.Character):

    def __init__(self, pos_x: float, pos_y: float, current_action: str, sprite: dict = None, speed: float = 0.0, current_face: float = 0.0, base_speed: float = 1.0, physics_type: str = "dynamic"):

        super().__init__(pos_x, pos_y, current_action,
                         sprite, speed, current_face, base_speed, physics_type)
        g = self.global_variable

        g["offense"] = {}
        g["offense"]["ketchup_mustard_ammo_max"] = 100
        g["offense"]["ketchup_mustard_ammo"] = g["offense"]["ketchup_mustard_ammo_max"]

        g["movement"]["momentum"] = 0.0
        g["movement"]["momentum_base"] = g["movement"]["momentum"]
        g["movement"]["momentum_vector"] = self.pos

        g["collision_box"] = {
            "minus_width": self.spr.width * 3 / 8,
            "plus_width": self.spr.width * 5 / 8,
            "minus_height": self.spr.height * 1 / 4,
            "plus_height": self.spr.height
        }

    def update(self, delta_time: float, map: pygame.Surface):

        g = self.global_variable

        if (g["position"] - g["movement"]["vector"]).is_zero:
            g["movement"]["speed"] = 0
            if g["animation"]["current_action"] != "shoot":
                g["animation"]["current_action"] = "standGun"
        else:
            g["movement"]["speed"] = g["movement"]["base_speed"]
            if g["animation"]["current_action"] not in ["walkShootFar", "walkShootNear", "walkShootBoth"]:
                if g["movement"]["vector_y_adjust"] != 0 and g["animation"]["current_action"] != "hurt":
                    g["animation"]["current_action"] = "jumpGun"
                else:
                    g["animation"]["current_action"] = "walkGunNoShoot"
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
            if g["animation"]["current_action"] in ["shoot", "walkShootFar", "walkShootNear", "walkShootBoth"]:
                g["animation"]["current_action"] = "standGun"

        self.travel(g["movement"]["vector"], g["movement"]["speed"])
        g["movement"]["vector"] = g["position"].copy()
        g["movement"]["vector"].x += g["movement"]["vector_x_adjust"]
        g["movement"]["vector"].y += g["movement"]["vector_y_adjust"]
        g["movement"]["vector_y_adjust"] += g["movement"]["gravity"]
        if g["movement"]["gravity"] == 0.0 and g["movement"]["vector_y_adjust"] >= 0:
            g["movement"]["vector_y_adjust"] = 0.0

        if g["movement"]["momentum"] != 0:
            g["movement"]["momentum_vector"] = self.pos
            g["movement"]["momentum_vector"].x += g["movement"]["momentum"]
            g["movement"]["vector_y_adjust"] -= abs(
                g["movement"]["momentum"] * 1/50)
            g["movement"]["momentum"] -= g["movement"]["momentum_base"] * 1 / 50
            self.travel(g["movement"]["momentum_vector"],
                        g["movement"]["momentum"])
            if 0.001 > g["movement"]["momentum"] and -0.001 < g["movement"]["momentum"]:
                g["movement"]["momentum"] = 0.0

        return g["alive"]

    def get_animation(self):
        return self.global_variable["animation"]["current_action"]

    def jumping(self):
        return self.global_variable["movement"]["vector_y_adjust"] < 0.0

    def hurt(self, knockback: float, other_object: generic_object.Generic_Object):
        g = self.global_variable

        g["animation"]["current_action"] = "hurt"
        if self.pos.x - other_object.pos.x < 0:
            g["movement"]["momentum"] = knockback
        else:
            g["movement"]["momentum"] = -knockback
        g["movement"]["momentum_base"] = g["movement"]["momentum"]

    def shoot(self):
        g = self.global_variable
        shot = "shoot"
        if not (g["position"] - g["movement"]["vector"]).is_zero:
            shot = random.choice(
                ["walkShootFar", "walkShootNear", "walkShootBoth"])
        if shot == "shoot":
            g["frame"] = random.randint(0, 2)
        g["animation"]["current_action"] = shot
