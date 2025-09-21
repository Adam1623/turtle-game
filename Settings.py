from random import uniform
global gamespeed, gamestate, gametime, gamedays, mooncycle, weather, weatherrange, debug, heatview, mousepos
debug = False
gamespeed = 1
if debug:
    gamespeed = 1
gamestate = 1
heatview = False
gametime = 0
gamedays = 1
mooncycle = 0
weatherrange = (0.2, 25.5)
mousepos = (0, 0)
if debug:
    weatherrange = (10, 10.01)
weather = uniform(weatherrange[0], weatherrange[1])
