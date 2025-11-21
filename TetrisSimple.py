import pygame, random, time, sys
from pygame.locals import *

import pygame.mixer

# set up the game
pygame.init()

# set up the window
WINDOWHEIGHT = 600
WINDOWWIDTH = WINDOWHEIGHT + int(WINDOWHEIGHT / 10)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Tetris')

# set up the main clock
mainClock = pygame.time.Clock()

# set game speed
FPS = 30

# set game size moddifier
GAMESIZE = 200

# set up colors
#          R    G    B
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

# load game background and board images
BACKGROUND = pygame.image.load('Background.png')
BOARDIMAGE = pygame.image.load('Board.png')
LEVELIMAGE = pygame.image.load('Level.png')
SCOREIMAGE = pygame.image.load('Score.png')
LINESIMAGE = pygame.image.load('Lines.png')
MENUIMAGE = pygame.image.load('Menu image1.png')
PLAYIMAGE = pygame.image.load('Play.png')
PLAYLIGHT = pygame.image.load('Play light.png')
QUITIMAGE = pygame.image.load('Quit.png')
QUITLIGHT = pygame.image.load('Quit light.png')
ENDGAME = pygame.image.load('End game.png')
PAUSEGAME = pygame.image.load('Game pause.png')

# load number image
ZERO = pygame.image.load('Zero.png')
ONE = pygame.image.load('One.png')
TWO = pygame.image.load('Two.png')
THREE = pygame.image.load('Three.png')
FOUR = pygame.image.load('Four.png')
FIVE = pygame.image.load('Five.png')
SIX = pygame.image.load('Six.png')
SEVEN = pygame.image.load('Seven.png')
EIGHT = pygame.image.load('Eight.png')
NINE = pygame.image.load('Nine.png')
NUMBERS = {0:ZERO, 1:ONE, 2:TWO, 3:THREE, 4:FOUR, 5:FIVE, 6:SIX, 7:SEVEN,
           8:EIGHT, 9:NINE}

# load block colors
BLUEBLOCK = pygame.image.load('Blue block.png')
REDBLOCK = pygame.image.load('Red block.png')
YELLOWBLOCK = pygame.image.load('Yellow block.png')
PINKBLOCK = pygame.image.load('Pink block.png')
ORANGEBLOCK = pygame.image.load('Orange block.png')
GREENBLOCK = pygame.image.load('Green block.png')
COLLORS = {2:REDBLOCK, 3:BLUEBLOCK, 4:YELLOWBLOCK, 5:PINKBLOCK, 6:ORANGEBLOCK,
           7:GREENBLOCK}

# board variables
board_x = 3
board_y = 0
board_line = 18
board_row = 10
board_thickness = 3

# block variables
sq_left = 0
sq_top = 0
sq_size = int(WINDOWHEIGHT / board_line)
TEMPLATEHEIGHT = 5
TEMPLATEWIDTH = 5

background_left = 0
background_top = 0
interface_width = sq_size * 7
interface_height = sq_size * 2
letter_size = int(sq_size * 0.8)

# interface positions
interface_left = background_left + (sq_size * 13)
level_top = background_top + (sq_size * 9)
score_top = background_top + (sq_size * 12)
lines_top = background_top + (sq_size * 15)

# menu letter coordinates
play_left = 180
play_top = 420
quit_left = 180
quit_top = 380 + 5 * letter_size

# menu letter size
play_width = letter_size * 4
quit_width = play_width

board_left = background_left + (sq_size * 2)
board_top = background_top
board_width = 2 * board_thickness + 1 + (sq_size + 1) * board_row
board_height = 2 * board_thickness + 1 + (sq_size + 1) * board_line

