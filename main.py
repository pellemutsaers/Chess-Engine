import pygame, chess, random, time, math
from colorama import Fore
import chess.pgn

white_is_computer = input("Enter if white should be played by the computer (Y/N): ")
if white_is_computer == "Y":
    white_is_computer = True
elif white_is_computer == "N":
    white_is_computer = False

black_is_computer = input("Enter if black should be played by the computer (Y/N): ")
if black_is_computer == "Y":
    black_is_computer = True
elif black_is_computer == "N":
    black_is_computer = False

display_size_x, display_size_y = 480, 480 + 32
pygame.init()
display = pygame.display.set_mode((display_size_x, display_size_y))
tile_colour_black = (115, 85, 70)
tile_colour_white = (235, 210, 180)
base_font = pygame.font.Font(r"Font\GothamRoundedMedium_21022.ttf", 32)
pygame.display.set_caption("Chess")
number_evals = 0


random_fen = "7r/1P2p3/3bB2N/3K2pp/4P3/5PR1/kP2pP2/8 w KQkq - 0 1"
random_fen2 = "rn1r2k1/pppq2pp/3b1n2/3Pp1N1/5pP1/2N2Q2/PPPP1P1P/R1B1R1K1 w - - 0 1"
chess960 = "qbbrnnkr/pppppppp/8/8/8/8/PPPPPPPP/QBBRNNKR b KQkq - 0 1"
won_fen = "8/Q7/8/8/8/3K4/8/5k2 w - - 0 1"
board = chess.Board()
game = chess.pgn.Game()

def drawBoard():
    for x in range(0, 8):
        for y in range(0, 8):
            if (x + y) % 2 == 1:
                pygame.draw.rect(display, tile_colour_black , pygame.Rect(x*(display_size_x/8), y*((display_size_y-32)/8), display_size_x/8, (display_size_y-32)/8))
            if (x + y) % 2 == 0: 
                pygame.draw.rect(display, tile_colour_white , pygame.Rect(x*(display_size_x/8), y*((display_size_y-32)/8), display_size_x/8, (display_size_y-32)/8))

#Pieces:
whitePawn = pygame.image.load("PNG's\White_pawn.png")
whiteRook = pygame.image.load("PNG's\White_rook.png")
whiteKnight = pygame.image.load("PNG's\White_knight.png")
whiteBishop = pygame.image.load("PNG's\White_bishop.png")
whiteQueen = pygame.image.load("PNG's\White_queen.png")
whiteKing = pygame.image.load("PNG's\White_king.png")

blackPawn = pygame.image.load("PNG's\Black_pawn.png")
blackRook = pygame.image.load("PNG's\Black_rook.png")
blackKnight = pygame.image.load("PNG's\Black_knight.png")
blackBishop = pygame.image.load("PNG's\Black_bishop.png")
blackQueen = pygame.image.load("PNG's\Black_queen.png")
blackKing = pygame.image.load("PNG's\Black_king.png")

def splitString(string):
    return [char for char in string]

def getSquare():
    mouseposition = pygame.mouse.get_pos()
    row = chr(97 + math.floor(mouseposition[0]/60))
    column = str(1 + math.floor((480 - mouseposition[1])/60))
    return (row+column)

def printFen(print):
    fen_split_on_slash = board.fen().split("/")
    fen_split = fen_split_on_slash[0:7] + fen_split_on_slash[7].split()

    columns = {
        "column1" : splitString(fen_split[0]),
        "column2" : splitString(fen_split[1]),
        "column3" : splitString(fen_split[2]),
        "column4" : splitString(fen_split[3]),
        "column5" : splitString(fen_split[4]),
        "column6" : splitString(fen_split[5]),
        "column7" : splitString(fen_split[6]),
        "column8" : splitString(fen_split[7])
    }

#Credit to GijsPeletier
    for column in columns:
        for index, i in enumerate(columns[column]):
            if i.isdigit():
                j = int(i)
                columns[column].pop(index)
                for ii in range(j):
                    columns[column].insert(index+ii, " ")
