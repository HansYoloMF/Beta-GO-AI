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
from go_gui import draw_board
from typing import Optional


class Game:
    """A class representing the state of a game of Go.

     Instance Attributes:
        - board: representation of the current state of the board
        - current_player: who's turn is it, either "Black" or "White
        - moves: a list that represents the sequence of moves played so far in the game
        - board_size: the size of the board. Note that the board is always a square

    """
    board: Board
    current_player: str
    moves: list[tuple[int, int, int]]
    board_size = int

    def __init__(self, size: Optional[int] = 9):
        """
        Initialise a new Go Game with the given board size - defaults to a 9x9 board

        """
        self.board = Board(size=size)  # initialise a new board with the give size
        self.current_player = "Black"
        self.moves = []
        self.board_size = size

    def play_move(self, x, y) -> bool:
        """
        Given the location of a new move, updates the board and game.
        :param x:
        :param y:
        :return:
        """
        if self.board.get_stone(x, y).color == "Neither":
            self.board.add_stone(x, y, self.current_player)
            self.current_player = "White" if self.current_player == "Black" else "Black"

            new_move = (len(self.moves) + 1, x, y)
            self.moves.append(new_move)
            return True
        else:
            return False

    def run_example(self, moves_sequence) -> None:
        """Function for testing the ouputting of a final board state"""
        for move in moves_sequence:
            x, y = move
            print(f"Playing {self.current_player}'s move at ({x}, {y})")
            success = self.play_move(x, y)
            if success:
                print("Move successful.")
            else:
                print("Move failed. Position already occupied.")
        print("Final board state:")
        print(self.board)
        draw_board(self.board, open_in_browser=True)


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


if __name__ == "__main__":
    # game = Game()
    # moves = [(0, 0), (1, 1), (0, 1), (1, 0), (0, 2), (2, 2)]
    # game.run_example(moves)
    game = run_game()
    print(game)
    draw_board(game.board, "Game_result/runner_example.jpg", True)
