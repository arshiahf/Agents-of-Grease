import sprite
import tilemap
import pygame
import player
import platform
import os
import json
import vector
import projectile
import random


class Application:

    def __init__(self, width: int, height: int) -> None:

        self.global_variable = {}
        g = self.global_variable

        g["screen"] = {}
        g["screen"]["dimensions"] = (width, height)
        g["screen"]["center"] = (
            g["screen"]["dimensions"][0] / 2, g["screen"]["dimensions"][1] / 2)
        g["screen"]["fill_color"] = pygame.color.Color((200, 200, 200))
        g["screen"]["window"] = pygame.display.set_mode(
            g["screen"]["dimensions"])
        g["time"] = {}
        g["time"]["clock"] = pygame.time.Clock()
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        g["error"] = {}
        g["error"]["keys"] = {}
        g["error"]["keys"]["a"] = False
        g["error"]["keys"]["d"] = False

        g["projectiles"] = {}
        g["projectiles"]["ketchup"] = []
        g["projectiles"]["mustard"] = []

        g["done"] = False

        pygame.init()

    def pull_sounds(self, sounds_path):

        g = self.global_variable
        g["sounds"] = {}

        return None

    def pull_sprites(self, sprites_path):

        g = self.global_variable
        g["sprites"] = {}
        g["sprites"]["manager"] = sprite.Sprite_Manager()

        for sprite_file in os.listdir(sprites_path):
            if sprite_file.endswith(".json"):
                g["sprites"]["manager"].load_sprite(sprites_path, sprite_file)

        return None

    def set_map(self, map_folder: str, map_file: str):

        g = self.global_variable
        g["map"] = {}
        map = g["map"]
        map["tilemap"] = tilemap.Tilemap(map_folder + map_file)
        map["dimensions"] = map["tilemap"].get_dimensions()
        map["image"] = map["tilemap"].draw_map()
        map["location"] = (0, 0)

        return None

    def make_player(self, x: float, y: float, current_action, player_sprite: sprite.Sprite):

        g = self.global_variable

        g["player"] = player.Player(x, y, current_action, player_sprite,
                                    0.15, base_speed=0.15)

        return None

    def make_platform(self, x: float, y: float, plat_sprite: sprite.Sprite):
        plat = platform.Platform(x, y, sprite=plat_sprite)
        self.global_variable["objects"]["platforms"].append(plat)

    def setup_objects(self, folder_name: str, filename: str):

        try:
            temp_file = open(folder_name + filename, "r")
        except FileNotFoundError:
            print("File does not exist")
            return None

        g = self.global_variable

        g["objects"] = {}
        g["objects"]["platforms"] = []
        g["objects"]["enemies"] = []

        objects_spots = json.load(temp_file)
        temp_file.close()

        for object_type in objects_spots:
            if object_type == "platform":
                for plat in objects_spots[object_type]:
                    for location in objects_spots[object_type][plat]:
                        self.make_platform(
                            location[0], location[1], g["sprites"]["manager"][plat])

        return None

    def get_input(self):

        g = self.global_variable

        all_keys = pygame.key.get_pressed()
        all_events = pygame.event.get()
        all_mouse = pygame.mouse.get_pressed()

        for event in all_events:

            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and all_keys[pygame.K_ESCAPE]:
                g["done"] = True
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if g["player"].get_animation() != "jump" and g["player"].get_animation() != "jumpGun":
                        g["player"].move(y_adjust=-2.5)
                if event.key == pygame.K_a and not g["error"]["keys"]["a"]:
                    g["player"].move(x_adjust=-2.5)
                    g["error"]["keys"]["a"] = True
                if event.key == pygame.K_d and not g["error"]["keys"]["d"]:
                    g["player"].move(x_adjust=2.5)
                    g["error"]["keys"]["d"] = True
                if event.key == pygame.K_s:
                    if g["player"].get_animation() != "jump" and g["player"].get_animation() != "jumpGun":
                        player_pos = g["player"].pos
                        player_pos.y += 6
                        g["player"].pos = player_pos

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if g["player"].jumping():
                        g["player"].global_variable["movement"]["vector_y_adjust"] = 0.0
                if event.key == pygame.K_a and g["error"]["keys"]["a"]:
                    g["player"].move(x_adjust=2.5)
                    g["error"]["keys"]["a"] = False
                if event.key == pygame.K_d and g["error"]["keys"]["d"]:
                    g["player"].move(x_adjust=-2.5)
                    g["error"]["keys"]["d"] = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if all_mouse[0]:
                    mouse_location = pygame.mouse.get_pos()
                    mouse_vector = vector.Vector2(
                        mouse_location[0], mouse_location[1])
                    mouse_vector.x -= g["player"].spr.width * 1 / 2
                    g["player"].face(g["player"].direction(mouse_vector))
                    g["player"].shoot()
                    player_y = g["player"].pos.y + \
                        g["player"].spr.height * 1 / 3
                    if mouse_vector.x <= g["player"].pos.x:
                        player_x = g["player"].pos.x + \
                            g["player"].spr.width * 1 / 8
                        mouse_vector.x = -g["screen"]["dimensions"][0]
                    else:
                        player_x = g["player"].pos.x + \
                            g["player"].spr.width * 7 / 8
                        mouse_vector.x = 2 * g["screen"]["dimensions"][0]
                    projectile_type = random.choice(["ketchup", "mustard"])
                    mouse_vector.y = player_y
                    new_proj = projectile.Projectile(
                        player_x, player_y, mouse_vector, projectile_type, sprite=g["sprites"]["manager"]["projectiles"], splat_sprite=g["sprites"]["manager"]["projectiles_splats"])
                    if projectile_type == "ketchup":
                        g["projectiles"]["ketchup"].append(new_proj)
                    elif projectile_type == "mustard":
                        g["projectiles"]["mustard"].append(new_proj)

            return None

    def draw(self):

        g = self.global_variable

        g["screen"]["window"].fill(g["screen"]["fill_color"])
        g["screen"]["window"].blit(g["map"]["image"], g["map"]["location"])

        for plat in range(len(g["objects"]["platforms"])):
            g["objects"]["platforms"][plat].update(
                g["time"]["delta_time"], g["screen"]["window"])

        mustard_limit = len(g["projectiles"]["mustard"])
        mustard = 0
        if mustard_limit > 0:
            while mustard < mustard_limit:
                must = g["projectiles"]["mustard"][mustard]
                mustard += 1
                if must.global_variable["dead"]:
                    g["projectiles"]["mustard"].remove(must)
                    mustard -= 1
                    mustard_limit -= 1
                    continue
                if must.pos.x <= 0 or must.pos.x + must.spr.width >= g["screen"]["dimensions"][0]:
                    must.splat()
                must.update(g["time"]["delta_time"], g["screen"]["window"])

        ketchup_limit = len(g["projectiles"]["ketchup"])
        ketchup = 0
        if ketchup_limit > 0:
            while ketchup < ketchup_limit:
                ketch = g["projectiles"]["ketchup"][ketchup]
                ketchup += 1
                if ketch.global_variable["dead"]:
                    g["projectiles"]["ketchup"].remove(ketch)
                    ketchup -= 1
                    ketchup_limit -= 1
                    continue
                if ketch.pos.x <= 10 or ketch.pos.x + ketch.spr.width >= g["screen"]["dimensions"][0] - 10:
                    ketch.splat()
                ketch.update(g["time"]["delta_time"], g["screen"]["window"])

        g["player"].update(g["time"]["delta_time"], g["screen"]["window"])

        pygame.display.flip()

        return None

    def update(self):

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick() / 1000

        self.get_input()
        self.draw()

        for other_object in range(len(g["objects"]["enemies"])):
            if g["player"].collide(g["objects"]["enemies"][other_object]):
                g["player"].global_variable["animation"]["current_action"] = "hurt"
                g["objects"]["enemies"][other_object].global_variable["animation"]["current_action"] = "attack"

        for other_object in range(len(g["objects"]["platforms"])):
            if not g["player"].collide(g["objects"]["platforms"][other_object]):
                g["player"].restore_grav()
            else:
                break

        if g["player"].pos.y + g["player"].spr.width * 3 / 4 >= g["screen"]["dimensions"][1]:
            g["done"] = True

        pygame.event.pump()

        return None

    def game_end(self):

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick() / 1000
        glob = g["player"].global_variable
        glob["animation"]["current_action"] = "die"
        glob["frame"] = 0
        glob["animation"]["timer"] = glob["animation"]["timer_base"]
        end_timer = 3

        while end_timer > 0:
            g["screen"]["window"].fill(g["screen"]["fill_color"])
            g["screen"]["window"].blit(g["map"]["image"], g["map"]["location"])
            g["time"]["delta_time"] = g["time"]["clock"].tick() / 1000
            if glob["frame"] < 1:
                if glob["animation"]["timer"] > 0:
                    glob["animation"]["timer"] -= g["time"]["delta_time"]
                    glob["frame"] -= 1
                    g["player"].animate(glob["animation"]["current_action"],
                                        g["screen"]["window"], glob["animation"]
                                        ["current_face"])
                else:
                    glob["animation"]["timer"] = glob["animation"]["timer_base"]
                    g["player"].animate(glob["animation"]["current_action"],
                                        g["screen"]["window"], glob["animation"]
                                        ["current_face"])
            else:
                glob["animation"]["timer"] -= g["time"]["delta_time"]
                glob["frame"] -= 1
                g["player"].animate(glob["animation"]["current_action"],
                                    g["screen"]["window"], glob["animation"]
                                    ["current_face"])

            for plat in range(len(g["objects"]["platforms"])):
                g["objects"]["platforms"][plat].update(
                    g["time"]["delta_time"], g["screen"]["window"])

            end_timer -= g["time"]["delta_time"]
            pygame.display.flip()
            pygame.event.pump()

        return None

    def run(self) -> None:

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        self.make_player(g["screen"]["center"][0], g["screen"]["center"]
                         [1] - 75, "standGun", g["sprites"]["manager"]["hotdog"])

        while not g["done"]:

            self.update()

        self.game_end()

        pygame.quit()

        return None
