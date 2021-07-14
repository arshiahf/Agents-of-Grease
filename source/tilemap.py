import pygame
import json
import xml.etree.ElementTree as ET
import re
import math

# Class for interpreting a Tiled tilemap file

class Tilemap:

    def __init__(self, filename):
        self.map = {}
        self.map["path"] = filename[:filename.rfind("\\")+1]
        self.map["filename"] = filename
        self.map["file"] = open(self.map["filename"], "r")

        # Default map settings
        self.map["width"] = 50
        self.map["height"] = 50
        self.map["tilewidth"] = 32
        self.map["tileheight"] = 32
        self.map["layers"] = []
        self.map["tilesets"] = []
        self.calculate_size()
        self.read_file_type()

# Convenience functions

    def calculate_size(self):

        total_width = self.map["width"] * self.map["tilewidth"]
        total_height = self.map["height"] * self.map["tileheight"]
        self.map["dimensions"] = (total_width, total_height)

        return None

    def read_file_type(self):

        name = self.map["filename"]
        if (name[name.rfind('.'):]).lower() == ".json":
            self.read_json()
        else:
            self.read_xml()

        return None

    def remove_file(self):
        self.map["file"].close()
        self.map.pop("file")
        self.map.pop("filename")

        return None

    def str_to_int(self, container):
        for item in container:
            if type(container) == type(dict()):
                try:
                    container[item] = int(container[item])
                except TypeError as t:
                    self.str_to_int(container[item])
                except ValueError as e:
                    pass
            else:
                try:
                    item = int(item)
                except TypeError as t:
                    self.str_to_int(item)
                except ValueError as e:
                    pass

        return None

# File interpret functions

    def read_json(self):

        json_data = json.load(self.map["file"])
        self.remove_file()

        # Pull pre-established map statistics from map
        for key in self.map:
            if key == "dimensions" or key == "path":
                continue
            self.map[key] = json_data[key]
        self.calculate_size()

        # Dereference the tileset's json file
        for tileset in self.map["tilesets"]:
            self.map["path_tileset"] = self.map["path"] + tileset["source"][:tileset["source"].rfind("/") + 1]
            tileset_file = open(self.map["path_tileset"] + tileset["source"][tileset["source"].find("/"):], "r")
            tileset_json = json.load(tileset_file)
            tileset["source"] = tileset_json
            tileset_file.close()

        return None

    def read_xml(self):

        xml_data = ET.parse(self.map["file"]).getroot()
        self.remove_file()

        # Pull pre-established map statistics from map
        for key in self.map:
            if key == "dimensions" or key == "path":
                continue
            elif key == "layers":
                for layer in xml_data:
                    if layer.tag == "layer":
                        self.map[key].append(layer.attrib)
                        for child in layer:
                            # Extracts the layer details and turns them into a numerical list
                            child_content_list = []
                            char_list = re.sub('[\s+]', '', child.text).split(',')
                            for character in char_list:
                                character = int(character)
                                child_content_list.append(character)
                            # child_dict = {:}
                            map_location = self.map[key][len(self.map[key]) - 1]
                            map_location[child.tag] = child_content_list
                        if "x" not in map_location.keys():
                            map_location["x"] = 0
                        if "y" not in map_location.keys():
                            map_location["y"] = 0
                continue
            elif key == "tilesets":
                for tileset in xml_data:
                    if tileset.tag == "tileset":
                        tileset_dict = {}
                        for tile_attr in tileset.attrib:
                            if tile_attr != "source":
                                tileset_dict[tile_attr] = tileset.get(tile_attr)
                            else:
                                # Dereferences source file
                                self.map["path_tileset"] = self.map["path"] + tileset.get(tile_attr)[:tileset.get(tile_attr).rfind("/") + 1]
                                tileset_file = open(self.map["path_tileset"] + tileset.get(tile_attr)[tileset.get(tile_attr).find("/"):], "r")
                                tileset_xml = ET.parse(tileset_file).getroot()

                                source_dict = tileset_xml.attrib
                                for child in tileset_xml:
                                    child_dict = child.attrib
                                    source_dict[child.tag] = child_dict
                                tileset_file.close()
                                source_dict["imagewidth"] = source_dict["image"].pop("width")
                                source_dict["imageheight"] = source_dict["image"].pop("height")
                                source_dict["image"] = source_dict["image"].pop("source")
                                if "spacing" not in source_dict:
                                    source_dict["spacing"] = 0
                                tileset_dict[tile_attr] = source_dict
                        self.map[key].append(tileset_dict)
                continue
            elif type(self.map[key]) == int:
                self.map[key] = int(xml_data.attrib[key])
        self.calculate_size()

        # Change layer and tileset numerical values into int type
        self.str_to_int(self.map["layers"])
        self.str_to_int(self.map["tilesets"])

        return None

# Post-interpret functions

    def get_dimensions(self):

        return self.map["dimensions"]

    def draw_map(self):

        for tileset in self.map["tilesets"]:
            tileset["source"]["image"] = pygame.image.load(self.map["path_tileset"] + tileset["source"]["image"]).convert_alpha()
        map_surface = pygame.Surface(self.map["dimensions"])

        for layer in self.map["layers"]:
            local_x, local_y = layer["x"], layer["y"]
            local_width, local_height = layer["width"], layer["height"]
            row = -1
            for column in range(len(layer["data"])):
                if column % self.map["width"] == 0:
                    row += 1
                if row >= self.map["height"]:
                    break

                current_tile = layer["data"][column]

                for tileset in self.map["tilesets"]:
                    if current_tile >= tileset["firstgid"] and current_tile < tileset["source"]["tilecount"] + tileset["firstgid"]:
                        current_tile_spot = (current_tile - tileset["firstgid"]) % tileset["source"]["tilecount"]
                        blit_coords = (local_x + (column % self.map["width"]) * self.map["tilewidth"], local_y + row * self.map["tileheight"])
                        tile_coords_x = (current_tile_spot % tileset["source"]["columns"]) * self.map["tilewidth"] + (current_tile_spot % tileset["source"]["columns"]) * tileset["source"]["spacing"]
                        tile_coords_y = math.floor(current_tile_spot / tileset["source"]["columns"]) * self.map["tileheight"] + math.floor(current_tile_spot / tileset["source"]["columns"]) * tileset["source"]["spacing"]
                        tile_coords = (tile_coords_x, tile_coords_y)
                        map_surface.blit(tileset["source"]["image"], blit_coords, pygame.rect.Rect(tile_coords, (self.map["tilewidth"], self.map["tileheight"])))
                        break



        return map_surface
