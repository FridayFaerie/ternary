#!/usr/bin/python3
import pygame
from sys import exit

#this is a test
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('sim')

circuit = {'in1': ['heyo'], 'in2': ['hi']}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    for i in circuit:
        print(circuit[i])


    pygame.display.update()
