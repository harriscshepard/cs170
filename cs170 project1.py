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
    def __init__(self, pos, val,row=-1,col=-1):
        self.pos = pos
        self.val = val
        self.row = row
        self.col = col
    def __str__(self):
        return str(self.val)
        #return "("+str(self.position)+","+ str(self.val)+")"
    #update the position of the tile
    def update_pos(self,pos,row,col):
        self.pos = pos
        self.row = row
        self.col = col

#has a position
#has a number


#class for  8 puzzle
#contains a list of tiles or empty tiles
class Puzzle:
    def __init__(self,rows = 3,empty_pos = 0):
        self.tiles = []
        self.rows = rows
        self.empty_pos = empty_pos
        for i in range(rows*rows):
            pos = i


            if(i == empty_pos):
                val = None
            else:
                val = i
            row,col = self.get_row_col(pos)
            
            self.tiles.append(Tile(pos,val,row,col))
    def __str__(self):
        tile_str = ""


        count = 0
        for i in range(self.rows):
            for j in range(self.rows):
                tile_str += str(self.tiles[count])+' '
                count+=1
            tile_str += '\n'
    

        return tile_str
    #function to get a tile
    def get_tile(self, pos):
        return self.tiles[pos]

    #function to get the row and col of a tile:
    #pos, a tile object's pos
    #rows, the number of rows in the puzzle
    def get_row_col(self,pos):
        row = (pos)//self.rows #integer division
        col = pos%self.rows
        return row,col

    #function to get adjacent nodes:
    def get_adj(self,tile):
        row = tile.row
        col = tile.col
        pos = tile.pos
        size = self.rows
        adjacent = []
        if(row==0):#then you have an adjacent node below
            adjacent.append(self.tiles[pos+size])


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
tile_test = Tile(0,None)
print("tile_test: (", tile_test.pos, tile_test.val,")")
if (not tile_test.val):
    print("test: tile_test is None")
print(tile_test)

puzzle_test = Puzzle(3,8)
print(puzzle_test)