# image sizes
board_image = pygame.transform.scale(BOARDIMAGE, (sq_size * board_row, sq_size * board_line))
level_image = pygame.transform.scale(LEVELIMAGE, (interface_width, interface_height))
score_image = pygame.transform.scale(SCOREIMAGE, (interface_width, interface_height))
lines_image = pygame.transform.scale(LINESIMAGE, (interface_width, interface_height))
background_image = pygame.transform.scale(BACKGROUND, (sq_size * (board_line + 2), sq_size * board_line))
menu_image = pygame.transform.scale(MENUIMAGE, (sq_size * board_row, sq_size * board_line))
play_image = pygame.transform.scale(PLAYIMAGE, (play_width, letter_size))
play_light = pygame.transform.scale(PLAYLIGHT, (play_width, letter_size))
quit_image = pygame.transform.scale(QUITIMAGE, (quit_width, letter_size))
quit_light = pygame.transform.scale(QUITLIGHT, (quit_width, letter_size))
end_image = pygame.transform.scale(ENDGAME, (sq_size * board_row, sq_size * board_line))
pause_game = pygame.transform.scale(PAUSEGAME, (sq_size * board_row, sq_size * board_line))

# scoring variables
one_line = 50
two_lines = 150
three_lines = 350
four_lines = 1000
board_clear = 2000
every_piece = 10
line_num = 0

max_level = 20
speed_index = 2
rotate_speed = 15
move_speed = 15

x = 0
y = 0

score = 0
level = 0
line = 0

# set the shape of the block
def blockShape():
    S = [['.....',
         '.....',
         '..OO.',
         '.OO..',
         '.....'],
         ['.....',
          '.O...',
          '.OO..',
          '..O..',
          '.....']]

    Z = [['.....',
          '.....',
          '.OO..',
          '..OO.',
          '.....'],
         ['.....',
          '..O..',
          '.OO..',
          '.O...',
          '.....']]

    I = [['..O..',
          '..O..',
          '..O..',
          '..O..',
          '.....'],
         ['.....',
          '.....',
          'OOOO.',
          '.....',
          '.....']]
    
    O = ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']

    J = [['.....',
          '.O...',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..OO.',
          '..O..',
          '..O..',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '...O.',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '.OO..',
          '.....']]

    L = [['.....',
          '...O.',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..O..',
          '..OO.',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '.O...',
          '.....'],
         ['.....',
          '.OO..',
          '..O..',
          '..O..',
          '.....']]

    T = [['.....',
          '..O..',
          '.OOO.',
          '.....',
          '.....'],
         ['.....',
          '..O..',
          '..OO.',
          '..O..',
          '.....'],
         ['.....',
          '.....',
          '.OOO.',
          '..O..',
          '.....'],
         ['.....',
          '..O..',
          '.OO..',
          '..O..',
          '.....']]
    
    return [S, Z, I, O, J, L, T]

# selects a shape
def randomShape():
    global board_y, board_x
    board_y = 0
    board_x = 3
    SHAPES = blockShape()
    # chose one of the shape rotations
    shape_rotations = random.choice(SHAPES)
    # if the shape rotation is a square
    if shape_rotations == SHAPES[3]:
        shape = shape_rotations
    else:
        shape = random.choice(shape_rotations)
    return(shape)

# rotates the block
def rotateShape(shape, SHAPES):
    if shape != SHAPES[3]:
        for i in range(len(SHAPES)):
            for t in range(len(SHAPES[i])):
                if SHAPES[i][t] == shape:
                    shape = SHAPES[i][(t + 1) % len(SHAPES[i])]
                    return(shape)
    return(shape)

def newBoard():
    board = [[0 for x in range(board_row)] for y in range(board_line)]
    return (board)

def checkForFirst(shape):
    for line in range(TEMPLATEHEIGHT):
        for row in range(TEMPLATEWIDTH):
            if shape[line][row] == 'O':
                return(line)

# puts the block matrix into the board matrix
def putInBoard(board, shape, start_line, board_x, board_y):
    for line in range(len(shape)):
        for row in range(len(shape[line])):
            if shape[line][row] == 'O':
                board[board_y + (line - start_line)][board_x + row] = 1
    return(board)
    
