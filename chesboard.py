
class ChessBoard:
    def __init__(self, chessboard=None):
        if chessboard is None:
            self.__chessboard = []
        else:
            self.__chessboard = chessboard
    
    def create_chessboard(self):
        
        number = 1
        row_number = 1
        for f in range(0,8):
            if row_number == 1:
                number = 1
                row_number = 0
            elif row_number == 0:
                number = 0
                row_number = 1
            new_row = []
            for i in range(0,8):
                if number == 1:
                    new_row.append(number)
                    number -= 1
                elif number == 0:
                    new_row.append(number)
                    number += 1
            self.__chessboard.append(new_row)        

    def fill_chessboard(self):
        for i in range(8):
            if i == 0 or i == 7:
                if i == 0:
                    owner = 1
                else:
                    owner = 0
                self.__chessboard[i][0] = Rook(owner, (i,0))
                self.__chessboard[i][1] = Horse(owner, (i,1))
                self.__chessboard[i][2] = Bishop(owner, (i,2))
                self.__chessboard[i][3] = Queen(owner, (i,3))
                self.__chessboard[i][4] = King(owner, (i,4))
                self.__chessboard[i][5] = Bishop(owner, (i,5))
                self.__chessboard[i][6] = Horse(owner, (i,6))
                self.__chessboard[i][7] = Rook(owner, (i,7))
            if i == 1 or i == 6:
                if i == 1:
                    owner = 1
                else:
                    owner = 0
                for f in range(8):
                    self.__chessboard[i][f] = Pawn(owner, (i,f))

        return self

    @property
    def chessboard(self):
        return self.__chessboard
    
    @chessboard.setter
    def chessboard(self, matrice:list):
        self.__chessboard = matrice

    def print_chessboard(self):
        #formatting the chessboard
        row_letters = "ABCDEFGH"
        row_numbers = "87654321"
        matrice = self.__chessboard
        row = (value for value in row_letters)
        row1 = (value for value in row_numbers)
        format1 = "_"
        format2 = "|____"
        print(f"{format1*41}")

        for item in matrice:
                
                for number in item:
                #prints 0 for empty white square, 1 for empty black square
                    if number ==0 or number == 1:
                        print(f"| {number:<2} ", end="")
                    else:
                        print("|", number, "",end="")
                print("|" + next(row1))
                
                print(f"{format2*8}|")
        for i in range(1,9):
            print(f"  {next(row)}  ", end="")
                
    
    def process_move(self, input:str):
        #changes chess notation into numbers, derives coordinates for start and end of move,
        # exports them as nested tuple
        dict_of_square_letter = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
        dict_of_square_number = {"8":0,"7":1,"6":2,"5":3,"4":4,"3":5,"2":6,"1":7}

        move = input.split(" ")
        starting_square = dict_of_square_number[move[0][1]], dict_of_square_letter[move[0][0]]
        ending_square =  dict_of_square_number[move[1][1]], dict_of_square_letter[move[1][0]]

        return starting_square, ending_square
    
    def all_legal_moves(self, owner:int):
        all_moves = []
        for row in self.chessboard:
            for square in row:
                if type(square) != int and square.owner == owner and type(square) != King:
                    moves, bool = square.legal_moves(self)
                    if type(moves) == list:
                        all_moves += moves
               
        return all_moves

    def promote(self, coords:tuple):
        x,y = coords
        print("promote by typing H - Horse etc.")
        while True:
            new_piece = input("What piece do you promote to:")
            if new_piece == "H":
                self.chessboard[x][y] = Horse(self.chessboard[x][y].owner, (x,y))
                break
            elif new_piece == "R":
                self.chessboard[x][y] = Rook(self.chessboard[x][y].owner, (x,y))
                break
            elif new_piece == "B":
                self.chessboard[x][y] = Bishop(self.chessboard[x][y].owner, (x,y))
                break
            elif new_piece == "Q":
                self.chessboard[x][y] = Queen(self.chessboard[x][y].owner, (x,y))
                break
            else:
                print("invalid piece initial")
    
    def kill_peasant(self, en_peasant:str, coords:tuple):
        x,y = coords
        if en_peasant == "white left" or en_peasant == "white right":
            return (x+1,y)
        elif en_peasant == "black left" or en_peasant == "black right":
            return (x-1,y) 
    
    def in_check(self, owner, chessboard:list):
        new_board = ChessBoard(chessboard)
        for item in new_board.all_legal_moves(owner):
            x,y = item
            if type(self.chessboard[x][y]) is King:
                return True
        return False

    def would_be_check(self, move_made:tuple, turn, starting_board):
        #importing and converting all data about move made 
        start_square, end_square = move_made
        x,y = start_square
        a,b = end_square
        new_board = []
        
        #creating independable list to NOT modify the existing self.chessboard
        for row in self.chessboard:
            new_row = []
            for item in row:
                new_row.append(item)
            new_board.append(new_row)
        #changing the chessboard according to user's input
        gamestate = new_board
        gamestate[a][b] = gamestate[x][y]
        gamestate[x][y] = starting_board[x][y]
        #checking if the returned position is legal, that is, king wouldnt be self-mated
        if self.in_check((turn+1)%2, gamestate):
            return False
        return True


    
        
