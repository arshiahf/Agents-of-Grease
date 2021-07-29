import sprite
import tilemap
import pygame
import player
import plat
import os
import json
import vector
import projectile
import random
import enemy


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
        g["time"]["enemy_timer_base"] = 2.5
        g["time"]["enemy_timer"] = g["time"]["enemy_timer_base"]

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
        Squirt_sound = "..\\assets\\sound\\finished_sounds\\bottle_squirt.mp3"

        pygame.mixer.init()
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
        new_plat = plat.Platform(x, y, sprite=plat_sprite)
        self.global_variable["objects"]["platforms"].append(new_plat)

    def light_fire(self, x: float, y: float, fire_sprite: sprite.Sprite):
        fire = plat.Platform(
            x, y, default_action="fullBurn", sprite=fire_sprite)
        self.global_variable["fire"] = fire

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

    def spawn_enemy(self, x_pos: float, y_pos: float):

        g = self.global_variable
        enemy_sprites = g["sprites"]["manager"]["enemies"]
        size = random.choice(["small", "small", "small", "big"])
        if size == "big":
            new_enemy = enemy.Enemy(
                x_pos, y_pos, "bigStand", enemy_sprites, size, 3.0)
        else:
            new_enemy = enemy.Enemy(
                x_pos, y_pos, "smallStand", enemy_sprites, size)

        # new_enemy.change_target(g["objects"]["fire"])
        new_enemy.change_target(g["fire"])
        g["objects"]["enemies"].append(new_enemy)

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

        g["fire"].update(g["time"]["delta_time"], g["screen"]["window"])

        for platform in g["objects"]["platforms"]:
            platform.update(g["time"]["delta_time"], g["screen"]["window"])

        for enem in g["objects"]["enemies"]:
            if not enem.update(g["time"]["delta_time"], g["screen"]["window"]):
                g["objects"]["enemies"].remove(enem)

        for must in g["projectiles"]["mustard"]:
            if must.global_variable["dead"]:
                g["projectiles"]["mustard"].remove(must)
                continue
            if must.pos.x <= 0 or must.pos.x + must.spr.width >= g["screen"]["dimensions"][0]:
                must.splat()
            must.update(g["time"]["delta_time"], g["screen"]["window"])

        for ketch in g["projectiles"]["ketchup"]:
            if ketch.global_variable["dead"]:
                g["projectiles"]["ketchup"].remove(ketch)
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

        for enemy_object in g["objects"]["enemies"]:
            if g["player"].collide(enemy_object) and enemy_object.size == "big":
                g["player"].hurt(enemy_object.knockback, enemy_object)

        for plat_object in g["objects"]["platforms"]:
            if not g["player"].collide(plat_object):
                g["player"].restore_grav()
            else:
                break

        for enemy_object in g["objects"]["enemies"]:
            for plat_object in g["objects"]["platforms"]:
                if not enemy_object.collide(plat_object):
                    enemy_object.restore_grav()
                else:
                    break
            if enemy_object.collide(g["fire"]):
                g["objects"]["enemies"].remove(enemy_object)
                if g["fire"].global_variable["animation"]["default_action"] == "fullBurn":
                    g["fire"].global_variable["animation"]["default_action"] = "lowBurn"
                elif g["fire"].global_variable["animation"]["default_action"] == "lowBurn":
                    g["fire"].global_variable["animation"]["default_action"] = "extinguished"
                    g["done"] = True
                    break

        for enemy_object in g["objects"]["enemies"]:
            for ketchup in g["projectiles"]["ketchup"]:
                if enemy_object.collide(ketchup) and not ketchup.is_splatted():
                    enemy_object.hurt("ketchup", g["player"])
                    ketchup.splat()
                    break
            for mustard in g["projectiles"]["mustard"]:
                if enemy_object.collide(mustard) and not mustard.is_splatted():
                    enemy_object.hurt("mustard", g["player"])
                    mustard.splat()
                    break
            if enemy_object.pos.y >= g["screen"]["dimensions"][1]:
                enemy_object.global_variable["health"] = 0

        if g["time"]["enemy_timer"] > 0:
            g["time"]["enemy_timer"] -= g["time"]["delta_time"]
        else:
            g["time"]["enemy_timer"] = g["time"]["enemy_timer_base"]
            x_pos = random.randint(
                int(g["screen"]["dimensions"][0] * 1 / 6), int(g["screen"]["dimensions"][0] * 1 / 2))
            y_pos = random.randint(
                int(g["screen"]["dimensions"][1] * 1 / 8), int(g["screen"]["dimensions"][1] * 3 / 8))
            self.spawn_enemy(x_pos, y_pos)

        if g["player"].pos.y + g["player"].spr.width * 3 / 4 >= g["screen"]["dimensions"][1]:
            g["done"] = True

        self.get_input()
        self.draw()

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

            g["fire"].update(g["time"]["delta_time"], g["screen"]["window"])

            for plat in range(len(g["objects"]["platforms"])):
                g["objects"]["platforms"][plat].update(
                    g["time"]["delta_time"], g["screen"]["window"])

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

            end_timer -= g["time"]["delta_time"]
            pygame.display.flip()
            pygame.event.pump()

        return None

    def run(self) -> None:

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        self.make_player(g["screen"]["center"][0], g["screen"]["center"]
                         [1] - 75, "standGun", g["sprites"]["manager"]["hotdog"])

        fire_sprite = g["sprites"]["manager"]["fire_extinguish"]
        self.light_fire(g["screen"]["dimensions"][0] - fire_sprite.width,
                        g["screen"]["dimensions"][1] - fire_sprite.height, fire_sprite)

        while not g["done"]:

            self.update()

        self.game_end()

        pygame.quit()

        return None
