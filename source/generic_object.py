import pygame
import vector
import math
import sprite as sprite_manager


class Generic_Object:

    def __init__(self, pos_x: float, pos_y: float, sprite: dict = None, speed: float = 0.0, physics_type: str = "dynamic"):

        self.global_variable = {}
        g = self.global_variable

        g["position"] = vector.Vector2(pos_x, pos_y)
        g["movement"] = {}
        g["movement"]["speed"] = speed
        g["alive"] = True

        g["movement"]["physics_type"] = physics_type
        if physics_type == "dynamic":
            g["movement"]["gravity_base"] = 0.004
        elif physics_type == "static" or physics_type == "kinematic":
            g["movement"]["gravity_base"] = 0.0
        g["movement"]["gravity"] = g["movement"]["gravity_base"]

        g["collision_box"] = {}

        if sprite is not None:
            g["sprite"]: sprite_manager.Sprite = sprite
            g["frame"] = -1

    @property
    def pos(self):
        return self.global_variable["position"].copy()

    @pos.setter
    def pos(self, new_vector: vector.Vector2):
        if not issubclass(new_vector.__class__, vector.Vector2):
            raise TypeError("Assignable for position must be a Vector2.")
        else:
            self.global_variable["position"] = new_vector.copy()

    @property
    def spr(self):
        return self.global_variable["sprite"]

    @property
    def phys_type(self):
        return self.global_variable["movement"]["physics_type"]

    @property
    def collision(self):
        return self.global_variable["collision_box"]

    def has_grav(self):
        return self.global_variable["movement"]["gravity"] == self.global_variable["movement"]["gravity_base"]

    def restore_grav(self):
        self.global_variable["movement"]["gravity"] = self.global_variable["movement"]["gravity_base"]

    def distance(self, other_object: vector.Vector2):

        distance_vector = other_object - self.pos
        return distance_vector.magnitude

    def direction(self, other_object: vector.Vector2):

        distance_vector = other_object - self.pos
        return distance_vector.radians

    def speed_vector(self, other_object: vector.Vector2):

        distance_vector = other_object - self.pos
        return distance_vector.normalized

    def travel(self, destination: vector.Vector2, travel_speed: float):
        self.global_variable["position"] += travel_speed * \
            self.speed_vector(destination)

    def animate(self, animation: str, map: pygame.Surface, direction: float, static: bool = False):
        g = self.global_variable
        if direction < math.pi / 2 and direction >= -math.pi / 2:
            direction = 0
        else:
            direction = math.pi
        g["frame"], sprite_location, spritesheet = g["sprite"].call_frame(
            animation, direction, g["frame"], static)
        map.blit(spritesheet, g["position"], sprite_location)
