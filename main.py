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

custom_gates = {
    "pos": {'0':[1],'+':[1],'-':[2]}
}

def process(circuit):
    if not circuit["tasklist"]:
        update_gate(circuit)
    
    counter = 0
    while circuit["tasklist"]:
        update_gate(circuit, circuit["tasklist"][0])
        circuit["tasklist"].pop(0)

        counter += 1
        if counter > 100:
            print("max cycles exceeded")
            break

def update_gate(circuit, component=0):
    gate,inputs,destinations = circuit[component]
    match gate:
        case "input":
            size = len(inputs)
            outputs = [None] * size
            for i in range(size):
                outputs[i] = inputs[i]
        case "neg":
            outputs = [inputs[0]*-1]
        case "max":
            outputs = [max(inputs[0],inputs[1])]          
        case "min":
            outputs = [min(inputs[0],inputs[1])]          
        case "wire":
            outputs = [inputs[0]]
        case "split":
            outputs = [inputs[0],inputs[0]]
        case "out":
            outputs = []
            print(outputs)
        case other:
            if gate in custom_gates:
                inputstring = ''
                for input in inputs:
                    match input:
                        case 1:
                            inputstring += '+'
                        case -1:
                            inputstring += '-'
                        case 0:
                            inputstring += '0'
                outputs = custom_gates[gate][inputstring]

            else:
                print(f"gate {gate} not found")
                #TODO: finding gate from file
                print("finding gates from file not implemented")
                exit()

    for i in range(len(outputs)):
        destination = destinations[i]
        value = outputs[i]

        if circuit[destination[0]][1][destination[1]] == value:
            continue
        else:
            circuit[destination[0]][1][destination[1]] = value
        if destination[0] not in circuit["tasklist"]:
            circuit["tasklist"](destination[0])





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

'''
#  id: [type,       inputs, destinations,   origins, positions  ]
gates_mul = {
    0: ["input",    [1,0],  [(1,0),(2,0)],   [],        [0,0]   ],
    1: ["split",    [2],    [(3,0),(4,0)],   [0],       [0,0]   ],
    2: ["split",    [2],    [(3,1),(4,1)],   [0],       [0,0]   ],
    3: ["min",      [2,2],  [(6,0)],         [1,2],     [0,0]   ],
    4: ["max",      [2,2],  [(5,0)],         [1,2],     [0,0]   ],
    5: ["neg",      [2],    [(6,1)],         [4],       [0,0]   ],
    6: ["max",      [2,2],  [(-1,0)],        [3,5],     [0,0]   ],
    -1:["out",      [2],    [],              [6],       [0,0]   ]
    }
custom_gates = {
    "pos": {'0':[1],'+':[1],'-':[2]}
}

circuitA = Circuit(gates_mul)
circuitA.process()
print(circuitA.gates)

'''