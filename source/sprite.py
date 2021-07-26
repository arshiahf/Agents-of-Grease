import json
import pygame
import math


class Sprite_Manager:

    def __init__(self):

        self.global_variable = {}
        self.global_variable["sheet_jsons"] = []
        self.global_variable["sprites"] = {}

    def load_sprite(self, path: str, filename: str) -> None:

        glob = self.global_variable
        try:
            temp_file = open(path + filename, "r")
        except FileNotFoundError:
            print("File does not exist")
            return None
        glob["sheet_jsons"].append(json.load(temp_file))
        temp_file.close()
        current_sheet = glob["sheet_jsons"][len(glob["sheet_jsons"]) - 1]

        for image in current_sheet["images"]:
            sprite_name = image[:image.rfind(".")]
            glob["sprites"][sprite_name] = self.extract_sprite(
                path, image, current_sheet["frame_dimensions"], current_sheet["animations"], current_sheet["is_static"])

        return None

    # Returns a sprite from a file reference
    def extract_sprite(self, path: str, image_filename: str, dimensions: list, animations: dict, static: bool = False) -> "Sprite":

        sprite_image = pygame.image.load(path + image_filename).convert_alpha()
        frame_dimensions = (dimensions[0], dimensions[1])
        for key in animations.keys():
            if len(animations[key]) == 1 and not static:
                square_dimension = max(dimensions[0], dimensions[1])
                frame_dimensions = (square_dimension, square_dimension)
        return Sprite(sprite_image, frame_dimensions, animations)

    def __str__(self):
        glob = self.global_variable
        sprites_string = "Sprites:"
        dict_index = len(glob["sprites"])
        for key in glob["sprites"].keys():
            sprites_string += "\n"
            sprites_string += "\t"
            sprites_string += key + ": " + str(glob["sprites"][key])
            dict_index -= 1
        return sprites_string

    def __getitem__(self, index: str):
        return self.global_variable["sprites"][index]

    @property
    def spritelist(self):
        sprite_list = []
        for key in self.global_variable["sprites"].keys():
            sprite_list.append(key)
        return sprite_list


