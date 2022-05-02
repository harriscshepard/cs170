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


UNIFORM_COST_SEARCH = 0
A_STAR_SEARCH_MISPLACED = 1
A_STAR_SEARCH_EUCLIDEAN = 2
class Problem:
    def is_solution(self,puzzle):
        if(self.solution == puzzle): 
            return True
        return False
    def __init__(self,size=3,user_puzzle = None):
        if(not user_puzzle):
            puzzle = make_puzzle(size)
        else:
            puzzle = user_puzzle

        self.unexplored = [Puzzle(puzzle,0,size,None,0)]
        self.explored = []
        self.size = size

        self.solution = get_solution(size)

        #check if the puzzle is the solution
        if(self.is_solution(puzzle)):
            self.found_solution = Puzzle(puzzle,0,size,None,0)
        else:
            self.found_solution = None



        #print("Unexplored:", self.unexplored)
        #print("Empty tile pos:", get_empty_tile_pos(puzzle))
        #print("Adjacent pos:",get_adjacent_pos(4,3))
        #swap(puzzle,0,1)
        #print("Swap:",puzzle)
        #print("maxint: ",sys.maxsize)
    

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
    def print_trace_back(self):
        puzzle_objs = self.trace_back()
        for puzzle in puzzle_objs:
            print(puzzle)

    #gets the number of misplaced tiles
    def get_num_misplaced_tiles(self,puzzle):
        
        num_misplaced_tiles = 0
        for n in range(len(self.solution)):
            if(self.solution[n]!=puzzle[n]):
                num_misplaced_tiles+=1
        return num_misplaced_tiles


    #for each position in the puzzle, gets the value and row/col # and finds the correct row/col given the value
    def get_euclidean_dists(self,puzzle):
        euclidean_dists = 0

        for n in range(len(self.solution)):
            val = puzzle[n]
            row,col = n//self.size , n%self.size

            correct_pos = self.solution.index(val)
            correct_row,correct_col = correct_pos//self.size, correct_pos%self.size

            euclidean_dist = ((correct_row-row)**2 + (correct_col-col)**2) **(1/2)#euclidean distance formula
            euclidean_dists += euclidean_dist
        return euclidean_dists
    

    #calculates cost of a node before appending it to unexplored
    def get_new_cost(self,old_cost,puzzle,num_moves,mode = UNIFORM_COST_SEARCH):
        new_cost= old_cost
        if(mode==UNIFORM_COST_SEARCH):
            new_cost+=1
        elif(mode==A_STAR_SEARCH_MISPLACED):
            new_cost = num_moves+self.get_num_misplaced_tiles(puzzle)
        elif(mode==A_STAR_SEARCH_EUCLIDEAN):
            new_cost = num_moves+self.get_euclidean_dists(puzzle)
        else:#uniform cost search
            new_cost+=1
        return new_cost
    
    def explore_next(self,mode = UNIFORM_COST_SEARCH):
        if not self.unexplored:
            print("ERROR: Cannot reach end position")#no nodes to explore
            print("Len of explored: ",len(self.explored))
            
            return
        
        #puzzle,cost = self.unexplored.pop()
        
        min_index = get_next_lowest_cost_puzzle(self.unexplored)
        puzzle_obj = self.unexplored.pop(min_index)
        puzzle,cost,num_moves = puzzle_obj.puzzle, puzzle_obj.cost, puzzle_obj.num_moves

        print("Exploring: \n",puzzle_obj)

        self.explored.append(puzzle_obj)

        if(self.found_solution): #already found solution, cull node if impossible for node to get better solution
            if(num_moves >= (self.found_solution.num_moves-1)): #if the current node is 13 moves, cannot find a better solution from this node
                return
            #discard node

        
        
        #print("popped:",puzzle_obj)

        empty_tile_pos = get_empty_tile_pos(puzzle)
        adj_nodes = get_adjacent_pos(empty_tile_pos,self.size)
        num_moves+=1#new num_moves

        print("Appending possible moves to the frontier:")
        for node in adj_nodes: #make new puzzles(copies) from the possible moves
            copy = puzzle.copy()#make a new list
            swap(copy,empty_tile_pos,node)

            
            new_cost = self.get_new_cost(cost,copy,num_moves,mode)#gets the new cost of a node
            
            if(self.is_solution(copy)):#check copies for solution before appending to frontier
                
                self.found_solution = Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves)
                print("******************************************************")
                print("Found Solution, Trying to find better solution:\n******************************************************\n",self.found_solution)

            if(not get_puzzle(self.explored,copy)):#if its not explored, append to unexplored
                if(not self.found_solution):
                    self.unexplored.append(Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves))
                    print(Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves))
                elif(num_moves<(self.found_solution.num_moves-2)):
                    #found solution, do not add nodes that cannot find a better solution
                    #if solution is 14, expanding a 12 move node can find a 13 move solution, but do not add 13 move nodes to unexplored
                    #12 !< 14-2
                    #11 < 14-2
                    self.unexplored.append(Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves))
                    print(Puzzle(copy,new_cost,self.size,puzzle_obj,num_moves))

                else:
                    return
        print('-----------------------------------')
        return


       
    #cull_obsolete_unexplored
    #only used for diagnostics
    #found the solution already, cull unexplored, cannot have better solutions with more moves than the found solution
    def cull_obsolete_unexplored(self):
        if (not self.found_solution):
            return

        #if solution is 14 moves, exploring any 13 move or above states cannot improve the solution
        num_moves_threshold = self.found_solution.num_moves-1

        index = 0
        len_before = len(self.unexplored)
        for puzzle_obj in self.unexplored:
            num_moves = puzzle_obj.num_moves
            
            
            if(num_moves >= num_moves_threshold ):
                self.unexplored.pop(index)
                print("popping: ", puzzle_obj)
                index-=1
            index+=1
        len_after = len(self.unexplored)
        print ("End of Cull, Before: ",len_before," after: ",len_after)
        return len_before,len_after


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

    #all searches will return whether the maximum iterations has been reached
    #only goes to the first solution, guaranteed to be the best
    def uniform_cost_search(self,upper_limit = 10000):
        iterations = 0
        while(not self.found_solution and iterations < upper_limit and self.unexplored):
            self.explore_next()
            iterations+=1

        
        #traceback, optional same as print_trace_back
        if(self.found_solution):
            #puzzle_obj_list = self.trace_back()
            #for puzzle in puzzle_obj_list:
            #    print(puzzle)
            print("Uniform Cost Search:")
            print("Found solution cost, (depth): ",self.found_solution.cost)
        print("Length explored: ",len(self.explored))
        print("Length unexplored: ", len(self.unexplored))
        print("Total Length, (nodes in memory):",len(self.explored)+len(self.unexplored))
        print("")

        return (iterations == upper_limit)
    def a_star_search_misplaced(self,upper_limit = 10000):
        iterations = 0
        
        #continues exploring until finding a solution, reaching the upper limit, or not having any unexplored nodes left
        while(iterations < upper_limit and self.unexplored):
            self.explore_next(A_STAR_SEARCH_MISPLACED)
            iterations+=1

        print("A* Search Misplaced Tiles:")
        #traceback, optional
        if(self.found_solution):
            #puzzle_obj_list = self.trace_back()
            #for puzzle in puzzle_obj_list:
                #print(puzzle)
            print("Found solution cost, (depth): ",self.found_solution.cost)
        print("Length explored: ",len(self.explored))
        print("Length unexplored: ", len(self.unexplored))
        print("Total Length, (nodes in memory):",len(self.explored)+len(self.unexplored))
        print("")
        return (iterations == upper_limit)
    def a_star_search_euclidean(self,upper_limit = 10000):
        iterations = 0
        
        #continues exploring until reaching the upper limit, or not having any unexplored nodes left
        while(iterations < upper_limit and self.unexplored):
            self.explore_next(A_STAR_SEARCH_EUCLIDEAN)
            iterations+=1
            
        print("A* Search Euclidean:")
        #traceback, optional
        if(self.found_solution):
            #puzzle_obj_list = self.trace_back()
            #for puzzle in puzzle_obj_list:
                #print(puzzle)
            print("Found solution cost, (depth): ",self.found_solution.cost)
        print("Length explored: ",len(self.explored))
        print("Length unexplored: ", len(self.unexplored))
        print("Total Length, (nodes in memory):",len(self.explored)+len(self.unexplored))
        print("")
        return (iterations == upper_limit)

    #call the other searches
    def do_search(self,mode=UNIFORM_COST_SEARCH,upper_limit=10000):
        ret = 0
        if(mode == UNIFORM_COST_SEARCH):
            ret = self.uniform_cost_search(upper_limit)
        elif(mode == A_STAR_SEARCH_MISPLACED):
            ret =self.a_star_search_misplaced(upper_limit)
        elif(mode == A_STAR_SEARCH_EUCLIDEAN):
            ret = self.a_star_search_euclidean(upper_limit)
        else:
            ret = self.uniform_cost_search(upper_limit)
    
