#         id: [type,    inputs, outputs         ]
circuit = {0: ["input", [1,-1], [(1,0),(2,0)]   ], 
           1: ["split", [0],    [(3,0),(4,0)]   ],
           2: ["split", [0],    [(3,1),(4,1)]   ],
           3: ["min",   [0,0],  [(6,0)]         ],
           4: ["max",   [0,0],  [(5,0)]         ],
           5: ["neg",   [0],    [(6,1)]         ],
           6: ["max",   [0,0],  [(7,0)]         ],
           7: ["out",   [0],    []              ]
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
    type,inputs,outputs = component
    match type:
        case "input":
            for i in range(len(inputs)):
                output = outputs[i]
                circuit[output[0]][1][output[1]] = inputs[i]
                if output[0] not in tasklist:
                    tasklist.append(output[0])

        case "neg":
            out0 = outputs[0]
            circuit[out0[0]][1][out0[1]] = inputs[0]*-1
            if out0[0] not in tasklist:
                tasklist.append(out0[0])

        case "max":
            out0 = outputs[0]
            circuit[out0[0]][1][out0[1]] = max(inputs[0],inputs[1])
            if out0[0] not in tasklist:
                tasklist.append(out0[0])
        
        case "min":
            out0 = outputs[0]
            circuit[out0[0]][1][out0[1]] = min(inputs[0],inputs[1])
            if out0[0] not in tasklist:
                tasklist.append(out0[0])
        
        case "split":
            for output in outputs:
                circuit[output[0]][1][output[1]] = inputs[0]
                if output[0] not in tasklist:
                    tasklist.append(output[0])

        case "out":
            for i in range(len(inputs)):
                print(f"output {i}: {inputs[i]}")
            return

        case other:
            print(type+" not implemented")




beginSolve()
