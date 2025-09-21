import math
import random

import pygame
import Settings

pygame.font.init()


class TempMeasure:
    def __init__(self, temp, mode, pos, heattravel, width):
        self.temp = temp
        self.mode = mode
        self.pos = pos
        self.heattravel = heattravel
        self.width = width
        # Modes:
        # 0 = give
        # 1 = recieve

    def UpdateTemp(self, temp, mode, pos, target):
        self.temp = temp
        self.mode = mode
        self.pos = pos
        if self.mode == 1:
            if target.mode == 0:
                pos1 = (self.pos[0], self.pos[1])
                pos2 = (target.pos[0], target.pos[1])
                distance = ((pos1[1] - pos2[1]) ** 2 + (pos1[0] - pos2[0]) ** 2) ** (1 / 2)
                if target.heattravel >= distance:
                    final = (target.temp - self.temp) / 1000
                    pass
                else:
                    final = 0
                return final

        return


class SpriteRenderer:
    def __init__(self, image, size, x, y):
        self.image = pygame.image.load(image)
        self.size = size
        self.x = x - size[0] / 2
        self.y = y - size[1] / 2
        self.image = pygame.transform.scale(self.image, size)
        self.colour = (0, 0, 0)

    def UpdatePicture(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, self.size)

    def WriteText(self, words, colour, size):
        mainfont = pygame.font.Font('freesansbold.ttf', size)
        return [mainfont.render(words, False, colour), (self.x, self.y)]

        pass


class Egg(SpriteRenderer, TempMeasure):
    def __init__(self, startx, starty):
        SpriteRenderer.__init__(self, "egg1.png", (25, 25), startx, starty)
        self.temp = 29.35
        self.gender = "unknown"
        self.mode = 1
        self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
        self.heattravel = 0
        self.width = (self.size[0] / 2, self.size[1] / 2)

    def GetGender(self):
        if self.temp <= 27.7:
            self.gender = "male"
            self.colour = (0, 0, 255)
            if self.temp <= 15:
                self.colour = (255, 0, 0)
        elif self.temp >= 31:
            self.gender = "female"
            self.colour = (255, 120, 200)
            if self.temp >= 50:
                self.colour = (255, 0, 0)
        else:
            self.gender = "unknown"
            self.colour = (0, 0, 0)
        return self.gender

    def Update(self):
        self.GetGender()
        self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
        if self.temp <= 10 or self.temp >= 60:
            return "delete"


class Tide(SpriteRenderer, TempMeasure):
    def __init__(self, startx, starty):
        SpriteRenderer.__init__(self, "tide1.png", (800, 600), startx, starty)
        self.temp = 13.6
        self.mode = 0
        self.pos = (self.x + self.size[0] / 4, self.y + 65)
        self.heattravel = 215
        self.width = (self.size[0] / 2, self.size[1] / 2)
        self.secondone = TempMeasure(self.temp, self.mode, (self.x + self.size[0] / 1.4, self.pos[1]), self.heattravel, self.width)

    def Update(self):
        self.y = (- math.cos(Settings.gametime / 50)) * Settings.mooncycle - 75
        self.secondone.y = self.y + 65
        self.pos = (self.x + self.size[0] / 4, self.y + 65)
        self.secondone.pos = (self.secondone.pos[0], self.y + 65)


class Moon(SpriteRenderer):
    def __init__(self, startx, starty):
        SpriteRenderer.__init__(self, "moon.png", (100, 100), startx, starty)
        self.time = 0

    def Update(self):
        pass


class Lightning(SpriteRenderer, TempMeasure):
    def __init__(self, startx, starty):
        SpriteRenderer.__init__(self, "lightning.png", (5, 5), startx, starty)
        self.temp = 0
        self.mode = 0
        self.pos = (self.x, self.y)
        self.heattravel = 0
        self.width = (self.size[0] / 2, self.size[1] / 2)
        
        self.strength = 0
        self.stage = 0
        self.lifespan = 10
        # Stages:
        # 0 = charging
        # 1 = release
        # 2 = decline
        # 3 = max charge, but not released

    def Update(self):
        if self.stage == 0:
            if self.strength >= 200:
                self.stage = 3
                return
            self.size = (self.size[0] + 3, self.size[1] + 3)
            self.width = (self.size[0] / 2, self.size[1] / 2)
            self.x = Settings.mousepos[0] - self.size[0] / 2
            self.y = Settings.mousepos[1] - self.size[1] / 2
            self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
            self.UpdatePicture("lightning.png")
            self.strength = self.size[0]
        elif self.stage == 1:
            self.temp = 250 + self.strength * 10 + Settings.gamedays * 2
            self.heattravel = self.size[0] / 2
            self.width = (self.size[0] / 2, self.size[1] / 2)
            self.UpdatePicture("bolt.png")
            self.stage = 2
        elif self.stage == 2:
            self.lifespan -= 1
            if self.lifespan <= 0:
                return "delete"
        elif self.stage == 3:
            self.x = Settings.mousepos[0] - self.size[0] / 2
            self.y = Settings.mousepos[1] - self.size[1] / 2
            self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
            self.UpdatePicture("lightning.png")
            pass


class Lizard(SpriteRenderer, TempMeasure):
    def __init__(self, startx, starty):
        SpriteRenderer.__init__(self, "lizard.png", (25, 25), startx, starty)
        self.temp = random.randint(15, 22)
        self.mode = 1
        self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
        self.heattravel = 0
        self.width = (self.size[0] / 2, self.size[1] / 2)
        self.lifespan = 20

    def FindEgg(self, eggs):
        if eggs:
            target = eggs[0]
            pos1 = (self.pos[0], self.pos[1])
            pos2 = (target.pos[0], target.pos[1])
            distance = ((pos1[1] - pos2[1]) ** 2 + (pos1[0] - pos2[0]) ** 2) ** (1 / 2)
            if distance <= 25:
                return target
            else:
                eggs.remove(target)
                return self.FindEgg(eggs)
        else:
            return False

    def Update(self):
        if self.temp >= 30:
            self.temp = 1000
            self.image = "lizard2.png"
            self.UpdatePicture("lizard2.png")
            self.lifespan -= 1
            if self.lifespan <= 0:
                return "delete"
            return
        if self.y <= 170:
            return "delete"
        self.y -= random.uniform(0, self.temp / 35)
        self.pos = (self.x + self.size[0] / 2, self.y + self.size[1] / 2)
