import json
import sys
import numpy as np
import copy
import queue  

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

    parent: object
    visited: bool
    D: int
    W: int
    H: int
    dim: list
    def  __init__(self,id):
        self.src = False
        self.trg = False
        self.visited = False
        self.stiener_point = False
        self.value = id
        self.parent = None
        if id == 0:
            #Empty
            self.empty = True
            self.via = False
            self.block = False
            self.cost = 1
        elif id == 1:
            #Block
            self.empty = False
            self.via = False
            self.block = True
            #Since we are dealing with consistent costs
            self.cost = 0
        elif id == 2:
            #Via
            self.empty = False
            self.via = True
            self.block = False
            #Since we are dealing with consistent costs
            self.cost = 1
            
    def setDim(self,D,H,W):
        self.D = D
        self.H = H
        self.W = W
        self.dim = [D,H,W]
        
    def specifySrc (self):
        self.src = True
        self.empty = False
        self.value = 3

    def specifyTrg (self):
        self.trg = True
        self.empty = False
        self.value = 4
    
    def myParent(self, Cell):
        self.parent = Cell
    
    def visitedNow(self):
        self.visited = True

    def giveRelative(self,relative,layers,width,height):
        emptyList = []
        if relative == "right":
            if self.W+1 >= width:
                return emptyList
            else:
                return [self.D , self.H, self.W+1]
        elif relative == "left":
            if self.W-1 <= -1:
                return emptyList
            else:
                return [self.D , self.H, self.W-1]
        elif relative == "north":
            if self.H-1 <= -1:
                return emptyList
            else:
                return [self.D, self.H-1, self.W]
        elif relative == "south":
            if self.H+1 >= height:
                return emptyList
            else:
                return [self.D , self.H+1, self.W]

        elif relative == "up":
            if self.D+1 >= layers:
                return emptyList
            else:
                return [self.D+1, self.H, self.W]
        elif relative == "down":
            if self.D-1 <= -1:
                return emptyList
            else:
                return [self.D-1 , self.H, self.W]
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
    graph = np.empty((D,H,W), dtype=object)
    graph[:,:,:] = vCells(init_arry)
    for layer in range(D):
        for j in range(H):
            for i in range (W):
                graph[layer][j][i].setDim(layer,j,i)
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
        for j in range(H):
            for i in range(W):
                #NOTE: if coloring is annoying, comment these
                #and replace with this:
                # print (str(graph[layer][j][i].value), end="\t")
                #Start..
                if graph[layer][j][i].visited:
                    print (Yellow + str(graph[layer][j][i].value), end="\t")
                else:
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
                    #End of commenting
                
                #To check dimensions
                # print (str(graph[layer][j][i].D) + ' '+\
                #         str(graph[layer][j][i].W) + ' '+\
                #         str(graph[layer][j][i].H) + ' '\
                #     , end="\t")

            print ("\n")
        print (Reset)

def findMinPath (myG_Copy, a, b):
    '''
    Gets the minimum path between a and b within the graph myG

    inputs:
        myG_Copy: copy of your graph
        a: point a
        b: :D

    outputs:
        path: simply the points..
    '''
    global D,W,H
    #init a Queue
    Q = queue.Queue() 
    #push the source/a
    Q.put(myG_Copy[a[0],a[1],a[2]])
    #Source is visited
    myG_Copy[a[0],a[1],a[2]].visitedNow()
    #the to-be-returned path
    path = []
    #false until found
    targetFound = False
    #list of directions
    directions = ["right", "left", "north", "south", "up","down"]
    while (not Q.empty() and not targetFound):
        #Pop from the Q
        x = Q.get()
        for direction in directions:
            #check all the edges (up, down, right, left, above, down)
            relative = x.giveRelative(direction, D, W, H)
            if len(relative) > 0:
                obj = myG_Copy[relative[0],relative[1],relative[2]]
                if obj.block == False and obj.visited == False: 
                    print (f'Im cell {x.dim} and my available relative is {obj.dim} on the {direction}')
                    obj.visitedNow()
                    obj.myParent(x)
                    if obj.dim == b:
                        targetFound = True
                    else:
                        Q.put(obj)


        printGrid(myG_Copy)
    while obj.parent != None:
        print (obj.parent.dim)
        temp = obj.parent
        obj = temp


if __name__ == "__main__":
    #Global Variables
    D = 0
    W = 0
    H = 0

    # inp = json.load(sys.stdin)
    inp = json.loads('{"grid": [[[0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0], [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0], [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1], [0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0], [1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1], [0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]]],\
         "src_coor": [0, 12, 11], "dest_coor": [[0, 7, 4], [0, 14, 12], [0, 6, 8], [0, 0, 1]]}')
    
    #init the dimensions
    D,H,W = initDimensions(inp['grid'])
    #init the grid
    myG = initGrid (inp)
    #print the grid
    printGrid(myG)

    #Main algorithm:
    #Loop until termination condition:
        #1- For each target we have:
            #find T_s the nearest source for each target
        #2- select the min one..if none exist...terminate(5)
        #3- mark the path as sources
        #4- extract that target point as it is a Src now
        #5- update condition of termination (terminals are cleared or no path exist from (2)!)
    #Print:
        #existence?
        #the path... it is easy..all the sources
        #the cost..this is easy it's = len(paths) + 1
    
    exitLoop = False
    sources = []
    sources.append(inp['src_coor'])
    targets = inp['dest_coor']
    while (not exitLoop):
        #Holds all the min paths for all targets
        minPaths = []
        for target in targets:
            #Create a copy of the current graph
            myG_Copy = copy.copy(myG)
            #Holds all the pathes of target i
            paths = []
            for source in sources:
                path = findMinPath (myG_Copy, target, source)
                #if there's a path between target i and source j
                if len(path) > 0:
                    paths.append(path)
            #if we have paths...get me the min
            if len(paths) > 0:
                minPaths.append(getMinPath(paths))
            #if we don't have paths, we don't have a solution..
            else:
                print (f'this target got no destination to sources {target}')
