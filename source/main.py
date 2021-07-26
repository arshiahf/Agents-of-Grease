import application

game_starting_map_folder = "..\\assets\\art\\map\\"
game_starting_map = "level1_tilemap_no_object_layer.json"
game_objects = "object_layout.json"
game_sprites = "..\\assets\\art\\sprites\\"
game_sounds = "..\\assets\\sound\\finished_sounds\\"

app = application.Application(800, 600)
app.pull_sprites(game_sprites)
app.set_map(game_starting_map_folder, game_starting_map)
app.setup_objects(game_starting_map_folder, game_objects)
app.run()
