#name: Harris Shepard
#8 Puzzle Problem
#Uniform Cost Search



import sys#used to get maxint

#makes a solution array depending on the size of the puzzle
def get_solution(size):
    solution = list(range(1,size*size))
    solution.append(None)
    return solution

#makes an easy to solve puzzle
def make_puzzle(size):
    puzzle = []
    for n in range(size*size-1):
        puzzle.append(n)
    puzzle.append(None)
    return puzzle

#returns the position of the empty tile in a puzzle
def get_empty_tile_pos(puzzle):
    return puzzle.index(None)#value of none is empty tile

#get_adjacent_pos, gets all adjacent positions from a place in the puzzle (the puzzle is represented as a 1d array)
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

#swap, swaps 2 tiles on a puzzle
def swap(puzzle,pos1,pos2):
    puzzle[pos1],puzzle[pos2] = puzzle[pos2],puzzle[pos1]

#get_next_lowest_cost_puzzle, alternative to priority queue looks for the minimum cost
#returns an index from a list of puzzles
def get_next_lowest_cost_puzzle(puzzles):
    if not puzzles:
        return
    min = puzzles[0].cost
    min_index = 0

    count = 0
    
    for puzzle in puzzles:
        cost = puzzle.cost
        if(cost< min):
            min = cost
            min_index = count
        count+=1
    return min_index

#puzzle objs, list of Puzzle objects
#target_puzzle, a puzzle arr
def get_puzzle(puzzle_objs,target_puzzle):
    index = 0
    for puzzle_obj in puzzle_objs:
        if(target_puzzle == puzzle_obj.puzzle):
            return index
        index+=1
    return None#else return None


#PUZZLE CLASS:
#has cost
#has puzzle
#has a __str__ function
#has a pointer to the previous state
class Puzzle:
    def __init__ (self, puzzle,cost,rows,previous_state,num_moves):
        self.puzzle = puzzle
        self.cost = cost
        self.parent = previous_state#previous obj is set when appending to unexplored
        self.rows = rows
        self.num_moves = num_moves
    def __str__(self):
        puzzle_str = ""
        count=0
        for i in range(self.rows):
            for j in range(self.rows):
                puzzle_str += str(self.puzzle[count])+' '
                count+=1
            puzzle_str+= '\n'
        puzzle_str += "c: "+str(self.cost) + '\n'  
        puzzle_str += "n: "+str(self.num_moves) + '\n'  
        return puzzle_str
#DRIVER CLASS:
#uses helper functions above

##important class members:
#explored, a list of Puzzles 
#unexplored, a list of Puzzles