def removeFromBoard(board, index):
    global iteration
    for line in range(board_line):
        for row in range(board_row):
            if board[line][row] == 1:
                if iteration == 2:
                    board[line][row] = index
                elif iteration != 2:
                    board[line][row] = 0
    return(board)

def checkFullLine(board):
    global line_filled, full_line
    for line in range(board_line):
        filled = 0
        for row in range(board_row):
            if board[line][row] != 0 and board[line][row] != 1:
                filled += 1
                if filled == 10:
                    full_line = line
                    line_filled = True
                    return(line_filled, full_line)

def deleteLine(board, full_line):
    global line_num, line_filled
    for line in range(full_line):
        line = full_line - line
        for row in range(board_row):
            #if board[line][row] != 0 and board[line][row] != 1:
            board[line][row] = board[line - 1][row]
    line_filled = False
    return(board, line_filled)
                
# check if rotating is possible
def checkRotate(board_x, board_y):
    test_shape = rotateShape(shape, SHAPES)
    for line in range(len(test_shape)):
        for row in range(len(test_shape[line])):
            if test_shape[line][row] == 'O':
                # stop rotation out of board
                if board_x + row < 0 or board_x + row > board_row - 1 or board_y + line > board_line - 1:
                    return(False)
                # stop rotation into a block
                elif board[board_y + line][board_x + row] != 0 and board[board_y + (line - start_line)][board_x + row] != 1:
                    return(False)
    return(True)

def collisionDetection(board):
    global right_collision, left_collision, bottom_collision
    for row in range(board_row):
        for line in range(board_line):
            if board[board_line - 1][row] == 1:
                bottom_collision = True
            if board[line][board_row - 1] == 1:
                right_collision = True
            if board[line][0] == 1:
                left_collision  = True
            if board[(line + 1) % board_line][row] != 0 and board[(line + 1) % board_line][row] != 1 and board[line][row] == 1:
                bottom_collision = True
            if (board[line][(row - 1) % board_row] != 0 and board[line][(row - 1) % board_row] != 1 and board[line][row] == 1) or ((board[line][(row - 1) % board_row] != 0 and board[line][(row - 1) % board_row] != 1 and board[line][row] == 1) and (board[(line + 1) % board_line][(row - 1) % board_row] != 0 and board[(line + 1) % board_line][(row - 1) % board_row] != 1 and board[line][row] == 1)):
                left_collision = True
            if (board[line][(row + 1) % board_row] != 0 and board[line][(row + 1) % board_row] != 1 and board[line][row] == 1) or ((board[line][(row + 1) % board_row] != 0 and board[line][(row + 1) % board_row] != 1 and board[line][row] == 1) and (board[(line + 1) % board_line][(row + 1) % board_row] != 0 and board[(line + 1) % board_line][(row + 1) % board_row] != 1 and board[line][row] == 1)):
                right_collision = True
    return(right_collision, left_collision, bottom_collision)

def collorIndex():
    index = random.randint(2, 7)
    return(index)
    
def drawBoard():
    global COLLORS, playing, on_play
    if playing:
        windowSurface.blit(background_image, (background_left, background_top))
        #windowSurface.blit(board_image, (board_left, board_top))
        for line in range(board_line):
            for row in range(board_row):
                if board[line][row] in COLLORS:
                    sq_left = board_left + ((sq_size) * row)
                    sq_top = board_top + ((sq_size) * line)
                    image = pygame.transform.scale(COLLORS[board[line][row]], (sq_size, sq_size))
                    board_block = windowSurface.blit(image, (sq_left, sq_top))
    elif game_end:
        windowSurface.blit(end_image, (board_left, board_top))
    else:
        windowSurface.blit(background_image, (background_left, background_top))
        windowSurface.blit(menu_image, (board_left, board_top))
        if not on_play:
            windowSurface.blit(play_image, (play_left, play_top))
        elif on_play:
            windowSurface.blit(play_light, (play_left, play_top))
        if not on_quit:
            windowSurface.blit(quit_image, (quit_left, quit_top))
        elif on_quit:
            windowSurface.blit(quit_light, (quit_left, quit_top))
    windowSurface.blit(level_image, (interface_left, level_top))
    windowSurface.blit(score_image, (interface_left, score_top))
    windowSurface.blit(lines_image, (interface_left, lines_top))

