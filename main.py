#  id: [type,       inputs, outputs         ]
circuit = {
    0: ["input",    [1,-1], [(1,0),(2,0)]   ],
    1: ["split",    [2],    [(3,0),(4,0)]   ],
    2: ["split",    [2],    [(3,1),(4,1)]   ],
    3: ["min",      [2,2],  [(6,0)]         ],
    4: ["max",      [2,2],  [(5,0)]         ],
    5: ["neg",      [2],    [(6,1)]         ],
    6: ["max",      [2,2],  [(7,0)]         ],
    7: ["out",      [2],    []              ]
    }
custom = {
    "pos": {'0':[1],'+':[1],'-':[2]}
}
tasklist = []

def beginSolve():
    process(circuit[0])
    counter = 0

    while tasklist != []:
        process(circuit[tasklist[0]])
        tasklist.pop(0)

        counter += 1
        if counter>100:
            print("depth reached")
            return


def process(component):
    gate,inputs,destinations = component
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
        
        case "split":
            outputs = [inputs[0]] * len(destinations)

        case "out":
            outputs = []
            for i in range(len(inputs)):
                print(f"output {i}: {inputs[i]}")

        case other:
            if gate[0]!="data":
                outputs = []
                print(f"gate {gate} not found")
                exit()

            if gate[1] in custom:
                inputstring = ''
                for input in inputs:
                    match input:
                        case 1:
                            inputstring += '+'
                        case -1:
                            inputstring += '-'
                        case 0:
                            inputstring += '0'
                outputs = custom[gate[1]][inputstring]

            else:
                #TODO: finding gate from file
                print("finding gates from file not implemented")
                print(f"custom gate {gate[1]} not found")
                outputs = []
                exit()


    for i in range(len(outputs)):
        destination = destinations[i]
        value = outputs[i]

        if circuit[destination[0]][1][destination[1]] == value:
            continue
        circuit[destination[0]][1][destination[1]] = value
        if destination[0] not in tasklist:
            tasklist.append(destination[0])
    




beginSolve()
print(circuit)