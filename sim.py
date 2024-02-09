#!/usr/bin/python3
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))

circuit = {'in1': ['heyo'], 'in2': ['hi']}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    for i in circuit:
        print(circuit[i])
