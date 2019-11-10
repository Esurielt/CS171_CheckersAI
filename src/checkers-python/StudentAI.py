from BoardClasses import Move
from BoardClasses import Board
import math
import copy

# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI:

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.colors_dict = {1: 'B', 2: 'W'}
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):
        """
        Returns a chosen move.
        :param move: a Move instance.
        :return: move: updated Move Instance.
        """
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        move = self.alpha_beta(self.board, 2, (Move([]), -math.inf), (Move([]), math.inf), True)[0]
        return move

    def evaluate(self, board: Board):
        """
        Return the state/heuristic of the current board according to self.color.
        State Params:
            - Own       N Pieces : int
            - Own       King Pieces : int
            - Own       Edge Pieces : int
            - Own       Vertical Center of Mass : int *
            - Opponent  N Pieces : int
            - Opponent  King Pieces : int
            - Opponent  Vertical Center of Mass : int *
        *(TODO: implement vertical center of mass. )

        :param board: the Board being evaluate.
        :return: a int representing the heuristic
        """
        coefficient = [1, -1][self.color - 1]
        population = 3 * (board.black_count - board.white_count)
        kingdom = self.kingdom_calc(board)
        lords = 2 * (kingdom[0] - kingdom[1])  # kings worth ~5
        walls = 3 * (kingdom[2] - kingdom[3])  # walls worth 7
        return coefficient * (population + lords + walls)

    def alpha_beta(self, board: Board, depth: int, alpha: (Move, int), beta: (Move, int), max_player: bool):
        """
        Traditional Alpha-Beta pruning.
        :param board: current board
        :param depth: how far left to explore
        :param alpha: max alpha value
        :param beta: min beta value
        :param max_player: whether the current color of players is the one being maxed
        :return: best Move.
        """
        # initial call: alpha_beta(board, 3, (Move([]),-math.inf), (Move([]),math.inf), true)
        def aux_move_assign(move1, move2, max_int):
            """ Helper function to return best move in a tuple of (move, h)."""
            if max_int * move1[1] > max_int * move2[1]:
                return move1
            else:
                return move2

        cached_board = ""

        if depth == 0 or board.is_win('B') or board.is_win('W'):
            print("bottom")
            return Move([]), self.evaluate(board)
        if max_player:
            max_h = (Move([]), -math.inf)
            moves = board.get_all_possible_moves(self.color)
            print(moves)
            for child in moves:
                print(child)
                if len(child) > 1:
                    board.show_board()
                    print("saving cache.")
                    cached_board = copy.deepcopy()
                for leaf in child:
                    print(leaf)
                    board.make_move(leaf, self.colors_dict[self.color])
                    h = self.alpha_beta(board, depth - 1, alpha, beta, False)
                    max_h = aux_move_assign(max_h, h, 1)
                    alpha = aux_move_assign(alpha, max_h, 1)
                    if beta[1] <= alpha[1]:
                        break
            if cached_board != "":
                board.show_board()
                print("loading cache.")
                board = cached_board
                board.show_board()
            return max_h
        else:
            min_h = (Move([]), math.inf)
            moves = board.get_all_possible_moves(self.opponent[self.color])
            print(moves)
            for child in moves:
                print(child)
                if len(child) > 1:
                    cached_board = copy.deepcopy(board)
                for leaf in child:
                    print(leaf)
                    board.make_move(leaf, self.colors_dict[self.opponent[self.color]])
                    h = self.alpha_beta(board, depth - 1, alpha, beta, True)
                    min_h = aux_move_assign(min_h, h, -1)
                    beta = aux_move_assign(beta, min_h, -1)
                    if beta[1] <= alpha[1]:
                        break
            if cached_board != "":
                board.show_board()
                print("loading cache.")
                board = cached_board
                board.show_board()
            return min_h

    def kingdom_calc(self, board):
        """
        Count the Kings for the specific color.
        :param board: current board
        :return: int tuple of
        (black_kings, white_kings, black_guards, white_guards, black_population, white_population)
        """
        kingdoms = [0, 0, 0, 0]
        colors_dict = {'B': 0, 'W': 1}
        for r in range(board.row):
            for c in range(board.col):
                checker = board.board[r][c]
                if checker.get_color()!=".":
                    index = colors_dict[checker.get_color()]
                else:
                    index = -1
                if checker.is_king:
                    kingdoms[index] += 1
                if index != -1:
                    # kingdoms[index + 4] += 1  # if needed, hand count the color of pieces.
                    if r == board.row - 1 or r == 0 or c == board.col - 1 or c == 0:
                        kingdoms[index + 2] += 1

        return tuple(kingdoms)
