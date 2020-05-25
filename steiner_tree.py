import json
import sys
import numpy as np


#Needed functions:
    #print graph..for illustration
    
#Colors
# Black = '\u001b[30m'
Red = '\u001b[31m'
Green = "\u001b[32m"
Yellow = '\u001b[33m'
Blue = '\u001b[34m'
Reset = "\u001b[0m" 

class Cells():
    src: bool
    trg: bool
    block: bool
    empty: bool
    via : bool
    stiener_point: bool
    cost: int
    value: int

    def  __init__(self,id):
        if id == 0:
            #Empty
            self.src = False
            self.trg = False
            self.block = False
            self.empty = True
            self.via = False
            self.stiener_point = False
            #Since we are dealing with consistent costs
            self.cost = 1
            self.value = id
        elif id == 1:
            #Block
            self.src = False
            self.trg = False
            self.block = True
            self.empty = False
            self.via = False
            self.stiener_point = False
            #Since we are dealing with consistent costs
            self.cost = 0
            self.value = id
        elif id == 2:
            #Via
            self.src = False
            self.trg = False
            self.block = False
            self.empty = True
            self.via = False
            self.stiener_point = False
            #Since we are dealing with consistent costs
            self.cost = 1
            self.value = id
        

    def specifySrc (self):
        self.src = True
        self.empty = False
        self.value = 3

    def specifyTrg (self):
        self.trg = True
        self.empty = False
        self.value = 4
    




#Functions:

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
    # init_arry = np.arange(D*H*W).reshape((D,W,H))
    init_arry = grid
    graph = np.empty((D,W,H), dtype=object)
    graph[:,:,:] = vCells(init_arry)

    return graph




def assignSource(myG, dim):
    myG[dim[0]][dim[1]][dim[2]].specifySrc()
    return

def assignTarget(myG, dim):
    myG[dim[0]][dim[1]][dim[2]].specifyTrg()
    return

def initDimensions(grid):
    return len(inp['grid']) , len(inp['grid'][0]) , len(inp['grid'][0][0])
    

def initGrid (inp):
    #constructing the Grid of objects
    myG = constructGraph(inp['grid'])
    #assign the source
    assignSource(myG , inp['src_coor'])
    #assign the targets (terminals)
    for target in (inp['dest_coor']):
        assignTarget(myG, target)
    return myG


def printGrid (graph):
    '''
    Lack of coloring..TODO
    '''
    global D,W,H
    for layer in range(D):
        print (f'Data of Layer {layer}\n')
        for j in range(W):
            for i in range(H):
                if graph[layer][j][i].value == 0:
                    #Empty..white
                    print (Reset + str(graph[layer][j][i].value), end="\t")
                elif graph[layer][j][i].value == 1:
                    #block..red
                    print (Red + str(graph[layer][j][i].value), end="\t")
                elif graph[layer][j][i].value == 2:
                    #Via..yellow
                    print (Yellow + str(graph[layer][j][i].value), end="\t")
                elif graph[layer][j][i].value == 3:
                    #Source..blue
                    print (Blue + str(graph[layer][j][i].value), end="\t")
                elif graph[layer][j][i].value == 4:
                    #Target..
                    print (Green + str(graph[layer][j][i].value), end="\t")
            print ("\n")
        print (Reset)



if __name__ == "__main__":
    #Global Variables
    D = 0
    W = 0
    H = 0

    # inp = json.load(sys.stdin)
    inp = json.loads('{"grid": [[[0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1], [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]]],\
        "src_coor": [0, 12, 11], "dest_coor": [[0, 7, 4], [0, 14, 12], [0, 6, 8], [0, 0, 1]]}')
    
    #init the dimensions
    D,W,H = initDimensions(inp['grid'])
    #init the grid
    myG = initGrid (inp)
    #print the grid
    printGrid(myG)

    #Main algorithm:
    
    #From each 