#        print(columns[column])
#End of credit to GijsPeletier

    if print:
        for column_val, column in enumerate(columns):
            for index, j in enumerate(columns[column]):
                drawPieces(j, index, column_val)
            pygame.display.flip()

def frmstr(n):
    n = round(n,4)
    s = f"{n:#05.5g}"
    if "-" not in s:
        s = " "+s
    return s[0:6]

def loadBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '#'):
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '.' * (length - filledLength)
    print(f'\r{prefix} | {bar} | {percent} % {suffix}',end = '\r')
    if iteration == total:
        print()

def distanceFromCenter(row, column):
    row -= 0.5
    column += 0.5
    distX = 4 - row
    distY = 4 - column
    distance = math.sqrt(math.pow(distX, 2)+ math.pow(distY, 2))
    return distance


def Evaluate(movenumber):
    evaluation = 0
    global number_evals
    number_evals += 1
    if board.is_checkmate():
        if movenumber % 2 == 0:
            evaluation = -1000
        else:
            evaluation = 1000

    elif board.is_insufficient_material() or board.is_stalemate() or board.can_claim_threefold_repetition():
        evaluation = 0

    else:
        fen_split_on_slash = board.fen().split("/")
        fen_split = fen_split_on_slash[0:7] + fen_split_on_slash[7].split()
        columns = {
            "column1" : splitString(fen_split[0]),
            "column2" : splitString(fen_split[1]),
            "column3" : splitString(fen_split[2]),
            "column4" : splitString(fen_split[3]),
            "column5" : splitString(fen_split[4]),
            "column6" : splitString(fen_split[5]),
            "column7" : splitString(fen_split[6]),
            "column8" : splitString(fen_split[7])
        }

        for columnval, column in enumerate(columns):
            for index, j in enumerate(columns[column]):
                if j.isdigit():
                    j = int(j)
                    columns[column].pop(index)
                    for i in range(j):
                        columns[column].insert(index + i, " ")

                try:
                    index += 1
                    if j.isupper():
                        if j == "R":
                            evaluation += 5
                            if columnval <= 4:
                                evaluation += 0.9 - 0.1*(columnval+1)

                        elif j == "K":
                            if index < 3 or index > 6:
                                evaluation += 1
                            if movenumber > 50:
                                distance = distanceFromCenter(index, columnval)
                                evaluation -= distance / 4

                        elif j == "N":
                            evaluation += 3
                            evaluation += 0.9 - 0.1*(columnval+1)
                            if index >= 3 or index <= 6:
                                evaluation += 0.5

                        elif j == "B":
                            evaluation += 3
                            evaluation += 0.9 - 0.1*(columnval+1)

                        elif j == "Q":
                            evaluation += 9
                            evaluation += 0.9 - 0.1*(columnval+1)

                        elif j == "P":
                            evaluation += 1
                            evaluation += 0.9 - 0.1*(columnval+1)

                    else:
                        if j == "r":
                            evaluation -= 5
                            if columnval >= 3:
                                evaluation -= 0.1*(columnval+1)

                        elif j == "k":
                            if index < 3 or index > 6:
                                evaluation -= 1
                            if movenumber > 50:
                                evaluation += distance / 4

                        elif j == "n":
                            evaluation -= 3
                            evaluation -= 0.1*(columnval+1)
                            if index >= 3 or index <= 6:
                                evaluation -= 0.5
                        
                        elif j == "b":
                            evaluation -= 3
                            evaluation -= 0.1*(columnval+1)                

                        elif j == "q":
                            evaluation -= 9
                            evaluation -= 0.1*(columnval+1)        

                        elif j == "p":
                            evaluation -= 1
                            evaluation -= 0.1*(columnval+1)
                except:
                    pass

    return evaluation