def drawNumbers(numbers, top_coord):
    i = 1
    score = int(numbers)
    for number in str(score):
        number = int(number)
        
        # determine number coordinates
        number_left = interface_left + sq_size * i + 2
        number_top = top_coord + sq_size

        number_image = pygame.transform.scale(NUMBERS[number], (letter_size, letter_size))
        windowSurface.blit(number_image, (number_left, number_top))
        i += 1

# draws the block on the board
def drawBlock(shape, index):
    image = pygame.transform.scale(COLLORS[index], (sq_size, sq_size))
    show_image = pygame.transform.scale(COLLORS[next_index], (int(sq_size / 1.2), int(sq_size / 1.2)))
    for line in range(len(shape)):
        for row in range(len(shape[line])):
            # draws the block from the template
            if shape[line][row] == 'O':
                sq_left = board_left + ((sq_size) * (board_x + row))
                sq_top = board_top + ((sq_size) * (board_y + (line - start_line)))
                block = windowSurface.blit(image, (sq_left, sq_top))

            if next_shape[line][row] == 'O':
                left_show = background_left + sq_size * 15.2 + (int(sq_size / 1.2) * row)
                top_show = background_top + sq_size * 2.8 + (int(sq_size / 1.2) * line)
                block_show = windowSurface.blit(show_image, (left_show, top_show))

def scoringSystem(line_num):
    global score
    score += every_piece
    if line_num == 1:
        score += one_line
    elif line_num == 2:
        score += two_lines
    elif line_num == 3:
        score += three_lines
    elif line_num == 4:
        score += four_lines
    for line in range(board_line):
        for row in range(board_row):
            if (board[line][row] != 0 or board[line][row] != 1) or (line == board_line and row == board_row):
                return(score)
            else:
                score += board_clear
                return(score)

def playerLevel(score):
    global level
    level = int(score / 1000) + 1
    return(level)

def readHighScore():
    global high_score, high_level, high_lines
    text_file = open("High score.txt", 'r')
    high_score = text_file.readline()
    high_level = text_file.readline()
    high_lines = text_file.readline()
    text_file.close

def newHighScore(score, level, total_lines):
    global high_score, high_level, high_lines
    text_file = open("High score.txt", 'w')
    if score > int(high_score):
        high_score = score
    if level > int(high_level):
        high_level = level
    if total_lines > int(high_lines):
        high_lines = total_lines
    text_file.writelines('%d\n' % int(high_score))
    text_file.writelines('%d\n' % int(high_level))
    text_file.writelines('%d' % int(high_lines))
    text_file.close

pygame.mixer.init()
pygame.mixer.music.load('Theme1.mp3')
change_music = False

sound = pygame.mixer.Sound('Crash.wav')

