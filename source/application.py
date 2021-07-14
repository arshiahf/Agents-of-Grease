import sprite
import tilemap
import pygame

class Application():

    def __init__(self, width, height):

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

    def pull_sprites(self, sprite_list):

        g = self.global_variable
        g["sprites"] = {}


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

    def get_input(self):

        g = self.global_variable

        all_keys = pygame.key.get_pressed()
        all_events = pygame.event.get()
        all_mouse = pygame.mouse.get_pressed()

        for event in all_events:
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and all_keys[pygame.K_ESCAPE]:
                g["done"] = True

        return None

    def draw(self):

        g = self.global_variable

        g["screen"]["window"].fill(g["screen"]["fill_color"])


        pygame.display.flip()

        return None

    def update(self):

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        self.get_input()
        self.draw()

        pygame.event.pump()

        return None

    def run(self):

        g = self.global_variable
        g["time"]["delta_time"] = g["time"]["clock"].tick()

        while not g["done"]:

            self.update()

            continue

        pygame.quit()

        return None
