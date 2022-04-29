#name: Harris Shepard
#8 Puzzle Problem
#Uniform Cost Search



import sys#used to get maxint


def get_solution(size):
    solution = list(range(size*size-1))
    solution.append(None)
    return solution
def make_puzzle(size):
    puzzle = []
    for n in range(size*size-1):
        puzzle.append(n)
    puzzle.append(None)
    return puzzle
def get_empty_tile_pos(puzzle):
    return puzzle.index(None)#value of none is empty tile

#size, the length/width of the puzzle
#pos, the reference position, gets adjacent from the reference    
def get_adjacent_pos(pos,size):
    row = pos//size
    col = pos%size
    max_rowcol_index = size -1
    adj_pos = []
    if(row < (max_rowcol_index)):#there is a node below
        adj_pos.append(pos+size)
    if(row > 0):#there is a node above
        adj_pos.append(pos-size)
    if(col < (max_rowcol_index)):#there is a node to the right
        adj_pos.append(pos+1)
    if(col > 0):#there is a node to the left
        adj_pos.append(pos-1)
    return adj_pos
#swaps 2 tiles on a puzzle
def swap(puzzle,pos1,pos2):
    puzzle[pos1],puzzle[pos2] = puzzle[pos2],puzzle[pos1]


#returns a pair from a list of pairs
def get_next_lowest_cost_pair(list,cost_pos_in_pair = 1):
    if (not list):
        return
    min = list[0][cost_pos_in_pair]
    min_index = 0

    count = 0
    for pair in list:
        cost = pair[1]
        if(cost< min):
            min = cost
            min_index = count
        count+=1
    return list[min_index]

#MAIN CLASS:
#uses helper functions above

##important class members:
#explored, a dictionary in the form of an n-tuple representing the puzzle state as the key
    #the value is the cost
    #{tuple(puzzle):cost}
#unexplored, a list of pairs with the first of the pair being a list of integers representing the puzzle state
    #the second of the pair is the cost
    #(puzzle,cost)

#explored,unexplored are dictionaries in the form of list:cost 
class Problem:
    def __init__(self,size=3):
        puzzle = make_puzzle(size)
        #self.known_positions = {}
        self.unexplored = [(puzzle,0)]
        self.explored = {}
        self.size = size
        #self.cost = 0
        self.solution = get_solution(size)



        #print("Unexplored:", self.unexplored)
        #print("Empty tile pos:", get_empty_tile_pos(puzzle))
        #print("Adjacent pos:",get_adjacent_pos(4,3))
        #swap(puzzle,0,1)
        #print("Swap:",puzzle)
        #print("maxint: ",sys.maxsize)

    def explore_next(self):
        if not self.unexplored:
            print("ERROR: Cannot reach end position")#no nodes to explore
            print("Len of explored: ",len(self.explored))
            
            return
        
        puzzle,cost = self.unexplored.pop()
        self.explored[tuple(puzzle)] = cost #append to explored
        cost+=1
       
        print("popped:",puzzle)

        empty_tile_pos = get_empty_tile_pos(puzzle)
        adj_nodes = get_adjacent_pos(empty_tile_pos,self.size)
        for node in adj_nodes:
            copy = puzzle.copy()
            swap(copy,empty_tile_pos,node)
            if(not self.explored.get(tuple(copy),None)):#if its not explored, append to unexplored
                self.unexplored.append((copy,cost))

            print("copy: ",copy,cost)
    def is_solution(self,puzzle):
        if(self.solution == puzzle):
            return True
        return False
    def uniform_cost_search(self):
        return
    def test(self):
        print("self.explored:")
        for pair in self.explored:
            print (pair)
        puzzle = [1, 0, 2, 3, 4, 5, 6, 7, None]
        
        print("index pos: ",self.explored.get(tuple(puzzle),None))
        

#function to check for solution


problem_test = Problem(3)
problem_test.explore_next()
print("len unexplored: ", len(problem_test.unexplored))
print("Next pair", get_next_lowest_cost_pair(problem_test.unexplored))

if([0,1,2]==[0,1,2]):
    print("array equality check")
solution = get_solution(3)
print("Solution: ",solution)
print("Is solution?",problem_test.is_solution([0, 1, 2, 3, 4, 5, 6, 7, None]))