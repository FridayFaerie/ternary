import pygame, sys
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Ternary Simulator')
icon = pygame.Surface((10,10))
icon.fill((255,255,255))
pygame.display.set_icon(icon)

WINDOW_SIZE = (800,600)
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((400,300))

update_required = False



while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                update_required = True
            elif event.key == K_LEFT:
                update_required = False

    


        
    if update_required:
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE),(0,0))
        pygame.display.update()
        display.fill((80,96,126))
    clock.tick(60)

