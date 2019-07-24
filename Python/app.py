import pygame
from pygame.sprite import Group

from settings import Settings
from intro import GUI, Button
import serial
import time

arduino1 = serial.Serial('COM11', 115200, timeout=0)

settings = Settings()
logo = Group()
gui = GUI()

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
pygame.display.set_caption('NeuroArmWrestling')

b1 = Button((settings.screen_width // 2 - 120, settings.screen_height // 2 - 150, 400, 100), 'start')
b2 = Button((settings.screen_width // 2 - 345, settings.screen_height // 2 + 220, 400, 100), 'exit')
gui.add_element(b1)
gui.add_element(b2)

cursor = pygame.sprite.Sprite()
cursor.image = pygame.transform.scale(pygame.image.load("arrow.png"), (50, 50))
cursor.rect = cursor.image.get_rect()
pygame.mouse.set_visible(False)

running1 = True
running2 = True
account1 = 0
account2 = 0
round = 1
now = 0
i = 3
x1 = 0
x2 = 0
x3 = 0
power1 = 0
power2 = 0
flag = 2
flag1 = True


def screen_1():
    global running1, running2

    clock = pygame.time.Clock()
    while running1:
        screen.fill((255, 204, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.get_event(event):
                    running2 = True
                    running1 = False
                    gui.delete_start()
                if b2.get_event(event):
                    running1 = False
                    running2 = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            gui.get_event(event)
        gui.render(screen)
        logo.draw(screen)
        gui.update()
        if pygame.mouse.get_focused():
            screen.blit(cursor.image, cursor.rect)
        clock.tick(120)
        pygame.display.flip()


def screen_2():
    global running1, running2, account1, account2, round, now, i, x1, x2, x3, power1, power2, flag, flag1

    arduino1.flushInput()
    arduino1.flushOutput()
    k1 = True
    k2 = True
    amplitude1 = 0
    amplitude2 = 0

    clock = pygame.time.Clock()
    while running2:
        for j in arduino1.readall():
            if k1:
                amplitude1 = j
                k1 = False
            elif k2:
                amplitude2 = j
                k2 = False
            if j == 0:
                k1 = True
            elif j == 1:
                k2 = True

        screen.fill((255, 204, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running1 = False
                running2 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b2.get_event(event):
                    running1 = False
                    running2 = False
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos
            gui.get_event(event)

        if round < 4:
            fontObj = pygame.font.Font('freesansbold.ttf', 60)
            textSurfaceObj = fontObj.render('{} раунд'.format(round), True, (0, 0, 0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (150, 50)
            screen.blit(textSurfaceObj, textRectObj)

            accObj = pygame.font.Font('freesansbold.ttf', 60)
            accSurfaceObj = accObj.render('{} : {}'.format(account1, account2), True, (0, 0, 0))
            accRectObj = accSurfaceObj.get_rect()
            accRectObj.center = (150, 150)
            screen.blit(accSurfaceObj, accRectObj)

            if i != 0:
                fontObj = pygame.font.Font('freesansbold.ttf', 60)
                textSurfaceObj = fontObj.render('{}'.format(i), True, (0, 0, 0))
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (350, 350)
                screen.blit(textSurfaceObj, textRectObj)

            if flag == 2:
                x1 = time.clock()
                flag = 1
            elif flag == 1:
                if i > 0:
                    if time.clock() - x1 >= 1:
                        i -= 1
                        flag = 2
                elif i == 0:
                    i = 'GO!'
                    flag = 0
                    x2 = time.clock()

            if time.clock() - x2 >= 10 and flag == 0:
                if power1 > power2:
                    now = 1
                    account1 += 1
                    flag1 = True
                elif power2 > power1:
                    now = 2
                    account2 += 1
                    flag1 = True

                power1 = 0
                power2 = 0
                pygame.draw.rect(screen, (255, 204, 0), pygame.Rect((150, 310, 400, 90)))

                if round != 3:
                    fontObj = pygame.font.Font('freesansbold.ttf', 60)
                    textSurfaceObj = fontObj.render('Player {} won!'.format(now), True, (0, 0, 0))
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (350, 350)
                    screen.blit(textSurfaceObj, textRectObj)

                    if flag1:
                        x3 = time.clock()
                        flag1 = False
                    if time.clock() - x3 >= 5:
                        i = 3
                        flag = 2
                        round += 1
                else:
                    round += 1

            elif time.clock() - x2 < 10 and flag == 0:
                if amplitude1 > amplitude2:
                    power1 += 1
                elif amplitude1 < amplitude2:
                    power2 += 1
        else:
            win = 0
            if account1 > account2:
                win = 1
            else:
                win = 2

            fontObj = pygame.font.Font('freesansbold.ttf', 60)
            textSurfaceObj = fontObj.render('Сongratulate Player {}!'.format(win), True, (0, 0, 0))
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (350, 350)
            screen.blit(textSurfaceObj, textRectObj)

            accObj = pygame.font.Font('freesansbold.ttf', 70)
            accSurfaceObj = accObj.render('{} : {}'.format(account1, account2), True, (0, 0, 0))
            accRectObj = accSurfaceObj.get_rect()
            accRectObj.center = (350, 200)
            screen.blit(accSurfaceObj, accRectObj)

        gui.render(screen)
        logo.draw(screen)
        gui.update()
        if pygame.mouse.get_focused():
            screen.blit(cursor.image, cursor.rect)
        clock.tick(120)
        pygame.display.flip()


screen_1()
screen_2()