def test_each_search(puzzles,rows=3):
    count =0
    problem_obj = None
    for puzzle in puzzles:
        puzzle_obj = Puzzle(puzzle,0,rows,None,0)#puzzle obj just to print and call str(Puzzle)
        print("Puzzle no: ",count,"\n",puzzle_obj)

        problem_obj = Problem(rows,puzzle)# make a problem object per search, stored explored, unexplored
        problem_obj.uniform_cost_search()
        

        problem_obj = Problem(rows,puzzle)# make a problem object per search, stored explored, unexplored
        problem_obj.a_star_search_misplaced()
        

        problem_obj = Problem(rows,puzzle)# make a problem object per search, stored explored, unexplored
        problem_obj.a_star_search_euclidean()
        print("Traceback:")
        problem_obj.print_trace_back()
    return problem_obj #a star euclidean object






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


hardest_puzzle = [8, 6, 7, 2, 5, 4, 3, None, 1]#DO NOT DO THIS, depth 30 might take forever with ucs, #6 mins gives depth 20
zero_move_puzzle = [1,2,3,4,5,6,7,8,None]
two_move_puzzle = [1,2,3,4,None,6,7,5,8]
four_move_puzzle = [None,1,3,4,2,6,7,5,8]
eleven_move_puzzle = [4,None,1,7,2,3,5,8,6]

