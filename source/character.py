import generic_object


class Character(generic_object.Generic_Object):

    def __init__(self, pos_x: float, pos_y: float, current_action: str, sprite: dict = None, speed: float = 0.0, current_face: float = 0.0, base_speed: float = 1.0, physics_type: str = "dynamic"):

        super().__init__(pos_x, pos_y, sprite, speed, physics_type)

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

    @property
    def category(self):
        return self.global_variable["category"]

    def move(self, x_adjust: float = 0.0, y_adjust: float = 0.0):
        g = self.global_variable
        g["movement"]["vector_x_adjust"] += x_adjust
        g["movement"]["vector_y_adjust"] += y_adjust

        return None

    def face(self, direction: float):
        self.global_variable["animation"]["current_face"] = direction

    def collide(self, other_object: generic_object.Generic_Object) -> bool:
        g = self.global_variable
        self_coll = self.collision
        other_coll = other_object.collision

        if other_object.phys_type == "static":
            if self.pos.y + self_coll["plus_height"] <= other_object.pos.y + other_coll["minus_height"]:
                if self.pos.y + self_coll["plus_height"] > other_object.pos.y + other_coll["minus_height"] - 5:
                    if self.pos.x + self_coll["plus_width"] >= other_object.pos.x + other_coll["minus_width"]:
                        if self.pos.x + self_coll["minus_width"] <= other_object.pos.x + other_coll["plus_width"]:
                            if g["movement"]["vector_y_adjust"] >= 0.0:
                                g["movement"]["vector_y_adjust"] = 0.0
                                g["movement"]["gravity"] = 0.0
                                return True
        elif other_object.phys_type in ["kinematic", "dynamic"]:
            if self.pos.y + self_coll["minus_height"] < other_object.pos.y + other_coll["plus_height"]:
                if self.pos.y + self_coll["plus_height"] > other_object.pos.y + other_coll["minus_height"]:
                    if self.pos.x + self_coll["minus_width"] < other_object.pos.x + other_coll["plus_width"]:
                        if self.pos.x + self_coll["plus_width"] > other_object.pos.x + other_coll["minus_width"]:
                            return True
        return False
