#!/usr/bin/env python3

import numpy as np
import json
import copy

import rules
from plan import Plan
from grid import Grid


class Board:
    class ExceptCantSolveTile(Exception):
        pass

    class ExceptTooManyOfATile(Exception):
        pass

    def __init__(self, tiles=None, data_str: (str or None) = None):
        assert (tiles is not None) or (data_str is not None)
        assert (tiles is None) or (data_str is None)

        if tiles is not None:
            self.grid = Grid(tiles=tiles)
            self.plan = Plan()

        if data_str is not None:
            self.grid = Grid(tiles=[])
            self.plan = Plan()
            bd = json.loads(data_str)
            self.plan.p = bd["plan"]
            self.grid.matrix = np.array(bd["spare_grid"], dtype=int)

    def print(self, tabs=0):
        self.plan.print(tabs=tabs)
        self.grid.print(tabs=tabs)

    def find_tile_moves(self, rank, suit, verbose=False):
        new_group_moves = self.grid.find_tile_new_group_moves(rank, suit)
        add_to_group_moves = self.plan.find_tile_add_to_group_moves(rank, suit)
        # print('new_group_moves', new_group_moves)
        # print('add_to_group_moves', add_to_group_moves)
        # print('matrix', self.grid.matrix)
        # input('enter to continue')

        for move in new_group_moves:
            print("found new group move") if verbose else None
            new_board = Board(tiles=[])
            new_board.plan.p = copy.deepcopy(self.plan.p)
            new_board.plan.p.append(copy.deepcopy(move["group"]))

            new_board.grid.matrix = copy.deepcopy(move["new_matrix"])
            move["new_board_data"] = new_board.data_str()

        for move in add_to_group_moves:
            print("found add to group move") if verbose else None
            rank = move["rank"]
            suit = move["suit"]
            new_matrix = copy.deepcopy(self.grid.matrix)
            new_matrix[rank, suit] -= 1
            new_board = Board(tiles=[])
            new_board.plan.p = move["new_plan"]
            new_board.grid.matrix = copy.deepcopy(new_matrix)
            move["new_board_data"] = new_board.data_str()

        return [*new_group_moves, *add_to_group_moves]

    def simplify(self, verbose=False):
        if verbose:
            print("\t" + "simplifying")
            self.print(tabs=2)
        fresh_changes = True
        while fresh_changes:
            fresh_changes = False
            # print('\nboard')
            # print(self.plan)
            # print(self.grid.matrix)
            for rank, suit in [(r, s) for r in rules.ranks for s in rules.suits]:
                # For each tile
                print(f"tile=({rank},{suit})") if verbose else None
                tiles_unplaced = self.grid.matrix[rank, suit]
                if tiles_unplaced == 0:
                    continue
                elif tiles_unplaced < 0:
                    raise Exception("Gone into negative")
                elif tiles_unplaced > 2:
                    # TODO This is incorrect for when using the joker
                    raise self.ExceptTooManyOfATile

                moves = self.find_tile_moves(rank, suit, verbose=verbose)

                if len(moves) == 0:
                    raise self.ExceptCantSolveTile
                elif len(moves) == tiles_unplaced:
                    # All moves must be true
                    if verbose:
                        print("\t\t" + f"enacting moves on ({rank}, {suit})")
                    for move in moves:
                        # Enact move
                        if move["type"] == "new_group":
                            if verbose:
                                print("\t\t\t" + "doing add to group move")
                            data = json.loads(move["new_board_data"])
                            self.grid.matrix = np.array(data["spare_grid"], dtype=int)
                            self.plan.p = data["plan"]
                        elif move["type"] == "add_to_group":
                            if verbose:
                                print("\t\t\t" + "doing add to group move")
                            data = json.loads(move["new_board_data"])
                            self.grid.matrix = np.array(data["spare_grid"], dtype=int)
                            self.plan.p = data["plan"]
                        else:
                            raise Exception("Bad move type")

                        if verbose:
                            print("\t\t\t" + "new board")
                            self.print(tabs=4)

                    fresh_changes = True

            print("\t" + "simplifying loopback") if verbose else None
        print("Done simplifying") if verbose else None

    def find_board_choice(self, verbose=False):
        tile_moves = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=list)
        tile_moves_len = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=int)
        for rank in rules.ranks:
            for suit in rules.suits:
                if self.grid.matrix[rank, suit] > 0:
                    moves = self.find_tile_moves(rank, suit, verbose=False)
                    tile_moves[rank, suit] = moves
                    tile_moves_len[rank, suit] = len(moves)

        num_least_move_options = tile_moves_len[tile_moves_len > 0].min()
        choice_tiles_indices = (tile_moves_len == num_least_move_options).nonzero()
        choice_tile = (choice_tiles_indices[0][0], choice_tiles_indices[1][0])
        choice = tile_moves[choice_tile[0], choice_tile[1]]
        return choice

    def solve(self, verbose=False):
        print("solving") if verbose else None
        routes = [[self]]
        for route in routes:
            board = route[-1]
            board.simplify()
            if board.is_done():
                print("simplify got it") if verbose else None
                return board.plan
            if verbose:
                board.print()
                print("finding choices")
            choice = board.find_board_choice(verbose=verbose)
            for move in choice:
                new_board = Board(data_str=move["new_board_data"])
                if new_board.is_done():
                    if verbose:
                        print("one move got it")
                        print(move)
                        print(new_board.grid.matrix)
                    return new_board.plan
                else:
                    new_route = [*route, new_board]
                    routes.append(new_route)
            print("going to next route") if verbose else None
        print("Damn didn't get it") if verbose else None
        return None

    def is_done(self):
        return self.grid.matrix.sum() == 0

    def data_str(self) -> str:
        o = dict()
        o["spare_grid"] = self.grid.matrix.tolist()
        o["plan"] = self.plan.p
        s = json.dumps(o)
        return s