class Piece:
    def __init__(self, owner:int, position:tuple):
        self.__owner = owner
        self.__position = position

    def __str__(self):
        return f"{self.__class__.__name__[0]}{self.__owner}"
    
    @property
    def owner(self):
        return self.__owner
    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self, coords:tuple):
        self.__position = coords


class Horse(Piece):
    def __init__(self, owner:int, position:tuple):
        super().__init__(owner, position)

    def legal_moves(self, chessboard:ChessBoard):
        x,y = self.position

        list_of_all_moves = [(x-2,y-1),(x-2,y+1),(x-1,y+2),
        (x-1, y-2),(x+1,y-2),(x+1,y+2),(x+2,y+1),(x+2,y-1)]

        moves_in_board = []

        for item in list_of_all_moves:
            a,b = item
            #if move would lead to an empty square 
            #or a square controlled by enemy it is allowed
            #moves that would lead out of chessboard, are ommited by try:except
            try:
                if a>= 0 and b >=0:
                    if type(chessboard.chessboard[a][b]) is int:
                        moves_in_board.append(item)
                    elif chessboard.chessboard[a][b].owner != self.owner:
                        moves_in_board.append(item)

            except IndexError:
                continue

        return moves_in_board, None


class Rook(Piece):
    def __init__(self, owner:int, position:tuple):
        super().__init__(owner, position)
    
    def legal_moves(self, chessboard:ChessBoard):
        list_of_all_moves = []
        x,y = self.position
        #check for collision in every of the 4 cardinal directions
        for i in range(x+1, 8):
            if issubclass(type(chessboard.chessboard[i][y]),Piece):
                #if collision is with enemy, move is possible
                if chessboard.chessboard[i][y].owner != self.owner:
                    list_of_all_moves.append((i, y)) 
                break
            list_of_all_moves.append((i,y))

        for i in range(y+1, 8):
            if issubclass(type(chessboard.chessboard[x][i]),Piece):
                if chessboard.chessboard[x][i].owner != self.owner:
                    list_of_all_moves.append((x, i))
                break
            list_of_all_moves.append((x,i))

        for i in range(x-1, 0, -1):
            if issubclass(type(chessboard.chessboard[i][y]),Piece):
                if chessboard.chessboard[i][y].owner != self.owner:
                    list_of_all_moves.append((i, y))  
                break
            list_of_all_moves.append((i,y))

        for i in range(y-1, 0, -1):
            if issubclass(type(chessboard.chessboard[x][i]),Piece):
                if chessboard.chessboard[x][i].owner != self.owner:
                    list_of_all_moves.append((x, i))
                break
            list_of_all_moves.append((x,i))
        return list_of_all_moves, None


