"""Beta-Go: Course project for CSC111 Winter 2023

Authors:
Henry "TJ" Chen
Dmitrii Vlasov
Ming Yau (Oscar) Lam
Duain Chhabra

Date: April 3, 2023

Version: pre-Alpha

Module Description
==================

This module contains a python class that represents an entire game of go.
It also contains additional runners which can be used to easily test our
work.

Copyright and Usage Information
===============================

This file was developed as part of the course project for CSC111 Winter 2023.
Feel free to test it out, but please contact us to obtain permission if you
intend to redistribute it or use it for your own work.
"""
from board import Board
from typing import Optional


class Game:
    """A class representing the state of a game of Go.

    Instance Attributes:
        - board: representation of the current state of the board
        - current_player: who's turn is it, either "Black" or "White
        - moves: a list that represents the sequence of moves played so far in the game
        - board_size: the size of the board. Note that the board is always a square
        - black_captured: the amount of stones captured BY BLACK so far
        - white_captured: the amount of stones captured BY WHITE so far
    Representation Invariants:
        - self.current_player in {'Black','White'}
        - self.board_size>0
        - self.black_captured>=0
        - self.white_captured>=0
    """
    board: Board
    current_player: str
    moves: list[tuple[int, int, int]]
    board_size: int
    black_captured: int
    white_captured: int

    def __init__(self, active_board: Optional[Board] = None, player_turn: Optional[str] = "Black",
                 move_sequence: Optional[list[tuple[int, int, int]]] = None, size: Optional[int] = 9) -> None:
        """
        Initialise a new Go game - defaults to a 9x9 empty board

        Other board sizes are typically 13x13 or 19x19 (19x19 is by far the most common of them all)

        Requires that the moves on the active board match those of the given move sequence
        """
        if active_board is None:
            self.board = Board(size=size)  # initialise a new board with the give size
        else:
            self.board = active_board
        self.current_player = player_turn
        if move_sequence is None:
            self.moves = []
        else:
            self.moves = move_sequence
        self.board_size = size

        self.white_captured = 0
        self.black_captured = 0

    def play_move(self, x: int, y: int) -> bool:
        """
        Given the location of a new move, updates the board and game.

        returns whether updating was sucessful or not
        Preconditions:
            - x<self.board.size
            - y<self.board.size
        """
        stone = self.board.get_stone(x, y)
        if stone.color == "Neither":
            self.board.add_stone(x, y, self.current_player)
            new_move = (len(self.moves) + 1, x, y)
            self.moves.append(new_move)

            for adjacent in stone.neighbours.values():
                if adjacent.check_is_dead(set()):
                    color = adjacent.color

                    # remember that the attribute keeps track of amount captured BY player
                    if color == "White":
                        self.black_captured += self.board.capture_stones(adjacent)
                    else:
                        self.white_captured += self.board.capture_stones(adjacent)

            # update current player attribute
            self.current_player = "White" if self.current_player == "Black" else "Black"
            return True
        else:
            return False

    def add_sequence(self, moves_sequence: list[tuple[int, int]]) -> None:
        """Function for testing the ouputting of a final board state
        Given a move sequence, it adds each move to the board
        Preconditions:
            - every move is a valid move
        """
        for move in moves_sequence:
            x, y = move
            print(f"Playing {self.current_player}'s move at ({x}, {y})")

    def is_valid_move(self, x: int, y: int) -> bool:
        """
        Return True if the move at (x, y) is valid, False otherwise
        Preconditions:
            - x<self.board.size
            - y<self.board.size
        """
        return self.board.get_stone(x, y).color == "Neither"

    def played_moves(self) -> list[tuple[int, int]]:
        """Return a list of the moves that have been played so far in the game"""
        new_moves = []
        for _, x, y in self.moves:
            new_moves.append((x, y))
        return new_moves

    def available_moves(self) -> list[tuple[int, int]]:
        """
        Return a list of the moves that are available to be played
        """
        available_moves = []
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.is_valid_move(x, y):
                    available_moves.append((x, y))
        return available_moves

    def get_move_info(self, x: int, y: int) -> tuple[int, str]:
        """Returns the turn number and player color based on the given coordinates
        """
        for turn, move_x, move_y in self.moves:
            if move_x == x and move_y == y:
                player_color = "Black" if turn % 2 == 1 else "White"
                return turn, player_color
        return -1, "Neither"

    def is_game_over(self) -> bool:
        """Checks if the game is over if both players have passed their turns it returns True, otherwise False
         add a check for if the board is full and check its fucntionality"""

        if self.played_moves()[-1] == (-1, -1) and len(self.moves) >= 2 and self.played_moves()[-1] == (-1, -1):
            return True
        else:
            return False

    def last_turn_no(self) -> int:
        """Returns the turn number of the last move played"""
        return len(self.moves)

    def pass_turn(self) -> None:
        """Allows a player to pass their turn."""
        self.current_player = "White" if self.current_player == "Black" else "Black"
        self.moves.append((self.last_turn_no() + 1, -1, -1))

    def add_move_using_color(self, turn: str, x: int, y: int) -> None:
        """Adds a move to the game using the turn number and coordinates
            TESTING DO NOT USE"""
        self.board.add_stone(x, y, turn)

    def game_end(self, max_moves: int) -> bool:
        """
        Checks if the game has ended
        Preconditions:
            - max_moves>0
        """
        if len(self.moves) == max_moves:
            return True
        elif not self.available_moves():
            return True
        else:
            return False

    def overall_score(self, technique: str = "dfs") -> tuple[float, float]:
        """
        Returns the overall score of the game
        Preconditions:
            - technique is a valid technique
        """
        total_white, total_black = 2.5, 0

        territory_score = self.board.calculate_score(technique)

        total_black += len(territory_score[0]) + self.black_captured

        total_white += len(territory_score[1]) + self.white_captured

        return total_white, total_black

    def iswinner(self, player: str) -> bool:
        """Returns True if the given player is the winner of the game, False otherwise
        Preconditions:
            - player in {'White', 'Black'}
        """
        if self.overall_score()[0] > self.overall_score()[1]:
            return player == "White"
        else:
            return player == "Black"

    def get_move_sequence(self) -> list[tuple[int, int, int]]:
        """Returns the move sequence of the game"""
        return self.moves


################################################################################
# Functions for running games
################################################################################

def run_game() -> Game:
    """Run a basic Go game on a 9x9 board game

    prompts user to input the moves they would like to make
    returns the newly created game
    """
    new_game = Game()
    next_move = ''

    while next_move != 'STOP':
        # used for creating a new line in f-string
        n1 = '\n'

        # get input from user
        next_move = input(
            f'It is currently {new_game.current_player}\'s turn. Please enter your next move as a coordinate'
            f'in the form: x,y.{n1}If you would like to end the game, enter \"STOP\" without qoutation marks!')

        # convert to upper case to avoid case sensitivity
        next_move.upper()

        if not next_move == 'STOP':
            coords = next_move.split(",")
            x = int(coords[0])
            y = int(coords[1])

            new_game.play_move(x, y)

    return new_game


# if __name__ == "__main__":
    # game = Game()
    # moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2), (2, 2)]
    # game.run_example(moves)
    # import python_ta
