import pygame, sys
clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('Ternary Simulator')
icon = pygame.Surface((10,10))
icon.fill((255,255,255))
pygame.display.set_icon(icon)


if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass # Windows XP doesn't support monitor scaling, so just do nothing.




#WINDOW_SIZE = (800,400)
WINDOW_SIZE = (1600,800)
BACKGROUND_COLOUR = (40,36,56)
GATE_WIDTH = 130
PORT_RADIUS = 7
screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
display = pygame.Surface((1600,800))

update_required = True
active_gate = None
active_port_in = None
active_port_out = None
tasklist = []

input = {
    0: ["input",    [1,0],  [(1,0),(2,0)],   [50,300] ],
    1: ["split",    None,    [(3,0),(4,0)],   [200,200]],
    2: ["split",    None,    [(3,1),(4,1)],   [200,400]],
    3: ["min",      None,  [(6,0)],         [350,500]],
    4: ["max",      None,  [(5,0)],         [350,300]],
    5: ["neg",      None,    [(6,1)],         [500,300]],
    6: ["max",      None,  [(-1,0)],        [650,300]],
    -1:["out",      None,    [],              [800,300]]
    }
colours = {
    -1: (255,0,0),
    0:  (150,150,150),
    1:  (0,0,255),
    2:  (0,0,0)
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

class Component:
    def __init__(self, id, argument):
        self.gate_type, values, self.destinations, position = argument
        self.id = id
        self.rect = pygame.Rect(position,(GATE_WIDTH, gate_styles[self.gate_type][0]))
        self.wires = []
        self.sources = []
        if values != None:
            self.values = values
        else:
            self.values = [2] * gate_styles[self.gate_type][1]

    def update_outports(self): #updates destination gates' sources
        for num, destination in enumerate(self.destinations):
            circuit[destination[0]].sources.append((self.id, num))

    def update_gate(self):
        gate_style = gate_styles[self.gate_type]
        inputs = self.values
        match self.gate_type:
            case "input":
                outputs = [None] * gate_style[1]
                for i in range(gate_style[1]):
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
                if self.gate_type in custom_gates:
                    inputstring = ''
                    for input in inputs:
                        match input:
                            case 1:
                                inputstring += '+'
                            case -1:
                                inputstring += '-'
                            case 0:
                                inputstring += '0'
                    outputs = custom_gates[self.gate_type][inputstring]

                else:
                    print(f"gate {self.gate_type} not found")
                    #TODO: finding gate from file
                    print("finding gates from file not implemented")
                    exit()

        for i in range(gate_styles[self.gate_type][2]):
            destination = self.destinations[i]
            value = outputs[i]

            if circuit[destination[0]].values[destination[1]] == value:
                continue
            else:
                circuit[destination[0]].values[destination[1]] = value
            if destination[0] not in tasklist:
                tasklist.append(destination[0])
    
    def render(self):
        gate_style = gate_styles[self.gate_type]
        match self.gate_type:
            case "input":
                return
            # case "out":
            #     return
            case other:
                font = pygame.font.Font(None, 32)
                pygame.draw.rect(display,gate_style[3],self.rect,border_radius=5)
                text = font.render(self.gate_type, True, (10, 10, 10))
                textpos = text.get_rect(centerx=(self.rect.width/2)+self.rect[0], centery=(self.rect.height/2)+self.rect[1])
                display.blit(text, textpos)

        for i in range(gate_style[1]):
            colour = colours[self.values[i]]
            origin, *_, end = self.wires[i]

            # pygame.draw.circle(display, colour, end, PORT_RADIUS)
            pygame.draw.rect(display,colour,pygame.Rect(end[0]-PORT_RADIUS,end[1]-PORT_RADIUS,PORT_RADIUS*2,PORT_RADIUS*2),border_radius=3)

            pygame.draw.lines(display, colour, False, self.wires[i],5)
            # pygame.draw.circle(display, colour, start, PORT_RADIUS)
            pygame.draw.rect(display,colour,pygame.Rect(origin[0]-PORT_RADIUS,origin[1]-PORT_RADIUS,PORT_RADIUS*2,PORT_RADIUS*2),border_radius=3)

    def update_wires(self):
        gate_style = gate_styles[self.gate_type]
        if self.sources == []:
            return
        input_height = gate_style[0]/gate_style[1]
        if not self.wires:
            for i in range(gate_style[1]):
                self.wires.append([None,None])
        for i in range(gate_style[1]):
            print(self.id, i)
            source_component = circuit[self.sources[i][0]]
            source_style = gate_styles[source_component.gate_type]
            source_height = source_style[0]/source_style[2]
            self.wires[i][0] = (source_component.rect[0]+GATE_WIDTH-2*PORT_RADIUS,source_component.rect[1]+(self.sources[i][1]+0.5)*source_height)
            self.wires[i][-1] = (self.rect[0]+PORT_RADIUS,self.rect[1]+(i+0.5)*input_height)

#inports collision
                            # spacing = gate_style[0]/gate_style[1]
                            # for port in component.ports:
                            #     if abs(rel_y-int(spacing*(port+0.5)))<PORT_RADIUS+1:
                            #         active_port_in = port


def process(circuit):
    if not tasklist:
        circuit[0].update_gate()
    
    counter = 0
    while tasklist:
        circuit[tasklist[0]].update_gate()
        tasklist.pop(0)

        counter += 1
        if counter > 100:
            print("max cycles exceeded")
            break
        
'''
def update_gate_outports(component, destination, num):
    if not destination:
        return
    
    gate_style = gate_styles[component[0]]
    origin = (component[3][0]+GATE_WIDTH-PORT_RADIUS, component[3][1]+(gate_style[0]/gate_style[2])*(num+0.5))
    

    gate_rect = circuit[destination[0]][3]
    destination_style = gate_styles[circuit[destination[0]][0]]
    input_height = destination_style[0]/destination_style[1]
    end = (gate_rect[0]+PORT_RADIUS, gate_rect[1]+destination[1]*input_height+input_height//2)

    circuit[destination[0]][4][destination[1]][1] = [origin,end]

def update_gate_inports(component):
    for num,input in enumerate(component[4]):
        gate_style = gate_styles[component[0]]
        source = circuit[input[0][0]]
        source_style = gate_styles[source[0]]
        input[1][0] = (source[3][0]+GATE_WIDTH-PORT_RADIUS, source[3][1]+(source_style[0]/source_style[2])*(num+0.5))
        input[1][-1] = (component[3][0]+PORT_RADIUS, component[3][1]+gate_style[0]/gate_style[1]*(num+0.5))


def check_collision(a,b):
    return False




        
'''


circuit = {}
for item in input:
    circuit[item] = Component(item, input[item])
for component in circuit:
    circuit[component].update_outports()
for component in circuit:
    circuit[component].update_wires()

process(circuit)

# for component in circuit:
#     print(circuit[component])

while True:
    #event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                continue
            elif event.key == K_LEFT:
                continue
        if event.type == MOUSEBUTTONUP:
            if active_port_in != None:
                for component in circuit:
                    if component.main_collision(event.pos) and event.pos[0]<component.rect[0]+PORT_RADIUS*2:
                        port = component.inports_collision(event.pos)
                        if port != None:
                            component.modify_inport(port, circuit[active_gate].sources[active_port_in])
                            port = None


            active_gate = None
            active_port_in = None
            active_port_out = None

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:

                for component in circuit:
                    if component.main_collision(event.pos):
                        active_gate = component.id

                        if event.pos[0]<component.rect[0]+PORT_RADIUS*2:
                            active_port_in = component.inports_collision(event.pos)

                        elif event.pos[0]>component.rect[0]+GATE_WIDTH-PORT_RADIUS*2:
                            active_port_out = component.outports_collision(event.pos)

        
        if event.type == MOUSEMOTION:
            if active_port_in != None:
                circuit[active_gate].wires[active_port_in][-1] = event.pos
                print(f"TODO: in {active_port_in}")
            elif active_port_out != None:
                print(f"TODO: out {active_port_out}")
            elif active_gate != None:
                circuit[active_gate].update_movement(event.rel) #rect.move_ip

#{-1: ['out', [0], [], <rect(975, 473, 130, 40)>, [[(6, 0), []]]]}


    #render components on display
    for component in circuit:
        circuit[component].render()
            
        


        
    if update_required:
        screen.blit(pygame.transform.scale(display, WINDOW_SIZE),(0,0))
        #screen.blit(display,(0,0))
        pygame.display.update()
        display.fill(BACKGROUND_COLOUR)
    clock.tick(60)