while True:
    # reads high score from a file
    readHighScore()
    
    on_play = False
    on_quit = False

    # variable that starts the game
    playing = False
    # variable that is true when the player clicks
    click = False

    game_end = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            click = True
        elif event.type == MOUSEMOTION:
            x, y = event.pos
    if not playing:
        if x > play_left and x < play_left + play_width and y > play_top and y < play_top + letter_size:
            on_play = True
            if click:
                playing = True
        if x > quit_left and x < quit_left + quit_width and y > quit_top and y < quit_top + letter_size:
            on_quit = True
            if click == True:
                pygame.quit()
                sys.exit()

    drawBoard()
    # draws high, score, level and line
    drawNumbers(high_score, score_top)
    drawNumbers(high_level, level_top)
    drawNumbers(high_lines, lines_top)
    
    # player level
    level = 0
    board = newBoard()
    score = 0
    set_speed = speed_index * max_level
    total_lines = 0

    # sets color index for current and next shape
    index = collorIndex()
    next_index = index

    # sets the current and next shape
    shape = randomShape()
    next_shape = shape

    pygame.display.update()

    if playing:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    while playing:
        windowSurface.fill(BLACK)
        left_collision = False
        right_collision = False
        bottom_collision = False
        index = next_index
        shape = next_shape
        next_index = collorIndex()
        next_shape = randomShape()
        start_line = checkForFirst(shape)
        speed = set_speed
        speed_c = speed_index * (level + 1) * 0.3
        set_shape = False
        rotate_shape = False

        '''if level == 1:
            change_music = True
            if change_music:
                pygame.mixer.music.load('Tetris_End_Round_Dancing_by_ArcadeTunes.com.mp3')
                pygame.mixer.music.play(-1)
                change_music = False'''
            

        # sets movement of the block to default
        move_down = False
        move_left = False
        move_right = False
        fast_move = False
        new_shape = False
        
        iteration = 0
        line_filled = False
        
        # number of lines
        scoringSystem(line_num)
        line_num = 0

        playerLevel(score)
                
        while new_shape == False:
            SHAPES = blockShape()
            click = False
            
            # this variable sets the fall speed of the block
            if fast_move == False:
                speed -= speed_c
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONUP:
                    click = True
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        set_shape = True
                    if event.key == K_UP:
                        rotate_shape = True
                    if event.key == K_LEFT:
                        move_left = True
                    if event.key == K_RIGHT:
                        move_right = True
                    if event.key == K_DOWN:
                        fast_move = True
                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        set_shape = False
                    if event.key == K_UP:
                        rotate_shape = False
                    if event.key == K_LEFT:
                        move_left = False
                    if event.key == K_RIGHT:
                        move_right = False
                    if event.key == K_DOWN:
                        fast_move = False
                        speed = set_speed

            while click:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == MOUSEBUTTONUP:
                        click = False
                windowSurface.blit(pause_game, (board_left, board_top))
                pygame.display.update()

            windowSurface.fill(BLACK)
            if set_shape == True:
                shape = randomShape()
            rotate_speed -= 3
            move_speed -= 5
            if rotate_shape == True:
                rotate_shape = checkRotate(board_x, board_y)
                if rotate_shape == True and rotate_speed < 5:
                    shape = rotateShape(shape, SHAPES)
                    rotate_speed = 15
            start_line = checkForFirst(shape)
            board = putInBoard(board, shape, start_line, board_x, board_y)
            if bottom_collision == True:
                iteration += 1
                bottom_collision = False
                collisionDetection(board)
                if bottom_collision == False:
                    iteration = 0
                elif iteration == 2 and bottom_collision:
                    sound.play()
                    new_shape = True
            collisionDetection(board)
            drawBoard()
            board = removeFromBoard(board, index)
            drawBlock(shape, index)
            drawNumbers(level, level_top)
            drawNumbers(score, score_top)
            drawNumbers(total_lines, lines_top)

            # every third iteration of the spped variable
            # triggers falling
            if bottom_collision == False and (speed < set_speed - max_level or fast_move == True):
                board_y += 1
                speed = set_speed
            if move_speed < 8:
                if move_left == True and left_collision == False:
                    board_x -= 1
                if move_right == True and right_collision == False:
                    board_x += 1
                move_speed = 15

            # sets the collision of the block to default
            left_collision = False
            right_collision = False


            checkFullLine(board)
            while line_filled:
                line_num += 1
                deleteLine(board, full_line)
                checkFullLine(board)
                total_lines += 1

            for row in range(board_row):
                if board[0][row] != 0 and board[0][row] != 1:
                    newHighScore(score, level, total_lines)
                    game_end = True
                    playing = False
                    while game_end:
                        click = False
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == MOUSEBUTTONUP:
                                click = True
                        drawBoard()
                        drawNumbers(level, level_top)
                        drawNumbers(score, score_top)
                        drawNumbers(total_lines, lines_top)
                        pygame.display.update()
                        if click:
                            game_end = False
                
            pygame.display.update()
            mainClock.tick(FPS)

