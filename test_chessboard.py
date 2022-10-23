import unittest

from chesboard import *

class TestPieces(unittest.TestCase):
#testing for starting position
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_position_start(self):
        test_game = ChessApp()
        test_game.current_board = ChessBoard()
        test_game.current_board.create_chessboard()
        test_game.current_board.fill_chessboard() 
        gamestate = test_game.current_board.chessboard
        #white pawns
        for i in range(0,8):
            value = []
            tested_piece = gamestate[6][i]

            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            expected_value = [(5,i),(4,i)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #white higher-pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[7][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            if i != 1 and i != 6:
                expected_value = []
            elif i == 1:
                expected_value = [(5,0),(5,2)]
            elif i == 6:
                expected_value = [(5,5),(5,7)]
            
            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #black pawns
        for i in range(0,8):
            value = []
            tested_piece = gamestate[1][i]

            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            expected_value = [(2,i),(3,i)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #black higher-pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[0][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            if i != 1 and i != 6:
                expected_value = []
            elif i == 1:
                expected_value = [(2,2),(2,0)]
            elif i == 6:
                expected_value = [(2,7),(2,5)]
            
            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        print('pieces move correctly in starting positiong')
        
#testing for a position with all pawns moved 1 square
    def test_position_moved_pawn(self):
        test_game = ChessApp()
        test_game.current_board = ChessBoard()
        test_game.current_board.create_chessboard()
        test_game.current_board.fill_chessboard('movedpawn')

        gamestate = test_game.current_board.chessboard
        #white pawns
        for i in range(0,8):
            value = []
            tested_piece = gamestate[5][i]

            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            expected_value = [(4,i)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #white higher-pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[7][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            if i == 0:
                expected_value = [(6,0)]
            if i == 1:
                expected_value = [(6,3)]
            if i == 2:
                expected_value = [(6,1),(6,3)]
            if i == 3:
                expected_value = [(6,2),(6,4),(6,3)]
            if i == 4:
                expected_value = [(6,3),(6,4), (6,5)]
            if i == 5:
                expected_value = [(6,4),(6,6)]
            if i == 6:
                expected_value = [(6,4)]
            if i == 7:
                expected_value = [(6,7)]
            
            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #black pawns
        for i in range(0,8):
            value = []
            tested_piece = gamestate[2][i]

            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            expected_value = [(3,i)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        #black higher-pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[0][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)

            if i == 0:
                expected_value = [(1,0)]
            if i == 1:
                expected_value = [(1,3)]
            if i == 2:
                expected_value = [(1,1),(1,3)]
            if i == 3:
                expected_value = [(1,2),(1,4),(1,3)]
            if i == 4:
                expected_value = [(1,3),(1,5), (1,4)]
            if i == 5:
                expected_value = [(1,4),(1,6)]
            if i == 6:
                expected_value = [(1,4)]
            if i == 7:
                expected_value = [(1,7)]
            
            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        print('pieces move correctly in position where every pawn is moved forward')
#testing for more 'engaged' position with captures possible
    def test_position_close_rank(self):
        test_game = ChessApp()
        test_game.current_board = ChessBoard()
        test_game.current_board.create_chessboard()
        test_game.current_board.fill_chessboard('closerank')
        gamestate = test_game.current_board.chessboard
        #white pawns
        for i in range(4):
            value = []
            tested_piece = gamestate[4][i+2]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            if i == 0:
                expected_value = [(3,3)]
            if i == 1:
                expected_value = [(3,2), (3,4)]
            if i == 2:
                expected_value = [(3,3),(3,5)]
            if i == 3:
                expected_value = [(3,4)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        
        #white hihger pieces, check legal moves method for every white piece on the board
        for i in range(8):
            value = []
            tested_piece = gamestate[7][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)

            #rook
            if i == 0:
                expected_value = [(6,0),(5,0),(4,0),(3,0),(2,0),(1,0),(0,0)]
            #horse
            if i == 1:
                expected_value = [(5,0),(5,2),(6,3)]
            #bishop
            if i == 2:
                expected_value = [(5,0),(6,1),(6,3),(5,4)]
            #queen
            if i == 3:
                expected_value = [(6,2),(6,4),(6,3),(5,1),(5,3),(5,5),(4,0),(4,6),(3,7)]
            #king
            if i == 4:
                expected_value = [(6,3),(6,4), (6,5)]
            #bishop
            if i == 5:
                expected_value = [(6,4),(6,6),(5,3),(5,7)]
            #horse
            if i == 6:
                expected_value = [(6,4),(5,5),(5,7)]
            #rook
            if i == 7:
                expected_value = [(6,7),(5,7),(4,7),(3,7),(2,7),(1,7),(0,7)]
            
            self.assertEqual(sorted(value), sorted(expected_value))
            self.assertEqual(en_peasant, None)
        
        #black pawns
        for i in range(4):
            value = []
            tested_piece = gamestate[3][i+2]

            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
            if i == 0:
                expected_value = [(4,3)]
            if i == 1:
                expected_value = [(4,2), (4,4)]
            if i == 2:
                expected_value = [(4,3),(4,5)]
            if i == 3:
                expected_value = [(4,4)]

            self.assertEqual(value, expected_value)
            self.assertEqual(en_peasant, None)
        
        #black higher pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[0][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
    
            if i == 0:
                expected_value = [(6,0),(5,0),(4,0),(3,0),(2,0),(1,0),(7,0)]
            if i == 1:
                expected_value = [(2,0),(2,2),(1,3)]
            if i == 2:
                expected_value = [(2,0),(1,1),(1,3),(2,4)]
            if i == 3:
                expected_value = [(1,2),(1,4),(1,3),(2,1),(2,3),(2,5),(3,0),(3,6),(4,7)]
            if i == 4:
                expected_value = [(1,3),(1,4), (1,5)]
            if i == 5:
                expected_value = [(1,4),(1,6),(2,3),(2,7)]
            if i == 6:
                expected_value = [(1,4),(2,5),(2,7)]
            if i == 7:
                expected_value = [(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)]
            
            self.assertEqual(sorted(value), sorted(expected_value))
            self.assertEqual(en_peasant, None)
        print('pieces move correctly in position with 4x2 pawn block in middle')


    def test_position_no_pawn(self):
        test_game = ChessApp()
        test_game.current_board = ChessBoard()
        test_game.current_board.create_chessboard()
        test_game.current_board.fill_chessboard('nopawn')
        gamestate = test_game.current_board.chessboard

        #white hihger pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[7][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
    
            if i == 0:
                expected_value = [(6,0),(5,0),(4,0),(3,0),(2,0),(1,0),(0,0)]
            if i == 1:
                expected_value = [(5,0),(5,2),(6,3)]
            if i == 2:
                expected_value = [(5,0),(6,1),(6,3),(5,4),(4,5),(3,6),(2,7)]
            if i == 3:
                expected_value = [(6,2),(6,4),(6,3),(5,1),(5,3),(5,5),(4,0),(4,6),(3,7),(4,3),(3,3),(2,3),(1,3),(0,3)]
            if i == 4:
                expected_value = [(6,4), (6,5)]
            if i == 5:
                expected_value = [(6,4),(6,6),(5,3),(5,7),(4,2),(3,1),(2,0)]
            if i == 6:
                expected_value = [(6,4),(5,5),(5,7)]
            if i == 7:
                expected_value = [(6,7),(5,7),(4,7),(3,7),(2,7),(1,7),(0,7)]
            
            self.assertEqual(sorted(value), sorted(expected_value))
            self.assertEqual(en_peasant, None)

        #black higher pieces
        for i in range(8):
            value = []
            tested_piece = gamestate[0][i]
            value, en_peasant = tested_piece.legal_moves(test_game.current_board)
    
            if i == 0:
                expected_value = [(6,0),(5,0),(4,0),(3,0),(2,0),(1,0),(7,0)]
            if i == 1:
                expected_value = [(2,0),(2,2),(1,3)]
            if i == 2:
                expected_value = [(2,0),(1,1),(1,3),(2,4),(3,5),(4,6),(5,7)]
            if i == 3:
                expected_value = [(1,2),(1,4),(1,3),(2,1),(2,3),(2,5),(3,0),(3,6),(4,7),(3,3),(4,3),(5,3),(6,3),(7,3)]
            if i == 4:
                expected_value = [(1,4),(1,5)]
            if i == 5:
                expected_value = [(1,4),(1,6),(2,3),(2,7),(3,2),(4,1),(5,0)]
            if i == 6:
                expected_value = [(1,4),(2,5),(2,7)]
            if i == 7:
                expected_value = [(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7)]
            
            self.assertEqual(sorted(value), sorted(expected_value))
            self.assertEqual(en_peasant, None)
        print('pieces move correctly in position with no pawns')

if __name__ == '__main__':
    unittest.main()