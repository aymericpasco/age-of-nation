# -*- coding: utf-8 -*-

VERSION = "0.10"

# Valeurs de points de statistiques initiales : 10/2
SCORE_MAX = 200
CARD_MAX = 27
MULTIPLICATOR = int(SCORE_MAX/10)

INIT_ECONOMY_PTS = int(SCORE_MAX/2)
INIT_ENVIRONMENT_PTS = int(SCORE_MAX/2)
INIT_PEOPLE_PTS = int(SCORE_MAX/2)
INIT_MILITARY_PTS = int(SCORE_MAX/2)


def initScore():
    return [INIT_ECONOMY_PTS, INIT_ENVIRONMENT_PTS, INIT_PEOPLE_PTS, INIT_MILITARY_PTS]

# X --- Y
SCREEN_SIZE = [1280, 720]

SIZE_CARD = [400, 400]
SIZE_TEXTBOX = [700, 118]
SIZE_ACCEPT_DENY = [270, 100]
ACCEPT_DENY_TO_CENTER = 25

POSITIONS_CARD = [SCREEN_SIZE[0]/2-SIZE_CARD[0]/2, SCREEN_SIZE[1]/2-SIZE_CARD[1]/2]
POSITIONS_ACCEPT = [SCREEN_SIZE[0]-SIZE_ACCEPT_DENY[0]-ACCEPT_DENY_TO_CENTER, SCREEN_SIZE[1]/2-SIZE_ACCEPT_DENY[1]/2]
POSITIONS_REFUSE = [ACCEPT_DENY_TO_CENTER, SCREEN_SIZE[1]/2-SIZE_ACCEPT_DENY[1]/2]
POSITIONS_TEXTBOX = [SCREEN_SIZE[0]/2-SIZE_TEXTBOX[0]/2, SCREEN_SIZE[1]-SIZE_TEXTBOX[1]]

# try:
import pygame
import pygame.font
from pygame.locals import *
import xml.etree.ElementTree as xml
import os

