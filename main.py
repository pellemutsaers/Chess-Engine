import pygame, chess, random, time

display_size_x, display_size_y = 480, 480 + 32
pygame.init()
display = pygame.display.set_mode((display_size_x, display_size_y))
tile_colour_black = (115, 85, 70)
tile_colour_white = (235, 210, 180)
base_font = pygame.font.Font(None, 32)
pygame.display.set_caption("Chess")
search_depth = 1
global movenumber


random_fen = "7r/1P2p3/3bB2N/3K2pp/4P3/5PR1/kP2pP2/8 w KQkq - 0 1"
chess960 = "qbbrnnkr/pppppppp/8/8/8/8/PPPPPPPP/QBBRNNKR b KQkq - 0 1"
drawn_fen = "8/8/8/8/8/6Q1/8/7k w - - 0 1"
board = chess.Board()

def drawBoard():
    for x in range(0, 8):
        for y in range(0, 8):
            if (x + y) % 2 == 1:
                pygame.draw.rect(display, tile_colour_black , pygame.Rect(x*(display_size_x/8), y*((display_size_y-32)/8), display_size_x/8, (display_size_y-32)/8))
            if (x + y) % 2 == 0: 
                pygame.draw.rect(display, tile_colour_white , pygame.Rect(x*(display_size_x/8), y*((display_size_y-32)/8), display_size_x/8, (display_size_y-32)/8))
    #pygame.display.flip()

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

#######



def Evaluate(move, movehm, movenumber):
    evaluation = 0
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

    for column in columns:
        for index, i in enumerate(columns[column]):
            if i.isdigit():
                j = int(i)
                columns[column].pop(index)
                for ii in range(j):
                    columns[column].insert(index+ii, " ")

    for columnval, column in enumerate(columns):
        for index, j in enumerate(columns[column]):
            index += 1

            if j == "R":
                evaluation += 5
                if columnval <= 4:
                    evaluation += 1.8 - 0.2*(columnval+1)

            elif j == "K":
                if index < 3 or index > 6:
                    evaluation += 1


            elif j == "N":
                evaluation += 3
                evaluation += 1.8 - 0.2*(columnval+1)
                if index >= 3 or index <= 6:
                    evaluation += 0.5

            elif j == "B":
                evaluation += 3
                evaluation += 1.8 - 0.2*(columnval+1)

            elif j == "Q":
                evaluation += 9
                evaluation += 1.8 - 0.2*(columnval+1)

            elif j == "P":
                evaluation += 1
                evaluation += 1.8 - 0.2*(columnval+1)

#-----------------------------------------------#
            elif j == "r":
                evaluation -= 5
                if columnval >= 3:
                    evaluation -= 0.2*(columnval + 1)

            elif j == "k":
                if index < 3 or index > 6:
                    evaluation -= 1

            elif j == "n":
                evaluation -= 3
                evaluation -= 0.2*(columnval + 1)
                if index >= 3 or index <= 6:
                    evaluation -= 0.5
            
            elif j == "b":
                evaluation -= 3
                evaluation -= 0.2*(columnval + 1)                

            elif j == "q":
                evaluation -= 9
                evaluation -= 0.2*(columnval + 1)        

            elif j == "p":
                evaluation -= 1
                evaluation -= 0.2*(columnval + 1)

    if board.is_checkmate():
        if movenumber % 2 == 0:
            evaluation = 1000
        else:
            evaluation = -1000

    if board.is_insufficient_material() or board.is_stalemate() or board.can_claim_threefold_repetition():
        evaluation = 0

    return evaluation


def getLegalMoves():
    legal_moves = str(board.legal_moves)
    legal_moves = legal_moves.split(' ')[3::]
    removetable = str.maketrans(" ", " ", "<>(),")
    legal_moves = [s.translate(removetable) for s in legal_moves]
    legal_moves1 = random.sample(legal_moves, len(legal_moves))
    return legal_moves1

def getMove(movenumber):

    running = True

    while running:
        if movenumber % 2 == 0:
            Evaluate("", "", movenumber)
            legal_moves1 = getLegalMoves()
            listOfEvals2 = []

            for i in legal_moves1:
                try:
                    board.push_san(i)
                except:
                    running = False
                    break
                legal_moves2 = getLegalMoves()
                listOfEvals1 = []

                for ii in legal_moves2:

                    try:
                        board.push_san(ii)
                    except:
                        running = False
                        break

                    layer2 = Evaluate(ii, i, movenumber)

                    listOfEvals1.append(layer2)
                    board.pop()

                listOfEvals2.append(min(listOfEvals1))

                board.pop()
            
            best_move = legal_moves1[listOfEvals2.index(max(listOfEvals2))]
            print(max(listOfEvals2))
            
            running = False

        else:
            Evaluate("", "", movenumber)
            legal_moves1 = getLegalMoves()
            listOfEvals2 = []

            for i in legal_moves1:
                try:
                    board.push_san(i)
                except:
                    running = False
                    break
                legal_moves2 = getLegalMoves()
                listOfEvals1 = []

                for ii in legal_moves2:

                    try:
                        board.push_san(ii)
                    except:
                        running = False
                        break

                    layer2 = -Evaluate(ii, i, movenumber)

                    listOfEvals1.append(layer2)
                    board.pop()

                listOfEvals2.append(min(listOfEvals1))

                board.pop()
            
            best_move = legal_moves1[listOfEvals2.index(max(listOfEvals2))]
            print(-max(listOfEvals2))
            running = False

    return best_move
                
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

def main():
    drawBoard()
    printFen(True)
    time.sleep(0.5)
    running = True
    White_Is_Computer = True
    Black_Is_Computer = True
    user_text = ""
    movenumber = 0
    Finished = False

    while running:

        if movenumber % 2 == 0:
            WhiteToMove = True
        else:
            WhiteToMove = False
        Human_move = False
        Computer_move = False
        if WhiteToMove:
            if White_Is_Computer:
                Computer_move = True
            elif Black_Is_Computer:
                Human_move = True
        else:
            if Black_Is_Computer:
                Computer_move = True
            elif White_Is_Computer:
                Human_move = True
            
        if Human_move and not Finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]

                    elif event.key == pygame.K_SPACE:

                        try:
                            board.push_san(user_text)
                            movenumber += 1
                            printFen(True)
                        except:
                            print("Illegal move")
                        
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

                    else:
                        user_text += event.unicode

        if Computer_move and not Finished:
            move = getMove(movenumber)

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

                if WhiteToMove:
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
            running = False
            
if __name__ == "__main__":
    main()