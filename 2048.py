import random
import curses
import time

def greetings():
    '''Welcomes user'''
    print("Hello user, welcome to terminal edition of 2048 game.")
    print("User arrow keys for merging board")
    print("To leave the game press 'q'")
    print("To restart the game press 'r'")
    enter = input("Press enter to start game:")

def init_game():
    '''Returns empty board and adds two initial tiles'''
    board = [[0 for col in range(4)] for row in range(4)]
    for i in range(2):
        x = new_tile(board)[0]
        y = new_tile(board)[1]
        tile = new_tile(board)[2]
        board[x][y] = tile
    return board

def add_new_tile(board):
    '''Adds tile to a board'''
    for row in board:
        if 0 in row:
            temp = new_tile(board)
            x = temp[0]
            y = temp[1]
            tile = temp[2]
            board[x][y] = tile
            break
    return board

def new_tile(board):
    '''Returns list containing coordinations and value of new tile:
    new_tile[0] - x coordination
    new_tile[1] - y coordination
    new_tile[2] - value of tile
    '''
    two_or_four = random.random()
    if two_or_four <= 0:
        new_tile_value = 4
    else:
        new_tile_value = 2

    new_x = random.randint(0, 3)
    new_y = random.randint(0, 3)
    while board[new_x][new_y] != 0:
        new_x = random.randint(0, 3)
        new_y = random.randint(0, 3)
    return [new_x, new_y, new_tile_value]

def remove_zeros(lst):
    '''Removes zeros from given row'''
    return [x for x in lst if x != 0]

def add_zeros(lst):
    '''Returns given list with added zeros at the end if list length is shorter than 4'''
    while len(lst) < 4:
        lst.append(0)
    return lst

def merge_line(line):
    '''Returns given list merged to the left side'''
    lst = remove_zeros(line)
    new_list = []
    while lst:
        if len(lst) == 1:
            new_list.append(lst[0])
            lst.pop(0)
        elif lst[0] == lst[1]:
            new_list.append(lst[0]*2)
            lst.pop(0)
            lst.pop(0)
        else:
            new_list.append(lst[0])
            lst.pop(0)
    new_list = add_zeros(new_list)
    return new_list

def left_merge(board):
    '''Returns board to the left side'''
    merged = []
    for x in board:
        merged.append(merge_line(x))
    return merged

def right_merge(board):
    '''Returns board to the right side'''
    merged = []
    for x in board:
        line = x
        line.reverse()
        line = merge_line(line)
        line.reverse()
        merged.append(line)
    return merged

def up_merge(board):
    '''Returns board to up direction'''
    new_board = [[0 for col in range(4)] for row in range(4)]
    line = []
    merged = []
    temp_board = []
    for x in range(0,4):
        for y in range(0,4):
            line.append(board[y][x])
        #print(line)    
        line = merge_line(line)
        temp_board.append(line)
        line = []    
    for x in range(0,4):
        for y in range(0,4):
            new_board[y][x] = temp_board[x][y]
    return new_board

def down_merge(board):
    '''Returns board to down direction'''
    new_board = [[0 for col in range(4)] for row in range(4)]
    line = []
    temp_board = []
    for x in range(0,4):
        for y in [3,2,1,0]:
            line.append(board[y][x])          
        line = merge_line(line)
        temp_board.append(line)
        line = []
        #print(temp_board)
    for x in range(0,4):
        lst = [3,2,1,0]
        for y in range(0,4):
            new_board[lst[x]][y] = temp_board[y][x]
    return new_board

def game_is_over(board):
    '''Returns True when game is over, otherwise returns False'''
    for i in range(0,4):
        for j in range(0,4):
            if (board[i][j] == 2048):
                return True
    for i in range(0,4):
        for j in range(0,4):
            if (board[i][j] == 0):
                return False
    for i in range(0,4):
        for j in range(0,3):
            if (board[i][j] == board[i][j+1]):
                return False
    for j in range(0,4):
        for i in range(0,3):
            if board[i][j] == board[i+1][j]:
                return False
    return True

def is_winner(board):
    '''Returns True when board has at least one tile with value 2048'''
    for x in range(0,4):
        for y in range(0,4):
            if board[x][y] == 2048:
                return True
    return False

def reset():
    ''''Returns empty board and adds two initial tiles'''
    val = init_game()
    return val

def get_score(board):
    '''Returns current board score'''
    score = 0
    for row in board:
        score += sum(row)
    return score

def print_score(board):
    '''Returns formatted string with current board score'''
    score = get_score(board)
    return "Your current score: {}".format(score)

def show_board(board):
    '''Returns formatted string with current board'''
    board_string = ''''''
    for row in board:
        board_string += ('      '.join(str(x) for x in row)) + "\n\n"
    board_string += "\n\n" + print_score(board)
    return board_string

greetings()
# get the curses screen window
screen = curses.initscr()
 
# turn off input echoing
curses.noecho()
 
# respond to keys immediately (don't wait for enter)
curses.cbreak()
 
# map arrow keys to special values
screen.keypad(True)

game = init_game()
#game = [[1024,2,0,0],[1024,16,2,2],[2,64,8,2],[16,2,16,8]]
screen.addstr(show_board(game))
try:
    while not game_is_over(game):    
       	char = screen.getch()
        if char == ord('q'):
            break
        elif char == ord('r'):
            game=reset()
            screen.addstr(0, 0, show_board(game))
        elif char == curses.KEY_RIGHT:
           # print doesn't work with curses, use addstr instead
            game = right_merge(game)
            game  = add_new_tile(game)
            screen.addstr(0, 0, show_board(game))
        elif char == curses.KEY_LEFT:
            game = left_merge(game)
            game = add_new_tile(game)
            screen.addstr(0, 0, show_board(game))   
        elif char == curses.KEY_UP:
            game = up_merge(game)
            game = add_new_tile(game)
            screen.addstr(0, 0, show_board(game))      
        elif char == curses.KEY_DOWN:
            game = down_merge(game)
            game = add_new_tile(game)  
            screen.addstr(0, 0, show_board(game))
            
finally:
     # shut down cleanly  
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    if is_winner(game):
        print("You Win")
    elif game_is_over(game):
        print("You Lost")