class TextRectException:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise ("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

            # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise ("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface

def loadImage(imgName):
    fullName = os.path.join('incl/img', imgName)
    image = pygame.image.load(fullName).convert_alpha()
    return image

def initIcons(screen, menu):
    if menu is False:
        iconEconomy = loadImage('money.png')
        screen.blit(iconEconomy, (125, 10))

        iconEnvironment = loadImage('environment.png')
        screen.blit(iconEnvironment, (125, 40))

        iconPeople = loadImage('people.png')
        screen.blit(iconPeople, (125, 70))

        iconMilitary = loadImage('tank.png')
        screen.blit(iconMilitary, (125, 100))

    elif menu is True:
        iconTitle = loadImage('title.png')
        screen.blit(iconTitle, (356, 40))

        iconTitle = loadImage('menu/logo-epsi.png')
        screen.blit(iconTitle, (20, 600))

def initSprites(screen, menu):
    if menu is False:
        background = loadImage('back-earth.png')
        screen.blit(background, (0, 0))

        spriteCard = loadImage('card.png')
        screen.blit(spriteCard, (POSITIONS_CARD[0], POSITIONS_CARD[1]))

        spriteTextBox = loadImage('textbox.png')
        screen.blit(spriteTextBox, (POSITIONS_TEXTBOX[0], POSITIONS_TEXTBOX[1]))

        spriteAccept = loadImage('accept.png')
        screen.blit(spriteAccept, (POSITIONS_ACCEPT[0], POSITIONS_ACCEPT[1]))

        spriteRefuse = loadImage('deny.png')
        screen.blit(spriteRefuse, (POSITIONS_REFUSE[0], POSITIONS_REFUSE[1]))

    elif menu is True:
        menuback = loadImage('back-menu.png')
        screen.blit(menuback, (0, 0))

        iconStart = loadImage('menu/new-game.png')
        screen.blit(iconStart, (420, 290))

        iconHelp = loadImage('menu/help.png')
        screen.blit(iconHelp, (420, 370))

        iconCredits = loadImage('menu/credits.png')
        screen.blit(iconCredits, (420, 450))

def initRender(screen, menu):
    initSprites(screen, menu)
    initIcons(screen, menu)
    pygame.display.flip()

def viewMenu(screen, indiceMenu):
    if indiceMenu == 1:
        background = loadImage('help.png')
        screen.blit(background, (0, 0))
    elif indiceMenu == 2:
        background = loadImage('credits.png')
        screen.blit(background, (0, 0))

card_data = xml.parse('incl/data-2.xml').getroot()

class Card:
    def __init__(self, step):

        self.date = card_data[step][0].text     # Year of card
        self.content = card_data[step][2].text # Text content of the card

        self.yes_answer = card_data[step][3].text  # Text content of choice "yes"/"accept"
        self.no_answer = card_data[step][4].text   # Text content of choice "no"/"refuse"

        # In order : [ Economy - Environment - People - Military ]
        self.yes_effects = [int(card_data[step][5][0][0].text), int(card_data[step][5][0][1].text),
                            int(card_data[step][5][0][2].text), int(card_data[step][5][0][3].text)]
        self.no_effects = [int(card_data[step][5][1][0].text), int(card_data[step][5][1][1].text),
                           int(card_data[step][5][1][2].text), int(card_data[step][5][1][3].text)]
        self.image = card_data[step][6].text

def avoidOverProgress(score):
    if score[0] > 200:
        score[0] = 200
    if score[1] > 200:
        score[1] = 200
    if score[2] > 200:
        score[2] = 200
    if score[2] > 200:
        score[2] = 200
    if score[3] > 200:
        score[3] = 200

def checkLose(score):
    if score[0] == 0 or score[1] == 0 or score[2] == 0 or score[3] == 0:
        return True
    else:
        return False

def updateScore(actualScore, answer, step):
    multiple = MULTIPLICATOR
    if answer == 1:
        cardEffects = Card(step).yes_effects
    elif answer == 0:
        cardEffects = Card(step).no_effects
    updatedCardEffects = [x * multiple for x in cardEffects]
    result = [x + y for x, y in zip(actualScore, updatedCardEffects)]
    avoidOverProgress(result)
    return result

def updateRenderCard(card, screen, menu):
    if menu is False:
        defineFontBox = pygame.font.Font('incl/font/jf-flat-regular.ttf', 15)
        boxContent = card.content
        boxRect = pygame.Rect((307, 618, 666, 90))
        renderedBox = render_textrect(boxContent, defineFontBox, boxRect, (173, 166, 145), (255, 255, 255), 0)

        defineFontDate = pygame.font.Font("incl/font/jf-flat-regular.ttf", 60)
        dateContent = card.date
        dateRect = pygame.Rect((1050, 30, 140, 80))
        renderedDate = render_textrect(dateContent, defineFontDate, dateRect, (173, 166, 145), (255, 250, 235), 0)


        imageCard = loadImage(card.image)
        screen.blit(imageCard, (POSITIONS_CARD[0], POSITIONS_CARD[1]))

        if renderedBox:
            screen.blit(renderedBox, boxRect.topleft)
        if renderedDate:
            screen.blit(renderedDate, dateRect.topleft)

def updateRenderResponse(card, screen, answer):
    defineFontBox = pygame.font.Font("incl/font/jf-flat-regular.ttf", 20)

    imageCard = loadImage("card.png")
    screen.blit(imageCard, (POSITIONS_CARD[0], POSITIONS_CARD[1]))

    if answer == 1:
        response = card.yes_answer
    else:
        response = card.no_answer

    responseContent = response
    responseRect = pygame.Rect((450, 170, 380, 380))
    renderedResponseBox = render_textrect(responseContent, defineFontBox, responseRect, (173, 166, 145), (255, 255, 255), 0)

    boxContent = "Appuyez sur ESPACE pour continuer."
    boxRect = pygame.Rect((307, 618, 666, 90))
    renderedBox = render_textrect(boxContent, defineFontBox, boxRect, (173, 166, 145), (255, 255, 255), 0)

    if renderedResponseBox:
        screen.blit(renderedResponseBox, responseRect.topleft)
    if renderedBox:
        screen.blit(renderedBox, boxRect.topleft)

def updateRenderScore(score, screen, menu):
    if menu is False:
        pygame.draw.rect(screen, (236, 231, 217), pygame.Rect(175, 18, 200, 8))
        pygame.draw.rect(screen, (236, 231, 217), pygame.Rect(175, 48, 200, 8))
        pygame.draw.rect(screen, (236, 231, 217), pygame.Rect(175, 78, 200, 8))
        pygame.draw.rect(screen, (236, 231, 217), pygame.Rect(175, 108, 200, 8))

        pygame.draw.rect(screen, (173, 166, 145), pygame.Rect(175, 18, score[0], 8))
        pygame.draw.rect(screen, (173, 166, 145), pygame.Rect(175, 48, score[1], 8))
        pygame.draw.rect(screen, (173, 166, 145), pygame.Rect(175, 78, score[2], 8))
        pygame.draw.rect(screen, (173, 166, 145), pygame.Rect(175, 108, score[3], 8))
        pygame.display.flip()

def onGame(step, score):
    if score[0] == 0 or score[1] == 0 or score[2] == 0 or score[3] == 0:
        return False
    elif step == 27:
        return False
    else:
        return True

def winGame(screen):
    background = loadImage('back-end.png')
    screen.blit(background, (0, 0))

def loseGame(screen):
    background = loadImage('back-lose.png')
    screen.blit(background, (0, 0))




def main():
    # Initialise screen
    pygame.init()

    icon = pygame.image.load('incl/img/transparant-icon.png')
    pygame.display.set_icon(icon)

    pygame.mixer.init()
    bo = pygame.mixer.Sound("incl/sound/bo.ogg")
    switch = pygame.mixer.Sound("incl/sound/switch.ogg")
    bo.play().set_volume(0.1)


    screen = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
    pygame.display.set_caption('Age of Nation')

    menu = True
    initRender(screen, menu)


    card_number = 0
    card = Card(card_number)
    score = initScore()


    waiting = False
    boucle = True
    game = True
    lose = False
    indiceMenu = 0

    # Event loop
    while boucle:

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and menu is True:
                if event.key == pygame.K_SPACE and indiceMenu == 0:
                    menu = False
                    initRender(screen, menu)
                    updateRenderCard(card, screen, menu)
                if event.key == pygame.K_h and indiceMenu == 0:
                    indiceMenu = 1
                    viewMenu(screen, indiceMenu)
                if event.key == pygame.K_c and indiceMenu == 0:
                    indiceMenu = 2
                    viewMenu(screen, indiceMenu)
                if event.key == pygame.K_SPACE and (indiceMenu == 1 or indiceMenu == 2):
                    indiceMenu = 0
                    initRender(screen, menu)
            elif event.type == KEYDOWN and (game is False or lose is True):
                if event.key == pygame.K_RETURN:
                    score = initScore()
                    card_number = 0
                    initRender(screen, menu)
                    waiting = False
            elif event.type == KEYDOWN and (game and lose is False):
                if waiting:
                    if event.key == pygame.K_SPACE:
                        card_number = card_number + 1
                        waiting = False
                else:
                    if event.key == pygame.K_LEFT:
                        answer = 0
                        switch.play().set_volume(0.2)
                        score = updateScore(score, answer, card_number)
                        waiting = True
                    if event.key == pygame.K_RIGHT:
                        answer = 1
                        switch.play().set_volume(0.2)
                        score = updateScore(score, answer, card_number)
                        waiting = True

        game = onGame(card_number, score)

        if game is False:
            if checkLose(score) is True:
                loseGame(screen)
            else:
                winGame(screen)
        else:
            updateRenderScore(score, screen, menu)
            if waiting:
                updateRenderResponse(card, screen, answer)
            else:
                updateRenderCard(card, screen, menu)
            card = Card(card_number)

        pygame.display.flip()

if __name__ == '__main__': 
    main()