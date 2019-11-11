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
        self.move = Move([])
        # self.debug_tree = StudentAI.Node("root", [])

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
        h = self.alpha_beta(self.board, 2, -math.inf, math.inf, True)
        # print("player decide", self.move)
        self.board.make_move(self.move, self.color)
        return self.move

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
        :return: eval
        """

        # initial call: alpha_beta(board, 3, (Move([]),-math.inf), (Move([]),math.inf), true)

        if depth == 0 or board.is_win('B') or board.is_win('W'):
            e = self.evaluate(board)
            # print("bottom")
            return e
        if max_player:
            max_h = -math.inf
            moves = board.get_all_possible_moves(self.color)
            # print(moves)
            for child in moves:
                # print(child)
                pruned = False
                for leaf in child:
                    board_new = copy.deepcopy(board)
                    board_new.make_move(leaf, self.colors_dict[self.color])
                    h = self.alpha_beta(board_new, depth - 1, alpha, beta, False)
                    self.move = leaf
                    max_h = max(max_h, h)
                    alpha = max(alpha, h)
                    if beta <= alpha:
                        # print("pruned from" + str(leaf))
                        pruned = True
                        break
                if pruned and len(child) == 1:
                    break
            # print(max_h)
            return max_h
        else:
            min_h = math.inf
            moves = board.get_all_possible_moves(self.opponent[self.color])
            # print(moves)
            for child in moves:
                # print(child)
                pruned = False
                for leaf in child:
                    # print(leaf)
                    board_new = copy.deepcopy(board)
                    board_new.make_move(leaf, self.colors_dict[self.opponent[self.color]])
                    h = self.alpha_beta(board_new, depth - 1, alpha, beta, True)
                    self.move = leaf
                    # print("finished", self.move, h)
                    min_h = min(min_h, h)
                    beta = min(beta, h)
                    if beta <= alpha:
                        # print("pruned from" + str(leaf))
                        pruned = True
                        break
                if pruned and len(child) == 1:
                    break
            # print(min_h)
            return min_h

    def kingdom_calc(self, board) -> tuple:
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
                if checker.get_color() != ".":
                    index = colors_dict[checker.get_color()]
                else:
                    index = -1
                if checker.is_king:
                    kingdoms[index] += 1
                if index != -1 and (c == board.col - 1 or c == 0):
                    kingdoms[index + 2] += 1
        return tuple(kingdoms)

#     class Node:
#         def __init__(self, value="root", children=[]):
#             self.value = value
#             self.children = children
#
#
# def _debug_pprint_tree(node, file=None, _prefix="", _last=True):
#     print(_prefix, "`- " if _last else "|- ", node, sep="", file=file)
#     _prefix += "   " if _last else "|  "
#     child_count = len(node)
#     for i, child in enumerate(node.children):
#         _last = i == (child_count - 1)
#         pprint_tree(child, file, _prefix, _last)
