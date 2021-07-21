import sprite
import tilemap
import pygame
import player
import os

class Application:

    def __init__(self, width:int, height:int) -> None:

        self.global_variable = {}
        g = self.global_variable

        g["screen"] = {}
        g["screen"]["dimensions"] = (width, height)
        g["screen"]["center"] = (g["screen"]["dimensions"][0] / 2, g["screen"]["dimensions"][1] / 2)
        g["screen"]["fill_color"] = pygame.color.Color((200, 200, 200))
        g["screen"]["window"] = pygame.display.set_mode(g["screen"]["dimensions"])

        g["time"] = {}
        g["time"]["clock"] = pygame.time.Clock()
        g["time"]["delta_time"] = g["time"]["clock"].tick()

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

    def set_map(self, map_file):

        g = self.global_variable
        g["map"] = {}
        map = g["map"]
        map["tilemap"] = tilemap.Tilemap(map_file)
        map["dimensions"] = map["tilemap"].get_dimensions()
        map["image"] = map["tilemap"].draw_map()
        map["location"] = (0, 0)

        return None

    def make_player(self, player_sprite):

        g = self.global_variable

        g["player"] = player.Player(g["screen"]["center"][0], g["screen"]["center"][1], "standGun", player_sprite, 0.15, base_speed=0.15)

        return None

    def get_input(self):

        g = self.global_variable

        all_keys = pygame.key.get_pressed()
        all_events = pygame.event.get()
        all_mouse = pygame.mouse.get_pressed()

        for event in all_events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and all_keys[pygame.K_ESCAPE]:
                g["done"] = True

            if event.type == pygame.KEYDOWN:
                if all_keys[pygame.K_SPACE] and g["player"].get_animation() != "jump":
                    g["player"].move(y_adjust = -2.5)
                if event.key == pygame.K_a:
                    g["player"].move(x_adjust = -2.5)
                if event.key == pygame.K_d:
                    g["player"].move(x_adjust = 2.5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    g["player"].move(x_adjust = 2.5)
                if event.key == pygame.K_d:
                    g["player"].move(x_adjust = -2.5)



        return None

    def draw(self):

        g = self.global_variable

        g["screen"]["window"].fill(g["screen"]["fill_color"])
        g["player"].update(g["time"]["delta_time"], g["screen"]["window"])


        pygame.display.flip()

        return None

    def update(self):

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick() / 1000

        self.get_input()
        self.draw()

        pygame.event.pump()

        return None

    def run(self) -> None:

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        self.make_player(g["sprites"]["manager"]["hotdog"])

        while not g["done"]:

            self.update()

            continue

        pygame.quit()

        return None