class Bishop(Piece):
    def __init__(self, owner:int, position:tuple):
        super().__init__(owner, position)
    
    def legal_moves(self, board:ChessBoard):
        x,y = self.position
        list_of_all_moves = []
        chessboard = board.chessboard
        #for every diagonall, check collision
        #north diagonals
        for i in range(x-1, 0, -1):
            try:
                
                if issubclass(type(chessboard[i][y-(x-i)]),Piece):
                    #if collision is with enemy, move is possible
                    if chessboard[i][y-(x-i)].owner != self.owner: 
                        list_of_all_moves.append((i,y-(x-i)))
                    break
                list_of_all_moves.append((i,y-(x-i))) 

            except IndexError:
                continue

        for i in range(x-1, 0, -1):
            try:

                if issubclass(type(chessboard[i][y+(x-i)]),Piece):
                    if chessboard[i][y+(x-i)].owner != self.owner:
                        list_of_all_moves.append((i, y+(x-i)))
                    break
                list_of_all_moves.append((i,y+(x-i))) 

            except IndexError:
                continue

        #south diagonals
        for i in range(x+1, 8):

            try:
                if issubclass(type(chessboard[i][y-(i-x)]),Piece):
                    if chessboard[i][y-(i-x)].owner != self.owner:
                        list_of_all_moves.append((i, y-(i-x)))
                    break
                list_of_all_moves.append((i,y-(i-x))) 

            except IndexError:
                continue

        for i in range(x+1, 8):
            try:

                if issubclass(type(chessboard[i][y+(i-x)]),Piece):
                    if chessboard[i][y+(i-x)].owner != self.owner:
                        list_of_all_moves.append((i, y+(i-x)))
                    break
                list_of_all_moves.append((i,y+(i-x))) 

            except IndexError:
                continue   

        return list_of_all_moves, None                 
    

class King(Piece):
    def __init__(self, owner:int, position:tuple):
        super().__init__(owner, position)
    
    def legal_moves(self, chessboard:ChessBoard):
        chessboard_positions = chessboard.chessboard
        x,y = self.position
        list_of_all_moves = [(x-1,y-1),(x-1,y),(x-1,y+1),
        (x, y-1),(x,y+1),(x+1,y-1),(x+1,y+1),(x+1,y)]
        moves_in_board = []
        

        for item in list_of_all_moves:
            a,b = item
            #if move would lead to an empty square 
            #or a square controlled by enemy it is allowed
            #moves that would lead out of chessboard, are ommited by try:except
            try:
                if type(chessboard_positions[a][b]) is int:
                    moves_in_board.append(item)
                elif chessboard_positions[a][b].owner != self.owner:
                    moves_in_board.append(item)
            except IndexError:
                continue
        if self.owner == 1:
            enemy_moves = chessboard.all_legal_moves(0)
        elif self.owner == 0:
            enemy_moves = chessboard.all_legal_moves(1)

        return [item for item in moves_in_board if item not in enemy_moves], None


class Queen(Piece):
    def __init__(self, owner:int, position:tuple):
        super().__init__(owner, position)
    
    def legal_moves(self, chessboard:ChessBoard):
        new_bishop = Bishop(self.owner, self.position)
        new_rook = Rook(self.owner, self.position)
        queen_moves = new_bishop.legal_moves(chessboard)+ new_rook.legal_moves(chessboard)
        return queen_moves, None


class Pawn(Piece):
    def __init__(self, owner:int, position:tuple,last_position:tuple = None):
        super().__init__(owner, position)
    
    def legal_moves(self, board:ChessBoard):
        chessboard = board.chessboard
        x,y = self.position
        en_peasant = None
        #black pawn moves
        if self.owner == 1:
            list_of_all_moves= []
            #normal movement
            try:
                if type(chessboard[x+1][y]) is int:
                    list_of_all_moves.append((x+1,y))
                    #can make a double move from starting position
                    if x == 1 and type(chessboard[x+2][y]) is int:
                        list_of_all_moves.append((x+2,y))
                #taking oponent's pieces diagonaly
            except (IndexError, AttributeError):
                pass
            try:
                if chessboard[x+1][y-1].owner == 0:
                        list_of_all_moves.append((x+1,y-1))
            except (IndexError, AttributeError):
                pass
            try:
                if chessboard[x+1][y+1].owner == 0:
                        list_of_all_moves.append((x+1,y+1))
            except (IndexError, AttributeError):
                pass
            if x == 4:
                try:
                    if type(board.chessboard[4][y-1]) is Pawn:
                        if board.chessboard[4][y-1].last_position == (6,y-1):
                            list_of_all_moves.append((5,y-1))
                            en_peasant = "black left"
                except IndexError:
                    pass

                try:
                    if type(board.chessboard[4][y+1]) is Pawn:
                        if board.chessboard[4][y+1].last_position == (6,y+1):
                            list_of_all_moves.append((5,y+1))
                            en_peasant = "black right"
                except IndexError:
                    pass
        #white pawn moves, same as above but towards different sides of the board
        elif self.owner == 0:
            list_of_all_moves = []
            if type(chessboard[x-1][y]) is int:
                list_of_all_moves.append((x-1,y))
                if x == 6 and type(chessboard[x-2][y]) is int:
                    list_of_all_moves.append((x-2,y))
            
            try:
                if chessboard[x-1][y-1].owner == 1:
                    list_of_all_moves.append((x-1,y-1))
            except (IndexError, AttributeError):
                pass
            try:
                if chessboard[x-1][y+1].owner == 1:
                    list_of_all_moves.append((x-1,y+1))
            except (IndexError, AttributeError):
                pass
            
            if x == 3:
                try:
                    
                    if type(board.chessboard[3][y-1]) is Pawn:
                        if board.chessboard[3][y-1].last_position == (1,y-1):
                            list_of_all_moves.append((2,y-1))
                            en_peasant = "white left"
                except IndexError:
                    pass
                try:
                    
                    if type(board.chessboard[3][y+1]) is Pawn:
                        if board.chessboard[3][y+1].last_position == (1,y+1):
                            list_of_all_moves.append((2,y+1))
                            en_peasant = "white right"
                except IndexError:
                    pass
                
        return list_of_all_moves, en_peasant
    
    


