##########
# Created by: Adam Fast
# Last updated: June 12th, 2024
# Title: Turtle Beach
# Description: Use lightning to protect some turtles eggs until they hatch! Watch out for lizards!
##########

# Instructions:
# Your goal is to protect your eggs from the elements (and lizards)!
# You can control lightning to heat up your eggs or fry the lizards
# After 30 days, your eggs will be counted and you will receive a score
# Monitor the temperature of your eggs closely or they will die! (Eggs will die above 60 degrees or below 10 degrees!)
# Egg temperature indicators turn blue if a male will hatch or pink for a female (or red if at an extreme temperature!)

# Controls:
# Space bar activates heat vision (allows you to see the temperature of the eggs)
# Left click creates a lightning circle, release the button to unleash lightning!

import math
import datetime
import pygame
import random
from DynamicThings import Egg, Tide, Moon, Lightning, Lizard, SpriteRenderer
import Settings

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
framerate = 60

Settings.gamestate = 0

endstate = 0

egglist = []

tide = Tide(400, 100)

moon = Moon(400, 85)

turndisplay = SpriteRenderer("egg1.png", (25, 25), 50, 50)

bolt = False

back = pygame.image.load("back1.png")

global allobj, heatobj, lizardobj


def StartGame():
    global allobj, heatobj, lizardobj
    Settings.gamestate = 1

    starteggs = 50
    if Settings.debug:
        starteggs = 1
    for i in range(starteggs):
        x = random.randint(60, 740)
        y = random.randint(210, 440)

        if Settings.debug:
            x = 400
            y = 200

        egglist.append(Egg(x, y))

    allobj = [moon] + [tide] + egglist
    heatobj = [tide] + [tide.secondone] + egglist

    lizardobj = []


StartGame()


def CreateLizard(pos):
    thislizard = Lizard(pos[0], pos[1])
    allobj.append(thislizard)
    lizardobj.append(thislizard)
    heatobj.append(thislizard)


def DestroyObj(i):
    allobj.remove(i)
    if i in heatobj:
        heatobj.remove(i)
    if i in egglist:
        egglist.remove(i)
    if i in lizardobj:
        lizardobj.remove(i)


