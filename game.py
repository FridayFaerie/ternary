import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()
pygame.display.set_caption('Ternary Simulator')

WINDOW_SIZE = (600,400)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((300,200))

while True:
    display.fill((146,244,255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                continue


    pygame.display.update()
    clock.tick(60)