class Sprite:

    def __init__(self, spritesheet: pygame.Surface, dimensions: tuple, animations: dict):

        self.global_variable = {}
        glob = self.global_variable
        glob["sheet"] = spritesheet
        glob["framesize"] = dimensions
        glob["animations"] = self.unpack_animations(animations)

    # Returns a dictionary of all animations the sprite has
    def unpack_animations(self, raw_animations: dict) -> dict:

        glob = self.global_variable
        animations = {}
        for key in raw_animations.keys():
            animations[key] = {}
            for direction_key in raw_animations[key].keys():
                animations[key][direction_key] = []
                for frame in raw_animations[key][direction_key]:
                    animations[key][direction_key].append(
                        (frame[0] * glob["framesize"][0], frame[1] * glob["framesize"][1]))
        return animations

    # Returns the frame number, the frame location, and the sprite sheet used
    def call_frame(self, animation: str, direction: float, frame: int, static: bool = False) -> (int, pygame.rect.Rect, pygame.Surface):

        glob = self.global_variable
        sheet = glob["animations"]
        spritesheet = glob["sheet"].copy()
        flipped = [False]

        return_animation = pygame.rect.Rect((0, 0), (0, 0))

        if animation not in glob["animations"]:
            raise KeyError("That animation is not present in this spritesheet")
        else:
            if len(sheet[animation]) > 1:
                # Covers sprite animations with multiple directions
                # Directions not included in the sprite package are assembled by mirroring the opposite direction. Results may vary.
                if direction > -math.pi * 3/4 and direction <= -math.pi * 1/4 and "away" in sheet[animation]:
                    if frame >= len(sheet[animation]["away"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    current_frame = sheet[animation]["away"][frame]
                elif direction > -math.pi * 3/4 and direction <= -math.pi * 1/4 and "away" not in sheet[animation]:
                    if frame >= len(sheet[animation]["towards"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    spritesheet = pygame.transform.flip(
                        spritesheet, False, True)
                    current_frame = sheet[animation]["towards"][frame]
                    flipped = [True, "towards"]
                elif direction < math.pi * 3/4 and direction >= math.pi * 1/4 and "towards" in sheet[animation]:
                    if frame >= len(sheet[animation]["towards"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    current_frame = sheet[animation]["towards"][frame]
                elif direction < math.pi * 3/4 and direction >= math.pi * 1/4 and "towards" not in sheet[animation]:
                    if frame >= len(sheet[animation]["away"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    spritesheet = pygame.transform.flip(
                        spritesheet, False, True)
                    current_frame = sheet[animation]["away"][frame]
                    flipped = [True, "away"]
                elif direction < math.pi * 1/4 and direction >= -math.pi * 1/4 and "right" in sheet[animation]:
                    if frame >= len(sheet[animation]["right"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    current_frame = sheet[animation]["right"][frame]
                elif direction < math.pi * 1/4 and direction >= -math.pi * 1/4 and "right" not in sheet[animation]:
                    if frame >= len(sheet[animation]["left"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    spritesheet = pygame.transform.flip(
                        spritesheet, True, False)
                    current_frame = sheet[animation]["left"][frame]
                    flipped = [True, "left"]
                elif (direction >= math.pi * 3/4 or direction <= -math.pi * 3/4) and "left" in sheet[animation]:
                    if frame >= len(sheet[animation]["left"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    current_frame = sheet[animation]["left"][frame]
                elif (direction >= math.pi * 3/4 or direction <= -math.pi * 3/4) and "left" not in sheet[animation]:
                    if frame >= len(sheet[animation]["right"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    spritesheet = pygame.transform.flip(
                        spritesheet, True, False)
                    current_frame = sheet[animation]["right"][frame]
                    flipped = [True, "right"]
                if not flipped[0]:
                    return_animation = pygame.rect.Rect(
                        (current_frame[0], current_frame[1]), glob["framesize"])
                else:
                    if flipped[1] == "right" or flipped[1] == "left":
                        flipped_frame = (glob["sheet"].get_width(
                        ) / glob["framesize"][0] - 1 - current_frame[0] / glob["framesize"][0]) * glob["framesize"][0]
                        return_animation = pygame.rect.Rect(
                            (flipped_frame, current_frame[1]), glob["framesize"])
                    else:
                        flipped_frame = (glob["sheet"].get_height(
                        ) / glob["framesize"][1] - 1 - current_frame[1] / glob["framesize"][1]) * glob["framesize"][1]
                        return_animation = pygame.rect.Rect(
                            (current_frame[0], flipped_frame), glob["framesize"])
            else:
                # Covers sprites with a single direction by rotating the frame to the 4 cardinal directions
                # Limited to 4 cardinal directions by Pygame, as its rotate function does not do partial rotations well
                direction_name = ""
                for key in sheet[animation].keys():
                    direction_name = key
                current_frame = None
                if direction > math.pi * 3/4 or direction < -math.pi * 3/4:
                    direction = math.pi
                elif direction <= math.pi * 3/4 and direction > math.pi * 1/4:
                    direction = -math.pi * 1/2
                elif direction <= math.pi * 1/4 and direction > -math.pi * 1/4:
                    direction = 0
                else:
                    direction = math.pi * 1/2
                if "away" in sheet[animation]:
                    if frame >= len(sheet[animation]["away"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    if direction < -math.pi / 2:
                        direction += 2 * math.pi
                    current_frame = sheet[animation][direction_name][frame]
                    if not static:
                        spritesheet = spritesheet.subsurface(
                            pygame.rect.Rect(current_frame, glob["framesize"])).copy()
                        spritesheet = pygame.transform.rotate(
                            spritesheet, math.degrees(direction - math.pi * 1 / 2))
                elif "towards" in sheet[animation]:
                    if frame >= len(sheet[animation]["towards"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    if direction < math.pi / 2:
                        direction += 2 * math.pi
                    current_frame = sheet[animation][direction_name][frame]
                    if not static:
                        spritesheet = spritesheet.subsurface(
                            pygame.rect.Rect(current_frame, glob["framesize"])).copy()
                        spritesheet = pygame.transform.rotate(
                            spritesheet, math.degrees(direction - math.pi * 3 / 2))
                elif "right" in sheet[animation]:
                    if frame >= len(sheet[animation]["right"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    current_frame = sheet[animation][direction_name][frame]
                    if not static:
                        spritesheet = spritesheet.subsurface(
                            pygame.rect.Rect(current_frame, glob["framesize"])).copy()
                        spritesheet = pygame.transform.rotate(
                            spritesheet, math.degrees(direction))
                elif "left" in sheet[animation]:
                    if frame >= len(sheet[animation]["left"]) - 1:
                        frame = 0
                    else:
                        frame += 1
                    if direction < 0:
                        direction += 2 * math.pi
                    current_frame = sheet[animation][direction_name][frame]
                    if not static:
                        spritesheet = spritesheet.subsurface(
                            pygame.rect.Rect(current_frame, glob["framesize"])).copy()
                        spritesheet = pygame.transform.rotate(
                            spritesheet, math.degrees(direction - math.pi))
                return_animation = pygame.rect.Rect((0, 0), glob["framesize"])

        return frame, return_animation, spritesheet

    def __getitem__(self, index: str):
        return self.global_variable["animations"][index]

    @property
    def width(self):
        return self.global_variable["framesize"][0]

    @property
    def height(self):
        return self.global_variable["framesize"][1]