def getLegalMoves():
    legal_moves = str(board.legal_moves).split(' ')[3::]
    removetable = str.maketrans(" ", " ", "<>(),")
    legal_moves = [s.translate(removetable) for s in legal_moves]
    legal_moves = random.sample(legal_moves, len(legal_moves))
    for index, move in enumerate(legal_moves):
        if "x"in move:
            legal_moves.pop(index)
            legal_moves.insert(0, move)

    #legal_moves.sort(key=len)
    return legal_moves

#---------------------------------------------------------#
def minimax(depth, initial_depth, movenumber, alpha, beta): 
    if depth == 0: 
        return Evaluate(movenumber) 

    if movenumber % 2 == 0: 
        maxEval = -float("inf") 
        legalmoves1 = getLegalMoves()
        if board.legal_moves.count() != 0:
            for index, move in enumerate(legalmoves1): 

                if depth == initial_depth and initial_depth > 3: 
                    loadBar(index + 1, len(legalmoves1), prefix = 'Progress:', suffix = 'Complete', length = 50) 
                board.push_san(move)
                eval = minimax(depth - 1, initial_depth, movenumber + 1, alpha, beta)
                alpha = max(alpha, eval)

                if eval > maxEval and depth != initial_depth: 
                    maxEval = eval

                if eval > maxEval and depth == initial_depth:
                    maxEval = eval
                    best_move = move
                if beta <= alpha:
                    board.pop()
                    return maxEval

                board.pop() 
        else:
            return Evaluate(movenumber)

        if depth == initial_depth:
            if initial_depth > 3: 
                print(f"Positions evaluated: {number_evals}, Evaluation: {frmstr(maxEval)}, depth: {initial_depth}", end = "")
            return (best_move, maxEval)
        else: 
            return maxEval 

    elif movenumber % 2 == 1:
        minEval = float("inf")
        legalmoves2 = getLegalMoves()

        if board.legal_moves.count() != 0: 
            for index, move in enumerate(legalmoves2): 
                if depth == initial_depth and initial_depth > 3: 
                    loadBar(index + 1, len(legalmoves2), prefix = 'Progress:', suffix = 'Complete', length = 50)
                board.push_san(move)
                eval = minimax(depth - 1, initial_depth, movenumber + 1, alpha, beta)
                beta = min(beta, eval)

                if eval < minEval and depth != initial_depth: 
                    minEval = eval 

                elif eval < minEval and depth == initial_depth: 
                    minEval = eval 
                    best_move = move

                if beta <= alpha:
                    board.pop()
                    return minEval

                board.pop() 
        else: 
            return Evaluate(movenumber) 

        if depth == initial_depth:
            if initial_depth > 3:
                print(f"Positions evaluated: {number_evals}, Evaluation: {frmstr(minEval)}, depth: {initial_depth}", end = "")
            return (best_move, minEval)

        else:
            return minEval 
#---------------------------------------------------------------#

def drawPieces(string, index, column):
    if string == " ":
        pass
    elif string == "P":
        display.blit(whitePawn, ((index)*60, (column)*60))
    elif string == "R":
        display.blit(whiteRook, ((index)*60, (column)*60))
    elif string == "N":
        display.blit(whiteKnight, ((index)*60, (column)*60))
    elif string == "B":
        display.blit(whiteBishop, ((index)*60, (column)*60))
    elif string == "Q":
        display.blit(whiteQueen, ((index)*60, (column)*60))
    elif string == "K":
        display.blit(whiteKing, ((index)*60, (column)*60))
    elif string == "p":
        display.blit(blackPawn, ((index)*60, (column)*60))
    elif string == "r":
        display.blit(blackRook, ((index)*60, (column)*60))
    elif string == "n":
        display.blit(blackKnight, ((index)*60, (column)*60))
    elif string == "b":
        display.blit(blackBishop, ((index)*60, (column)*60))
    elif string == "q":
        display.blit(blackQueen, ((index)*60, (column)*60))
    elif string == "k":
        display.blit(blackKing, ((index)*60, (column)*60))

