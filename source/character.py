import generic_object
import math


class Character(generic_object.Generic_Object):

    def __init__(self, pos_x: float, pos_y: float, current_action: str, sprite: dict = None, speed: float = 0.0, current_face: float = 0.0, base_speed: float = 1.0):

        super().__init__(pos_x, pos_y, sprite, speed)

        g = self.global_variable
        g["animation"] = {}
        g["animation"]["current_action"] = current_action
        g["animation"]["timer_base"] = 0.20
        g["animation"]["timer"] = 0
        g["animation"]["current_face"] = current_face

        g["movement"]["base_speed"] = base_speed
        g["movement"]["vector"] = g["position"].copy()
        g["movement"]["vector_x_adjust"] = 0
        g["movement"]["vector_y_adjust"] = 0
        g["movement"]["jump_strength"] = 1.0

    def move(self, x_adjust: float = 0.0, y_adjust: float = 0.0):
        g = self.global_variable
        g["movement"]["vector_x_adjust"] += x_adjust
        g["movement"]["vector_y_adjust"] += y_adjust

        return None

    def face(self, direction: float):
        self.global_variable["animation"]["current_face"] = direction

    def collide(self, other_object: generic_object.Generic_Object) -> bool:
        g = self.global_variable
        self_min_width = self.pos.x + self.spr.width * 3 / 8
        self_plus_width = self.pos.x + self.spr.width * 5 / 8
        other_min_width = other_object.pos.x
        other_plus_width = other_object.pos.x + other_object.spr.width * 9 / 10
        self_min_height = self.pos.y - self.spr.height / 2
        self_plus_height = self.pos.y + self.spr.height / 2
        other_min_height = other_object.pos.y - other_object.spr.height
        other_plus_height = other_object.pos.y + other_object.spr.height / 2

        if other_object.phys_type == "static" or other_object.phys_type == "kinematic":
            if self_plus_height <= other_min_height and self_plus_height > other_min_height - 5:
                if self_plus_width >= other_min_width and self_min_width <= other_plus_width:
                    if g["movement"]["vector_y_adjust"] >= 0.0:
                        g["movement"]["gravity"] = 0.0
                        return True
            return False