running = True
while running:
    Settings.mousepos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Settings.gamestate == 1:
                    # CreateLizard((random.randint(20, 780), 625))
                    Settings.heatview = not Settings.heatview
                elif Settings.gamestate == 2:
                    endstate += 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                bolt = Lightning(Settings.mousepos[0], Settings.mousepos[1])
                allobj.append(bolt)
                heatobj.append(bolt)
        elif event.type == pygame.MOUSEBUTTONUP:
            if not pygame.mouse.get_pressed()[0]:
                if bolt:
                    bolt.stage = 1

    screen.fill((0, 0, 0))

    # Main menu
    if Settings.gamestate == 0:
        pass

    # Regular Gameplay state
    elif Settings.gamestate == 1:

        if len(egglist) == 0:
            males = 0
            females = 0
            finalscore = 0
            rank = "regular"
            rankcolour = (0, 0, 0)
            Settings.gamestate = 2

        # Currently the game will last for 4.15 minutes
        Settings.gametime += 1 * Settings.gamespeed
        if Settings.gametime % 500 == 0:
            Settings.gamedays += 1
            Settings.weather = random.uniform(Settings.weatherrange[0], Settings.weatherrange[1])
            if Settings.gamedays >= 31:
                Settings.gamedays = 30
                males = 0
                females = 0
                rank = "regular"
                rankcolour = (0, 0, 0)
                for i in egglist:
                    if i.gender == "male":
                        males += 1
                    elif i.gender == "female":
                        females += 1
                    elif i.gender == "unknown":
                        if males >= females:
                            females += 1
                        else:
                            males += 1
                theratio = math.gcd(males, females)
                if theratio == 0 or males == 0 or females == 0:
                    finalscore = 0
                else:
                    finalscore = (int(round((1 / (males / theratio) / (females / theratio)) * len(egglist), 0)) * 2 +
                                  (len(egglist) * 15))

                if 200 < finalscore <= 599:
                    rank = "bronze"
                    rankcolour = (130, 110, 35)
                elif 600 < finalscore <= 799:
                    rank = "silver"
                    rankcolour = (153, 174, 194)
                elif finalscore >= 800:
                    rank = "gold"
                    rankcolour = (167, 155, 36)

                scoretext = open("TURTLESCORE", "a")
                scoretext.write(f"{"#" * 25} \nGame played at {datetime.datetime.now()} "
                                f"\nTurtles saved: {len(egglist)} \nMale turtles: {males} \n"
                                f"Female turtles: {females} \nFinal score: {finalscore}\nRank achieved: {rank.upper()} "
                                f"\n{"#" * 25} \n")
                scoretext.close()
                Settings.gamestate = 2

            for d in range(int(Settings.gamedays / 2)):
                CreateLizard((random.randint(20, 780), 625))

        screen.blit(back, (0, 0))

        for a in egglist:
            screen.blit(a.image, (a.x, a.y))

        if lizardobj:
            for l in lizardobj:
                screen.blit(l.image, (l.x, l.y))
                if l.y <= 500:
                    deadegg = l.FindEgg(list(egglist))
                    if deadegg:
                        DestroyObj(deadegg)
                        DestroyObj(l)

        for i in allobj:
            objcommand = i.Update()
            if objcommand == "delete":
                DestroyObj(i)
                if i == tide:
                    tide = False
                if i == bolt:
                    bolt = False

        for h in heatobj:
            # If the object receives heat
            if h.mode == 1:
                for b in heatobj:
                    # If the object is giving heat
                    if b == h:
                        h.temp += (Settings.weather - b.temp) / 1000
                    if b.mode == 0:
                        if h == tide:
                            print("tide")
                        h.temp += h.UpdateTemp(h.temp, h.mode, h.pos, b)

        Settings.mooncycle = math.sin(Settings.gametime / 7500) * 125

        screen.blit(tide.image, (tide.x, tide.y))
        if Settings.debug:
            pygame.draw.circle(screen, (255, 255, 50), (tide.pos[0], tide.pos[1]), tide.heattravel, 0)
            pygame.draw.circle(screen, (255, 255, 50), (tide.secondone.pos[0], tide.secondone.pos[1]),
                               tide.secondone.heattravel, 0)

        screen.blit(moon.image, (moon.x, moon.y))

        textcolour = (0, 0, 0)
        if Settings.gamedays == 30:
            textcolour = (255, 0, 0)

        turntext = turndisplay.WriteText(f"day {Settings.gamedays}", textcolour, 30)
        screen.blit(turntext[0], turntext[1])

        if bolt:
            screen.blit(bolt.image, (bolt.x, bolt.y))
            if Settings.debug:
                pygame.draw.circle(screen, (255, 0, 0), (bolt.pos[0], bolt.pos[1]), bolt.heattravel, 1)

        if Settings.heatview:
            for i in egglist:
                eggtext = i.WriteText(str(round(i.temp)), i.colour, 20)
                screen.blit(eggtext[0], eggtext[1])
                if Settings.debug:
                    pygame.draw.circle(screen, (0, 255, 0), (i.pos[0], i.pos[1]), i.size[0] / 2, 1)

    # Game end
    elif Settings.gamestate == 2:
        # endstate things:
        # 0 = starting thing
        # 1 = eggs saved
        # 2 = male / female eggs
        # 3 = final score
        # 4 = close game

        screen.blit(back, (0, 0))
        turndisplay = SpriteRenderer("egg1.png", (25, 25), 50, 50)
        turntext = turndisplay.WriteText(f"day {Settings.gamedays}", (255, 0, 0), 30)
        screen.blit(turntext[0], turntext[1])

        if endstate == 0:
            # print("game over")

            text1display = SpriteRenderer("egg1.png", (25, 25), 250, 500)
            text1 = text1display.WriteText(f"press space to continue", (0, 0, 0), 30)
            screen.blit(text1[0], text1[1])

            for a in egglist:
                screen.blit(a.image, (a.x, a.y))
            pass

        elif endstate == 1:
            screen.blit(text1[0], text1[1])

            text2display = SpriteRenderer("egg1.png", (25, 25), 250, 225)
            text2 = text2display.WriteText(f"you saved {len(egglist)} / 50 eggs", (0, 0, 0), 30)
            screen.blit(text2[0], text2[1])

        elif endstate == 2:
            screen.blit(text1[0], text1[1])

            screen.blit(text2[0], text2[1])

            text3display = SpriteRenderer("egg1.png", (25, 25), 225, 275)
            text3 = text3display.WriteText(f"you created {males} male turtles", (0, 0, 255), 30)
            screen.blit(text3[0], text3[1])

            text4display = SpriteRenderer("egg1.png", (25, 25), 215, 325)
            text4 = text4display.WriteText(f"you created {females} female turtles", (255, 120, 200), 30)
            screen.blit(text4[0], text4[1])

        elif endstate == 3:
            screen.blit(text2[0], text2[1])
            screen.blit(text3[0], text3[1])
            screen.blit(text4[0], text4[1])

            text5display = SpriteRenderer("egg1.png", (25, 25), 250, 375)
            text5 = text5display.WriteText(f"your final score is {finalscore}", rankcolour, 30)
            screen.blit(text5[0], text5[1])

            text1display = SpriteRenderer("egg1.png", (25, 25), 190, 500)
            text1 = text1display.WriteText(f"press space to close the game", (0, 0, 0), 30)
            screen.blit(text1[0], text1[1])

        elif endstate == 4:
            running = False

    clock.tick(framerate)
    pygame.display.flip()

pygame.quit()
