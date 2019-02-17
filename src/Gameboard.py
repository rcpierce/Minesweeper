#This is the Gameboard class which will render the gameboard after a size and number of mines is initiated
import pygame
import random

# from src.Styles import Styles
from src.Tiles import Tiles

class Gameboard:
"""
Gameboard class creation. TO handle the board and display of board
"""
    # This was previously in the board_generator() function, but it needs to be
    # initialized outside of that function's scope for it to last the whole game

    # Constructor for initializing board values
    def __init__(self, board_size, mine_count, display):
    """
    initialization
    :param board_size: handled by user, create board of n^2
    :param mine_count: mine count handled by user
    :param display : create display of board based upon past two params
    """
        self.board_size = int(board_size)
        self.mine_count = int(mine_count)
        self.display    = display
        self.game_board = []
        self.total_mines = mine_count
        self.flag_count = self.mine_count #keeps a running total of number of flags used
        self.num_revealed_tiles = 0
        self.board_generator()
        

    # def loop(self): (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
        # while True:

    # Generate board and create tiles.
    def board_generator(self):
        """
        create gameboard with params passed in. 
        add mines randomly based upon number given in mine_count
        """
        # Traverse game board and fill with tiles.
        for x in range(0, self.board_size):
            arr = []
            for y in range(0, self.board_size):
                arr.append(Tiles(False, False, False, self.display))
            self.game_board.append(arr)

        # Randomly adds mines to the board until mine count equals zero
        # Creates two random numbers in range of board size and checks arr[][] at that location
        # Adds a mine to that location if one does not already exist
        while(self.mine_count > 0):
            random_row = random.randint(0, self.board_size - 1)
            random_col = random.randint(0, self.board_size - 1)
            
            if (not self.game_board[random_row][random_col].is_mine):
                self.game_board[random_row][random_col].is_mine = True
                self.mine_count -= 1

        # Counts number of adjacent mines at each tile
        # A nested for loop calling count_adjacent_mines() at each tile
        # count_adjacent_mines() will send count to Tiles object
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                self.count_adjacent_mines(x, y)

    def win(self, x, y):
        """
        rules for winning game: once all mines flagged or all other mines left alone
        """
        if (self.mine_count == self.total_mines):  #if number of correct used flags == total_mines
            return True  #win
        else:
            return False

    def lose(self, x, y):
        """
        game lost conditions
        """
        if (self.game_board[x][y].is_mine):
            return True  #lose
        else:
            return False        

    # Check and reveal surrounding tiles until base case or mine
    # It accepts coordinates as a position, checks if the coordinates are valid,
    # and calls other tiles recursively
    def rec_reveal(self, row, column):
        """
        recursively reveal tiles around, based upon click by user in gameboard
        :param row: identify row of mine
        :param column: identify column of mine
        """
        if(((row >= 0 and row < self.board_size) and (column >= 0 and column < self.board_size)) and not self.game_board[row][column].is_mine and not self.game_board[row][column].is_revealed and not self.game_board[row][column].is_flag):
            self.game_board[row][column].tile_reveal()
            self.num_revealed_tiles += 1    #increment number of revealed tiles
            if (self.game_board[row][column].num_adjacent_mines == 0):
                # Update display (tile_reveal()) (TO BE FINISHED WHEN WE IMPLEMENT PYGAME)
                self.rec_reveal(row - 1, column)          # (UP)
                self.rec_reveal(row - 1, column - 1)
                self.rec_reveal(row + 1, column)          # (DOWN)
                self.rec_reveal(row + 1, column - 1)
                self.rec_reveal(row, column - 1)          # (LEFT)
                self.rec_reveal(row + 1, column + 1)
                self.rec_reveal(row, column + 1)          # (RIGHT)
                self.rec_reveal(row - 1, column + 1)


    def flag_reveal(self, row, column):
        """
        rules for winning game: once all mines flagged or all other mines left alone
        """
        if self.game_board[row][column].is_mine == True and self.game_board[row][column].is_flag == True:
            return(self.game_board[row][column].tile_flag())
        elif self.game_board[row][column].is_mine == True and self.game_board[row][column].is_flag == False:
            return(self.game_board[row][column].tile_flag())
        else:
            return(self.game_board[row][column].tile_flag())

    # Counts number of mines adjacent to a given tile
    # It accepts position through row and column parameters
	# According to these coordinates, it determines whether an adjacent tile is valid
	# and if it is a mine. If it is a mine, increments num_adjacent_mines
    def count_adjacent_mines(self, row, column):
        """
        accepts position through row and column
        counts number of adjacent mines
        increment accordingly
        """
	#increment num_adjacent_mines including diagonals
        for row_inc in range (-1, 2):
            for col_inc in range (-1, 2):
			    #first check for valid indices
                if (((row+row_inc < self.board_size) and (column + col_inc < self.board_size) and ((not row_inc == 0) or (not col_inc == 0))) and row+row_inc >= 0 and column+col_inc >= 0):
                    #check if adjacent tile is a mine
                    if (self.game_board[row+row_inc][column+col_inc].is_mine):
                        self.game_board[row][column].num_adjacent_mines+=1

    def draw(self):
        """
        display of gameboard and fill mines or tiles accordingly.
        """
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                # if self.game_board[x][y].is_mine:
                #     self.game_board[x][y].surf.fill((255,0,0))
                self.display.blit(self.game_board[x][y].surf, ((5+35*x),(5+35*y)))
        pygame.display.flip()

    def detect_location(self):
        """
        pygame exact mouse click location
        helpful to identify if tile pressed has mine at location
        """
        #get mouse position
        board_position = pygame.mouse.get_pos() #returns tuple of pixels

		#check if clicking on dead space
        for i in range(0, self.board_size+1):
            if (board_position[0] in range (35*i, 35*i+5)) or (board_position[1] in range (35*i, 35*i+5)):
                return #do nothing

        #subtract 5 from board_position
        x_pos = int(board_position[0]) - 5
        y_pos = int(board_position[1]) - 5

        #divide by 35
        x_pos /= 35
        y_pos /= 35

        if ((not (self.win(int(x_pos), int(y_pos))) and not (self.lose(int(x_pos), int(y_pos)))) and not (self.game_board[int(x_pos)][int(y_pos)].is_flag)):
            self.rec_reveal(int(x_pos), int(y_pos))
        elif (self.game_board[int(x_pos)][int(y_pos)].is_mine and not self.game_board[int(x_pos)][int(y_pos)].is_flag):
            self.lose(int(x_pos), int(y_pos))
            raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop
        else:
            return 0

        if self.win(int(x_pos), int(y_pos)):
            raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop

        if self.lose(int(x_pos), int(y_pos)):
            raise Exception('Oh no! You exploded!') #raise exception to be caught by the calling loop

    def call_flag(self):
            #get mouse position
            board_position = pygame.mouse.get_pos() #returns tuple of pixels

            #check if clicking on dead space
            for i in range(0, self.board_size+1):
                if (board_position[0] in range (35*i, 35*i+5)) or (board_position[1] in range (35*i, 35*i+5)):
                    return #do nothing

            #subtract 5 from board_position
            x_pos = int(board_position[0]) - 5
            y_pos = int(board_position[1]) - 5

            #divide by 35
            x_pos /= 35
            y_pos /= 35

            print(f"This is where a flag should be ({x_pos},{y_pos})")
            if(self.game_board[int(x_pos)][int(y_pos)].is_flag):
                self.flag_count += 1
                self.mine_count += self.flag_reveal(int(x_pos), int(y_pos))
            elif(self.flag_count == 0 and not (self.game_board[int(x_pos)][int(y_pos)].is_flag)):
                print(f"Current flag count is: {self.flag_count}")
                return 0
            else:
                self.mine_count += self.flag_reveal(int(x_pos), int(y_pos))
                self.flag_count -= 1
            print(f"Current flag count is: {self.flag_count}")

            if self.win(int(x_pos), int(y_pos)):
                raise Exception('Congratulations, you win!') #raise exception to be caught by the calling loop

            print(f"{self.mine_count}")
            print(f"{self.total_mines}")