def findMove(depth, start, movenumber, alpha, beta):
    move = minimax(depth, depth, movenumber, alpha, beta)
    if not (time.time() - start > 10) and not move[1] > 999:
        if depth > 3:
            print(" -> searching deeper")
        move = findMove(depth + 1, start, movenumber, alpha, beta)
    return move

def main():
    drawBoard()
    printFen(True)
    time.sleep(0.5)
    running = True
    user_text = ""
    movenumber = 0
    Finished = False
    receiving = True
    alpha = -float("inf")
    beta = float("inf")
    global number_evals

    while running:
        if movenumber % 2 == 0:
            WhiteToMove = True
        else:
            WhiteToMove = False
        Human_move = False
        Computer_move = False
        if WhiteToMove:
            if white_is_computer:
                Computer_move = True
            elif black_is_computer:
                Human_move = True
        else:
            if black_is_computer:
                Computer_move = True
            elif white_is_computer:
                Human_move = True
            
        if Human_move and not Finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and receiving:
                    square1 = getSquare()
                    receiving = False

                elif event.type == pygame.MOUSEBUTTONDOWN and not receiving:
                    square2 = getSquare()
                    receiving = True
                    mousemove = square1 + square2

                    try:
                        board.push_san(mousemove)
                        movenumber += 1
                        printFen(True)
                    except:
                        print(Fore.RED + "Illegal move" + Fore.WHITE)
                    drawBoard()
                    printFen(True)
                    user_text = ""
                    checkmate_status = board.is_checkmate()
                    repetition_status = board.is_stalemate()
                    insufficient_material_status = board.is_insufficient_material()
                    threefold_status = board.can_claim_draw()

                    if checkmate_status == True:
                        if WhiteToMove:
                            user_text = "Black won"
                            Finished = True
                        else:
                            user_text = "White won"
                            Finished = True
                    if repetition_status or insufficient_material_status or threefold_status:
                        user_text = "Draw"
                        Finished = True

                        square1, square2 = "", ""

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == pygame.K_SPACE:

                        try:
                            board.push_san(user_text)
                            movenumber += 1
                        except:
                            print(Fore.RED + "Illegal move" + Fore.WHITE)
                        
                        drawBoard()
                        printFen(True)
                        user_text = ""
                        checkmate_status = board.is_checkmate()
                        repetition_status = board.is_stalemate()
                        insufficient_material_status = board.is_insufficient_material()
                        threefold_status = board.can_claim_draw()

                        if checkmate_status == True:
                            if WhiteToMove:
                                user_text = "White won"
                                Finished = True
                            else:
                                user_text = "Black won"
                                Finished = True
                        if repetition_status or insufficient_material_status or threefold_status:
                            user_text = "Draw"
                            Finished = True

                    else:
                        user_text += event.unicode

        if Computer_move and not Finished:
            depth = 1
            number_evals = 0
            start = time.time()
            move = findMove(depth, start, movenumber, alpha, beta)[0]

            print(f" in: {frmstr(time.time() - start)} seconds")

            try:
                board.push_san(move)
                movenumber += 1
                drawBoard()
            except:
                Finished = True
            printFen(True)

            checkmate_status = board.is_checkmate()
            stalemate_status  = board.is_stalemate()
            insufficient_material_status = board.is_insufficient_material()
            threefold_status = board.can_claim_draw()

            if checkmate_status == True:

                if not  WhiteToMove:
                    user_text = "Black won"
                    Finished = True
                else:
                    user_text = "White won"
                    Finished = True

            if stalemate_status or insufficient_material_status or threefold_status:
                user_text = "Draw"
                Finished = True
                 
            drawBoard()
            printFen(True)

        pygame.draw.rect(display, (50, 50, 50) , pygame.Rect(0, display_size_y-32, display_size_x, display_size_y))
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        display.blit(text_surface, (0, display_size_y-32 + 5))
        pygame.display.flip()

        if Finished:
            closing = str(input("Enter anything to close "))
            print(game)
            running = False
            
if __name__ == "__main__":
    main()