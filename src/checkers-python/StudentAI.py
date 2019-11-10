from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI:

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        # color {black: 1, white: 2}
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.true_color = 2

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
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0, len(moves) - 1)
        inner_index = randint(0, len(moves[index]) - 1)
        move = moves[index][inner_index]
        self.board.make_move(move, self.color)
        return move

    def eval(self, board: Board):
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
        pass

    def alpha_beta(self, board: Board, depth: int, alpha: int, beta: int, max_player: bool):
        """
        Traditional Alpha-Beta pruning.
        :param board: current board
        :param depth: how far left to explore
        :param alpha: max alpha value
        :param beta: min beta value
        :param max_player: whether the current color of players is the one being maxed
        :return: best Move.
        """
        # initial call: alpha_beta(board, 3, -math.inf, math.inf, true)
        pass
