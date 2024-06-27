import pygame, sys
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Ternary Simulator')
icon = pygame.Surface((10,10))
icon.fill((255,255,255))
pygame.display.set_icon(icon)


WINDOW_SIZE = (800,400)
#WINDOW_SIZE = (1600,800)
BACKGROUND_COLOUR = (40,36,56)
GATE_WIDTH = 130
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((1600,800))

update_required = True

colours = {
    -1: (255,0,0),
    0:  (150,150,150),
    1:  (0,0,255),
    2:  (0,0,0)
}
circuit = {
    0: ["input",    [1,0],  [(1,0),(2,0)],   [50,300]   ],
    1: ["split",    [2],    [(3,0),(4,0)],   [200,200]   ],
    2: ["split",    [2],    [(3,1),(4,1)],   [200,400]   ],
    3: ["min",      [2,2],  [(6,0)],         [350,500]  ],
    4: ["max",      [2,2],  [(5,0)],         [350,300]  ],
    5: ["neg",      [2],    [(6,1)],         [500,300]  ],
    6: ["max",      [2,2],  [(-1,0)],        [650,300]  ],
    -1:["out",      [2],    [],              [800,300]  ]
    }
wires = {
    0: [[], (0,0), (1,0)],
    1: [[], (0,1), (2,0)],
    2: [[], (1,0), (3,0)],
    3: [[], (1,1), (4,0)],
    4: [[], (2,0), (3,1)],
    5: [[], (2,1), (4,1)],
    6: [[], (3,0), (6,0)],
    7: [[], (4,0), (5,0)],
    8: [[], (5,0), (6,1)],
    9: [[], (6,0), (-1,0)]
}
custom_gates = {
    "pos": {'0':[1],'+':[1],'-':[2]}
}
gate_styles = { #height, input#, output#, colour
    "input":    [80,2,2,(123,74,195)],
    "split":    [80,1,2,(100,100,195)],
    "min":      [80,2,1,(200,150,230)],
    "max":      [80,2,1,(140,240,195)],
    "neg":      [40,1,1,(90,190,90)],
    "out":      [40,1,0,(190,90,90)]
}
tasklist = []

def process(circuit, tasklist):
    if not tasklist:
        update_gate(circuit, tasklist, 0)
    
    counter = 0
    while tasklist:
        update_gate(circuit, tasklist, tasklist[0])
        tasklist.pop(0)

        counter += 1
        if counter > 100:
            print("max cycles exceeded")
            break

def update_gate(circuit, tasklist, component=0):
    gate,inputs,destinations,*_ = circuit[component]
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
            #print(outputs)
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
        if destination[0] not in tasklist:
            tasklist.append(destination[0])

'''  id: [gate,    inputs, destinations,   position  ]
gates_mul = {
    0: ["input",    [1,0],  [(1,0),(2,0)],   [0,0]   ],
'''

def render(component):
    gate, inputs, destinations, position = component
    match gate:
        # case "input":
        #     return
        # case "out":
        #     return
        case other:
            gate_style = gate_styles[gate]

            main_rect = pygame.Rect(position,(GATE_WIDTH,gate_style[0]))

            font = pygame.font.Font(None, 32)
            pygame.draw.rect(display,gate_style[3],main_rect,border_radius=5)
            text = font.render(gate, True, (10, 10, 10))
            textpos = text.get_rect(centerx=(main_rect.width/2)+position[0], centery=(main_rect.height/2)+position[1])
            display.blit(text, textpos)

    
    input_height = gate_style[0]/gate_style[1]
    for i in range(gate_style[1]):
        x=position[0]
        y=position[1]+i*input_height+input_height//2
        colour = colours[inputs[i]]
        pygame.draw.circle(display, colour, (x,y), 7)

def render_wire(wire):
    path, source, destination = wire
    source_gate = circuit[source[0]]
    destination_gate = circuit[destination[0]]
    source_style = gate_styles[source_gate[0]]
    destination_style = gate_styles[destination_gate[0]]

    colour = colours[destination_gate[1][destination[1]]]
    start = [(source_gate[3][0]+GATE_WIDTH, source_gate[3][1]+int((source_style[0]/source_style[2])*(source[1]+0.5)))]
    end = [(destination_gate[3][0],         destination_gate[3][1]+int((destination_style[0]/destination_style[1])*(destination[1]+0.5)))]

    pygame.draw.lines(display, colour, False, start+path+end,10)
    pygame.draw.circle(display, colour, start[0], 7)

process(circuit,tasklist)
while True:
    #event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                update_required = True
            elif event.key == K_LEFT:
                update_required = False

    #render components on display
    for component in circuit:
        render(circuit[component])
    for wire in wires:
        render_wire(wires[wire])
        


        
    if update_required:
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE),(0,0))
        #screen.blit(display,(0,0))
        pygame.display.update()
        display.fill(BACKGROUND_COLOUR)
    clock.tick(60)

'''
#  id: [gate,       inputs, destinations,   origins, positions  ]
gates_mul = {
    0: ["input",    [1,0],  [(1,0),(2,0)],   [0,0]   ],
    1: ["split",    [2],    [(3,0),(4,0)],   [0,0]   ],
    2: ["split",    [2],    [(3,1),(4,1)],   [0,0]   ],
    3: ["min",      [2,2],  [(6,0)],         [0,0]   ],
    4: ["max",      [2,2],  [(5,0)],         [0,0]   ],
    5: ["neg",      [2],    [(6,1)],         [0,0]   ],
    6: ["max",      [2,2],  [(-1,0)],        [0,0]   ],
    -1:["out",      [2],    [],              [0,0]   ]
    }
custom_gates = {
    "pos": {'0':[1],'+':[1],'-':[2]}
}

circuitA = Circuit(gates_mul)
circuitA.process()
print(circuitA.gates)

'''