#explored,unexplored are dictionaries in the form of list:cost 
UNIFORM_COST_SEARCH = 0
A_STAR_SEARCH_MISPLACED = 1
A_STAR_SEARCH_EUCLIDEAN = 2
class Problem:
    
    def __init__(self,size=3,user_puzzle = None):
        if(not user_puzzle):
            puzzle = make_puzzle(size)
        else:
            puzzle = user_puzzle
        #self.known_positions = {}
        self.unexplored = [Puzzle(puzzle,0,size,None,0)]
        self.explored = []
        self.size = size
        #self.cost = 0
        self.solution = get_solution(size)
        self.found_solution = None



        #print("Unexplored:", self.unexplored)
        #print("Empty tile pos:", get_empty_tile_pos(puzzle))
        #print("Adjacent pos:",get_adjacent_pos(4,3))
        #swap(puzzle,0,1)
        #print("Swap:",puzzle)
        #print("maxint: ",sys.maxsize)
    def is_solution(self,puzzle):
        if(self.solution == puzzle): 
            return True
        return False

    #done after finding the solution
    #trace back the puzzles until None state
    def trace_back(self):
        puzzle_obj_list = []
        if(not self.found_solution):
            return
        current_puzzle_obj = self.found_solution
        while(current_puzzle_obj != None):
            puzzle_obj_list.append(current_puzzle_obj)
            current_puzzle_obj = current_puzzle_obj.parent
        return puzzle_obj_list

    #gets the number of misplaced tiles
    def get_num_misplaced_tiles(self,puzzle):
        
        num_misplaced_tiles = 0
        for n in range(len(self.solution)):
            if(self.solution[n]!=puzzle[n]):
                num_misplaced_tiles+=1
        return num_misplaced_tiles

    #calculates cost of a node before appending it to unexplored
    def get_new_cost(self,old_cost,puzzle,num_moves,mode = UNIFORM_COST_SEARCH):
        new_cost= old_cost
        if(mode==UNIFORM_COST_SEARCH):
            new_cost+=1
        elif(mode==A_STAR_SEARCH_MISPLACED):
            new_cost = num_moves+self.get_num_misplaced_tiles(puzzle)
        return new_cost
    
    def explore_next(self,mode = UNIFORM_COST_SEARCH):
        if not self.unexplored:
            print("ERROR: Cannot reach end position")#no nodes to explore
            print("Len of explored: ",len(self.explored))
            
            return
        
        #puzzle,cost = self.unexplored.pop()
        min_index = get_next_lowest_cost_puzzle(self.unexplored)
        puzzle_obj = self.unexplored.pop(min_index)
        puzzle,cost,num_moves = puzzle_obj.puzzle,puzzle_obj.cost,puzzle_obj.num_moves

        self.explored.append(puzzle_obj)
        
        #print("popped:",puzzle_obj)

        empty_tile_pos = get_empty_tile_pos(puzzle)
        adj_nodes = get_adjacent_pos(empty_tile_pos,self.size)
        num_moves+=1#new num_moves

        for node in adj_nodes: #make new puzzles(copies) from the possible moves
            copy = puzzle.copy()#make a new list
            swap(copy,empty_tile_pos,node)

            
            new_cost = self.get_new_cost(cost,copy,num_moves,mode)#gets the new cost of a node
            
            if(self.is_solution(copy)):#check copies for solution before appending to frontier
                print("Solution Found: ")
                self.found_solution = Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves)
                

            if(not get_puzzle(self.explored,copy)):#if its not explored, append to unexplored
                self.unexplored.append(Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves))

            #print("copy: ",copy,cost)

    
    
        
        

    #not used, only for testing
    def explore_n_times(self,n):
        for i in range(n):
            self.explore_next()

        print("Explored",n," times: ")
        print("Unexplored: ")
        for node in self.unexplored:
            print(node)
        print(self.explored)
        return

    #only goes to the first solution, guaranteed to be the best
    def uniform_cost_search(self,upper_limit = 10000):
        iterations = 0
        while(not self.found_solution and iterations < upper_limit and self.unexplored):
            self.explore_next()
            iterations+=1
        if(self.found_solution):
            puzzle_obj_list = self.trace_back()
            for puzzle in puzzle_obj_list:
                print(puzzle)
            print("Found solution cost: ",self.found_solution.cost)
        print("Length explored: ",len(self.explored))
        print("Length unexplored: ", len(self.unexplored))


        return
    def a_star_search(self,upper_limit = 10000):
        iterations = 0
        
        #continues exploring until finding a solution, reaching the upper limit, or not having any unexplored nodes left
        while(not self.found_solution and iterations < upper_limit and self.unexplored):
            self.explore_next(A_STAR_SEARCH_MISPLACED)
            iterations+=1
        if(self.found_solution):
            puzzle_obj_list = self.trace_back()
            for puzzle in puzzle_obj_list:
                print(puzzle)
            print("Found solution cost: ",self.found_solution.cost)
        print("Length explored: ",len(self.explored))
        print("Length unexplored: ", len(self.unexplored))
        print("")




#function to check for solution


problem_test = Problem(3)
#problem_test.explore_next()
#print("len unexplored: ", len(problem_test.unexplored))
#print("Next pair", get_next_lowest_cost_pair(problem_test.unexplored))

#if([0,1,2]==[0,1,2]):
    #print("array equality check")
solution = get_solution(3)
#print("Solution: ",solution)
#print("Is solution?",problem_test.is_solution([0, 1, 2, 3, 4, 5, 6, 7, None]))

#problem_test2 = Problem(3)
#problem_test2.explore_n_times(10)


hardest_puzzle = [8, 6, 7, 2, 5, 4, 3, None, 1]
zero_move_puzzle = [1,2,3,4,5,6,7,8,None]
two_move_puzzle = [1,2,3,4,None,6,7,5,8]
four_move_puzzle = [None,1,3,4,2,6,7,5,8]
#problem_test3 = Problem(3,hardest_puzzle) #DO NOT DO THIS, depth 30 is ~>1 billion states 2^30, #6 mins gives depth 20
problem_test3 = Problem(3,four_move_puzzle)
print("Solution:",problem_test3.solution)            
#problem_test3.uniform_cost_search()
problem_test3.a_star_search()
