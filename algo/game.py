#!/usr/bin/env python3

import copy, time
import numpy as np
from board import Board


class Game:
    def __init__(self, hand_tiles, board_tiles):
        self.hand_tiles = hand_tiles
        self.board_tiles = board_tiles

    def get_turn_options(self, verbose=False):
        num_combinations = 2 ** len(self.hand_tiles)
        turn_options = []
        if verbose:
            print("num_combinations", num_combinations)
        for i in range(num_combinations):
            if verbose:
                print("i", i)
            # Get tiles to place
            hand_tiles_to_place = []
            for t, tile in enumerate(self.hand_tiles):
                if i & 2**t:
                    hand_tiles_to_place.append(tile)
            if verbose:
                print("\thand_tiles_to_place", hand_tiles_to_place)

            # Figure out if tiles can be placed
            tiles = [*hand_tiles_to_place, *self.board_tiles]
            if verbose:
                print("\t\ttiles", tiles)
            board = Board(tiles)
            try:
                plan = board.solve()
            except Board.ExceptCantSolveTile:
                if verbose:
                    print("\tCant solve")
                continue
            if plan == None:
                print("\tNo plan?")
                raise Exception()
                continue
            if verbose:
                print("\tAppending option :)")
            turn_options.append((hand_tiles_to_place, plan))

        return turn_options

    def place_most_tiles(self):
        turn_options = self.get_turn_options()
        turn_option_scores = np.zeros(shape=len(turn_options), dtype=int)
        for i, option in enumerate(turn_options):
            hand_leftover: list = copy.deepcopy(self.hand_tiles)
            for tile in option[0]:
                hand_leftover.remove(tile)
            score = 0
            for tile in hand_leftover:
                score += tile[0] + 1
            turn_option_scores[i] = score

        min_score = turn_option_scores.min()
        best_turn_options = []
        for i in range(len(turn_options)):
            if turn_option_scores[i] == min_score:
                best_turn_options.append(turn_options[i])
        return best_turn_options


if __name__ == "__main__":
    game = Game(
        board_tiles=[
            # Group 0
            (5, "🟥"),
            (6, "🟥"),
            (7, "🟥"),
            # Group 1
            (6, "🟥"),
            (6, "🟦"),
            (6, "🟨"),
            # Group 2
            (1, "🟥"),
            (2, "🟥"),
            (3, "🟥"),
            (4, "🟥"),
            # Group 3
            (7, "🟥"),
            (8, "🟥"),
            (9, "🟥"),
            (10, "🟥"),
            # Group 4
            (10, "🟥"),
            (11, "🟥"),
            (12, "🟥"),
            # Group 5
            (2, "🟨"),
            (3, "🟨"),
            (4, "🟨"),
            (5, "🟨"),
            # Group 6
            (1, "⬛️"),
            (2, "⬛️"),
            (3, "⬛️"),
            (4, "⬛️"),
            (5, "⬛️"),
            (6, "⬛️"),
            (7, "⬛️"),
            # Group 7
            (4, "🟨"),
            (5, "🟨"),
            (6, "🟨"),
            (7, "🟨"),
            # Group 8
            (9, "🟨"),
            (10, "🟨"),
            (11, "🟨"),
            (12, "🟨"),
        ],
        hand_tiles=[
            (7, "🟨"),
            (8, "🟨"),
            (0, "🟥"),
            (11, "🟨"),
            (12, "⬛️"),
            (4, "🟦"),
            (2, "🟦"),
            (9, "🟦"),
        ],
    )

    result = game.place_most_tiles()
    print(result)