if __name__ == "__main__":
    if False:
        board = Board(
            tiles=[
                (6, "⬛️"),
                (7, "⬛️"),
                (8, "⬛️"),
                (9, "⬛️"),
            ]
        )
        print(board.solve())

    if False:
        board = Board(
            tiles=[
                (6, "🟥"),
                (6, "⬛️"),
                (6, "🟦"),
                (6, "🟨"),
                (7, "🟥"),
                (7, "🟨"),
                (8, "🟥"),
                (8, "🟨"),
                (9, "🟥"),
                (9, "⬛️"),
                (9, "🟦"),
                (9, "🟨"),
                # (12,'🟨'),
            ]
        )
        try:
            print(board.solve())
        except ExceptCantSolveTile:
            print("cant solve it")

    if False:
        board = Board(
            tiles=[
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
                # More in Goodnotes pictures
            ]
        )

        if False:
            board.simplify()
            board.plan.print()
            board.grid.print()
        else:
            import time

            start = time.time()
            try:
                res = board.solve()
                res.print(suit_strings=True)
            except ExceptCantSolveTile:
                print("cant solve it")
            end = time.time()
            print(f"Took {end-start}sec")

    if False:
        tiles = []
        for rank in rules.ranks[0:3]:
            for suit in rules.suits[0:1]:
                tiles.append((rank, suit))
                tiles.append((rank, suit))
        board = Board(tiles=tiles)
        try:
            print(board.solve())
        except ExceptCantSolveTile:
            print("cant solve it")

    if True:
        tiles = [
            # Group 0
            [6, "🟦"],
            [7, "🟦"],
            [8, "🟦"],
            # Group 1
            [7, "⬛️"],
            [7, "🟨"],
            [7, "🟥"],
            # Group 2
            [5, "🟦"],
            [6, "🟦"],
            [7, "🟦"],
            # Group 3
            [10, "🟦"],
            [11, "🟦"],
            [12, "🟦"],
            [13, "🟦"],
            # Group 4
            [9, "🟥"],
            [10, "🟥"],
            [11, "🟥"],
            [12, "🟥"],
            # Group 5
            [3, "⬛️"],
            [4, "⬛️"],
            [5, "⬛️"],
            # Group 6
            [7, "⬛️"],
            [8, "⬛️"],
            [9, "⬛️"],
            [10, "⬛️"],
            [11, "⬛️"],
            # Group 7
            [11, "⬛️"],
            [12, "⬛️"],
            [13, "⬛️"],
            # Group 8
            [8, "⬛️"],
            [8, "🟦"],
            [8, "🟥"],
            # Group 9
            [13, "⬛️"],
            [13, "🟦"],
            [13, "🟥"],
            [13, "🟨"],
            # Group 10
            [3, "🟥"],
            [4, "🟥"],
            [5, "🟥"],
            [6, "🟥"],
            [7, "🟥"],
            # Group 11
            [1, "⬛️"],
            [1, "🟨"],
            [1, "🟥"],
            # Group 12
            [4, "🟦"],
            [4, "🟨"],
            [4, "🟥"],
            # Group 13
            [1, "⬛️"],
            [1, "🟦"],
            [1, "🟥"],
            # Group 14
            [5, "⬛️"],
            [5, "🟦"],
            [5, "🟨"],
            # Group 15
            [2, "🟦"],
            [3, "🟦"],
            [4, "🟦"],
            # Group 16
            [10, "⬛️"],
            [10, "🟦"],
            [10, "🟥"],
            [10, "🟨"],
            # Group 17
            [6, "🟨"],
            [7, "🟨"],
            [8, "🟨"],
            [9, "🟨"],
            # Group 18
            [9, "🟨"],
            [10, "🟨"],
            [11, "🟨"],
            [12, "🟨"],
            [13, "🟨"],
            # Group 19
            [3, "🟨"],
            [4, "🟨"],
            [5, "🟨"],
            [6, "🟨"],
            # Group 20
            [12, "⬛️"],
            [12, "🟦"],
            [12, "🟥"],
            # Group 21
            [2, "🟦"],
            [2, "🟥"],
            ["J", "⬛️"],
            # Group 22
            [3, "🟨"],
        ]
        # Numbers -> ranks
        for tile in tiles:
            if tile[0] != "J":
                tile[0] -= 1

        # Test for each joker value
        jokers = []
        for tile in tiles:
            if tile[0] == "J":
                jokers.append(tile)

        if len(jokers) == 0:
            board = Board(tiles=tiles)
            try:
                print(board.solve())
            except board.ExceptCantSolveTile:
                print("cant solve it")
            except board.ExceptTooManyOfATile:
                print("too many of a tile")

        if len(jokers) == 1:
            for rank in rules.ranks:
                for suit in rules.suits:
                    jokers[0][0] = rank
                    jokers[0][1] = suit
                    print(f"Trying jokers = {jokers}")
                    board = Board(tiles=tiles)
                    try:
                        print(board.solve())
                    except board.ExceptCantSolveTile:
                        print("cant solve it")
                    except board.ExceptTooManyOfATile:
                        print("too many of a tile")

        if len(jokers) == 2:
            for rankA in rules.ranks:
                for suitA in rules.ranks:
                    for rankB in rules.ranks:
                        for suitB in rules.ranks:
                            jokers[0][0] = rankA
                            jokers[0][1] = suitA
                            jokers[1][0] = rankB
                            jokers[1][1] = suitB
                            print(f"Trying jokers = {jokers}")
                            board = Board(tiles=tiles)
                            try:
                                print(board.solve())
                            except board.ExceptCantSolveTile:
                                print("cant solve it")
                            except board.ExceptTooManyOfATile:
                                print("too many of a tile")
