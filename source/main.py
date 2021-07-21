import application

game_starting_map = "..\\assets\\art\\map\\"
game_sprites = "..\\assets\\art\\sprites\\"
game_sounds = "..\\assets\\sound\\finished_sounds\\"

app = application.Application(800, 600)
app.pull_sprites(game_sprites)
# app.set_map(game_starting_map)
app.run()
