#name: Harris Shepard
#8 Puzzle Problem
#Uniform Cost Search





#class for empty tile
#has a position
class Empty_Tile:
    def __init__(self, position):
        self.position = position
        self.val = None




#class for tile
class Tile:
    def __init__(self, position, val):
        self.position = position
        self.val = val
    
tile_test = Empty_Tile(0)
print("tile_test: (", tile_test.position, tile_test.val,")")
if (not tile_test.val):
    print("test: tile_test is None")
#has a position
#has a number


#class for  8 puzzle
#contains a list of tiles or empty tiles
class Puzzle:
    def __init__(self,rows = 3):
        for i in range(rows*rows):
            

#function to move empty tile (adjacent_tile)
    #swaps empty tile and an adjacent tile
        #swap position in puzzle arr
        
#function to swap tile (empty_tile,adjacent_tile):
    #swap positions in puzzle arr
    #update empty_tile's values
    #update adjacent_tile's values

#function to check for solution
    #for tile in puzzle_arr:
        #if(tile.val != count):
            #return false
    #return True
