import character
import pygame
import generic_object


class Enemy(character.Character):

    def __init__(self, pos_x: float, pos_y: float, current_action: str, sprite: dict = None, size: str = "small", knockback: float = 0.0, speed: float = 0.0, current_face: float = 0.0, base_speed: float = 0.75, physics_type: str = "dynamic"):

        super().__init__(pos_x, pos_y, current_action,
                         sprite, speed, current_face, base_speed, physics_type)
        g = self.global_variable

        g["offense"] = {}
        g["offense"]["knockback"] = knockback
        g["offense"]["charge_speed"] = 1.15
        g["charging"] = False

        g["movement"]["jump_strength"] = -2.5

        g["target"] = "campfire"

        g["size"] = size
        if g["size"] == "big":
            g["health"] = 2
            g["collision_box"] = {
                "minus_width": self.spr.width * 3 / 10,
                "plus_width": self.spr.width * 7 / 10,
                "minus_height": self.spr.height * 1 / 4,
                "plus_height": self.spr.height
            }
        else:
            g["collision_box"] = {
                "minus_width": self.spr.width * 2 / 5,
                "plus_width": self.spr.width * 3 / 5,
                "minus_height": self.spr.height * 1 / 2,
                "plus_height": self.spr.height
            }
            g["health"] = 1

    def update(self, delta_time: float, map: pygame.Surface):

        g = self.global_variable

        if "Die" not in g["animation"]["current_action"]:
            if (g["position"] - g["movement"]["vector"]).is_zero:
                g["movement"]["speed"] = 0
                if g["size"] == "big":
                    g["animation"]["current_action"] = "bigStand"
                else:
                    g["animation"]["current_action"] = "smallStand"
            else:
                if g["animation"]["current_action"] != "bigCharge":
                    g["movement"]["speed"] = g["movement"]["base_speed"]
                    if g["movement"]["vector_y_adjust"] != 0:
                        if g["size"] == "big":
                            g["animation"]["current_action"] = "bigJump"
                        else:
                            g["animation"]["current_action"] = "smallJump"
                    else:
                        if g["size"] == "big":
                            g["animation"]["current_action"] = "bigWalk"
                        else:
                            g["animation"]["current_action"] = "smallWalk"
                else:
                    g["movement"]["speed"] = g["offense"]["charge_speed"]
        g["animation"]["current_face"] = self.direction(
            g["movement"]["vector"])

        if g["animation"]["timer"] > 0:
            g["animation"]["timer"] -= delta_time
            g["frame"] -= 1
            self.animate(g["animation"]["current_action"],
                         map, g["animation"]["current_face"])
        else:
            if g["health"] < 1:
                g["alive"] = False
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

    @property
    def size(self):
        return self.global_variable["size"]

    @property
    def knockback(self):
        return self.global_variable["offense"]["knockback"]

    def get_animation(self):
        return self.global_variable["animation"]["current_action"]

    def jumping(self):
        return self.global_variable["movement"]["vector_y_adjust"] < 0.0

    def hurt(self, projectile_type: str, curr_player: character.Character):
        g = self.global_variable
        g["health"] -= 1
        if g["health"] < 1:
            if projectile_type == "ketchup":
                if g["size"] == "big":
                    g["animation"]["current_action"] = "bigDieKetchup"
                else:
                    g["animation"]["current_action"] = "smallDieKetchup"
            else:
                if g["size"] == "big":
                    g["animation"]["current_action"] = "bigDieMustard"
                else:
                    g["animation"]["current_action"] = "smallDieMustard"
        elif g["health"] == 1 and g["size"] == "big":
            g["animation"]["current_action"] = "bigCharge"
            g["movement"]["vector"] = curr_player.pos.copy()