class ChessApp:
    def __init__(self):
        self.starting_board = ChessBoard()

    def start_game(self):
        self.current_board = ChessBoard()
        self.current_board.create_chessboard()
        self.starting_board.create_chessboard()
        self.current_board = self.current_board.fill_chessboard()
        gamestate = self.current_board.chessboard
        base_board = self.starting_board.chessboard
        turn = 0
        print()
        print("input form: a1 h8")
        print("first part declares chosen piece, second part declares new location for it")
        while True:
            if self.check_material():
                print("game ended, draw by insufficient material")
            if len(self.current_board.all_legal_moves(0)+self.current_board.all_legal_moves(1)) == []:
                print("game ended, draw by stalemate")
                break
            self.check_promotion()
            self.current_board.print_chessboard()
            print()
            try:
                if turn %2== 0:
                    move0 = input("White, make your move:")
                    move_made = self.current_board.process_move(move0)
                elif turn %2!= 0:
                    move1 = input("Black, make your move:")
                    move_made = self.current_board.process_move(move1)
            except (IndexError, KeyError):
                print("invalid input")
                continue
            start_square, end_square = move_made
            x,y = start_square
            a,b = end_square
            if type(gamestate[x][y]) is int:
                print("you chose empty square")
            else:
                if gamestate[x][y].owner == turn%2:
                    if self.current_board.would_be_check(move_made, turn%2,self.starting_board.chessboard):
                        move_list, en_peasant = gamestate[x][y].legal_moves(self.current_board)

                        if end_square in move_list:
                            if type(gamestate[a][b]) is King:
                                print()
                                print()
                                print()
                                if gamestate[x][y].owner == 1:
                                    print("Black won the game by taking the King!")
                                elif gamestate[x][y].owner == 0:
                                    print("White won the game by taking the King!")
                                break
                            if type(gamestate[x][y]) is Pawn:
                                gamestate[x][y].last_position = (x,y)
                            gamestate[a][b] = gamestate[x][y]
                            gamestate[a][b].position = (a,b)
                            gamestate[x][y] = base_board[x][y]
                            if en_peasant is not None:
                                p,o = self.current_board.kill_peasant(en_peasant, (a,b))
                                gamestate[p][o] = base_board[p][o]
                            turn += 1
                        else:
                            print("invalid move")
                    else:
                        print("this move would forfeit your king")
                else: print("this piece doesn't belong to you")

    def check_material(self):
        all_squares = []
        for item in self.current_board.chessboard:
            all_squares += item
        all_pieces = [item for item in all_squares if type(item) is not int]
        if sum(isinstance(i, Pawn) for i in all_pieces) == 0:
            if sum(isinstance(i, Queen) for i in all_pieces) == 0:
                if sum(isinstance(i, Rook) for i in all_pieces) == 0:
                    if sum(isinstance(i, Horse) for i in all_pieces) + sum(isinstance(i, Bishop) for i in all_pieces) < 2:
                        return True
        return False                    
                    
    def check_promotion(self):
        gamestate = self.current_board.chessboard
        for i in range(8):
            if type(gamestate[0][i]) is Pawn:
                self.current_board.promote((0, i))
        for i in range(8):
            if type(gamestate[7][i]) is Pawn:
                self.current_board.promote((7, i))
    
         

new_game = ChessApp()
new_game.start_game()