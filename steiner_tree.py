import json
import sys
import numpy as np

#Needed functions:
    #Construct graph
    #print graph..for illustration
    
class Cells():
    src: bool
    trg: bool
    block: bool
    empty: bool
    via : bool
    stiener_point: bool
    cost: int

    def  __init__(self,type):
        if type == "empty":
            self.src = False
            self.trg = False
            self.block = False
            self.empty = True
            self.via = False
            self.stiener_point = False
        elif type == "trg":
            self.src = False
            self.trg = True
            self.block = False
            self.empty = False
            self.via = False
            self.stiener_point = False
        elif type == "block":
            self.src = False
            self.trg = False
            self.block = True
            self.empty = False
            self.via = False
            self.stiener_point = False
        elif type == "via":
            self.src = False
            self.trg = False
            self.block = False
            self.empty = False
            self.via = True
            self.stiener_point = False

        #Since we are dealing with consistent costs
        self.cost = 1
        print("I init")



def constructGraph (grid):
    '''
    This function construct the Graph of objects(cells)
    each cell has a state, cost...etc.

    Inputs: grid from JSON file input

    Outputs: Graph (numpy), which is the grid of objects
    '''
    global D,H,W
    # graph = np.random.uniform(low=0, high=10, size=(D,W,H)).astype('uint8')
    # graph = np.zeros([D,W,H])

    #Constructing Grid of Objects:
    vCells = np.vectorize(Cells)
    init_arry = np.arange(D*H*W).reshape((D,W,H))
    graph = np.empty((D,W,H), dtype=object)
    graph[:,:,:] = vCells(init_arry)

    return graph
















if __name__ == "__main__":
    #Global Variables
    D = 0
    W = 0
    H = 0

    # inp = json.load(sys.stdin)
    inp = json.loads('{"grid": [[[0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1], [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]]], "src_coor": [0, 12, 11], "dest_coor": [[0, 7, 4], [0, 14, 12], [0, 6, 8], [0, 0, 1]]}')
    D = len(inp['grid'])
    W = len(inp['grid'][0])
    H = len(inp['grid'][0][0])

    constructGraph(inp['grid'])

    