trivial = [1,2,3,4,5,6,7,8,None]
easy = [1,2,None,4,5,3,7,8,6]
very_easy = [1,2,3,4,5,6,7,None,8]
doable = [None,1,2,4,5,3,7,8,6]
oh_boy  =[8,7,1,6,None,2,5,4,3]
submission_puzzle = [1,None,3,4,2,6,7,5,8]

#problem_test3 = Problem(3,hardest_puzzle) 
problem_test3 = Problem(3,submission_puzzle)
#problem_test3.a_star_search_euclidean()

#print("Solution:",problem_test3.solution)            
#problem_test3.uniform_cost_search()
#problem_test3.a_star_search_euclidean()
#print("Euclidean Dists: ",problem_test3.get_euclidean_dists())



#problem_test4 = test_each_search([eleven_move_puzzle])

#problem_test4.cull_obsolete_unexplored()

user_input = ""
print("Welcome to Harris Shepard, 862132345 8 puzzle program")
print("Default parameters:")
print("Smallest Tile value: 1")
print("'None' for Empty tile, (enter empty tiles as * please)")
print("q to quit\n")

user_puzzle = []
search_menu = "0: UNIFORM_COST_SEARCH:\n1: A* SEARCH MISPLACED\n2: A* SEARCH EUCLIDEAN\n:"
while(user_input != 'q'):

    user_input = input("Enter a puzzle as a list\nExample: 1 2 3 4 5 6 7 8 *\nor 'q' to quit\n: ")
    if(user_input == 'q'):
        break
    puzzle = user_input.split()
    #replace the star with a None
    count = 0
    #print(len(puzzle))
    for letter in puzzle:
        if letter == "*":
            puzzle[count] = None
        else:
            puzzle[count] = int(letter)
        count+=1

    user_puzzle_obj = Puzzle(puzzle,0,3,None,0)
    print("Your puzzle is: \n",user_puzzle_obj)
    print("What type of search would you like to do?")
    user_input = int(input(search_menu))

    user_problem = Problem(3,puzzle)
    reached_upper_limit = user_problem.do_search(user_input)
    if(reached_upper_limit):
        print("Could not find solution explored the upper limit (default 10,000) nodes")
    else:
        user_input = input("Would you like the traceback? (y/n): ")
        if(user_input == 'y'):
            user_problem.print_trace_back()
            user_input = input("Type anything to continue...")
        
        

    


