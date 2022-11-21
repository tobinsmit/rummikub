import copy, time
import numpy as np
from board import Board

class Game():
    def __init__(self, hand_tiles, board_tiles):
        self.hand_tiles = hand_tiles
        self.board_tiles = board_tiles

    def get_turn_options(self, verbose=False):
        num_combinations = 2**len(self.hand_tiles)
        turn_options = []
        if verbose: print('num_combinations', num_combinations)
        for i in range(num_combinations):
            if verbose: print('i', i)
            # Get tiles to place
            hand_tiles_to_place = []
            for t, tile in enumerate(self.hand_tiles):
                if i & 2**t:
                    hand_tiles_to_place.append(tile)
            if verbose: print('\thand_tiles_to_place', hand_tiles_to_place)
            
            # Figure out if tiles can be placed
            tiles = [*hand_tiles_to_place, *self.board_tiles]
            if verbose: print('\t\ttiles', tiles)
            board = Board(tiles)
            try:
                plan = board.solve()
            except Board.CantSolveTile:
                if verbose: print('\tCant solve')
                continue
            if plan == None:
                print('\tNo plan?')
                raise Exception()
                continue
            if verbose: print('\tAppending option :)')
            turn_options.append((hand_tiles_to_place, plan))

        return turn_options

    def place_most_tiles(self):
        turn_options = self.get_turn_options()
        turn_option_scores = np.zeros(shape=len(turn_options), dtype=int)
        for i, to in enumerate(turn_options):
            hand_leftover : list = copy.deepcopy(self.hand_tiles)
            for tile in to[0]:
                hand_leftover.remove(tile)
            score = 0
            for tile in hand_leftover:
                score += tile[0]+1
            turn_option_scores[i] = score

        min_score = turn_option_scores.min()
        best_turn_options = []
        for i in range(len(turn_options)):
            if turn_option_scores[i] == min_score:
                best_turn_options.append(turn_options[i])
        return best_turn_options


if __name__ == '__main__':
    game = Game(board_tiles=[
        ( 5, 'Red'),
        ( 6, 'Red'),
        ( 7, 'Red'),

        ( 6, 'Red'),
        ( 6, 'Blu'),
        ( 6, 'Yel'),

        ( 1, 'Red'),
        ( 2, 'Red'),
        ( 3, 'Red'),
        ( 4, 'Red'),

        ( 7, 'Red'),
        ( 8, 'Red'),
        ( 9, 'Red'),
        (10, 'Red'),

        (10, 'Red'),
        (11, 'Red'),
        (12, 'Red'),

        ( 2, 'Yel'),
        ( 3, 'Yel'),
        ( 4, 'Yel'),
        ( 5, 'Yel'),

        ( 1, 'Blk'),
        ( 2, 'Blk'),
        ( 3, 'Blk'),
        ( 4, 'Blk'),
        ( 5, 'Blk'),
        ( 6, 'Blk'),
        ( 7, 'Blk'),

        ( 4, 'Yel'),
        ( 5, 'Yel'),
        ( 6, 'Yel'),
        ( 7, 'Yel'),

        ( 9, 'Yel'),
        (10, 'Yel'),
        (11, 'Yel'),
        (12, 'Yel'),
        ], 
        hand_tiles=[
            ( 7, 'Yel'),
            ( 8, 'Yel'),
            ( 0, 'Red'),
            ( 11, 'Yel'),
            ( 12, 'Blk'),
            ( 4, 'Blu'),
            ( 2, 'Blu'),
            ( 9, 'Blu'),
        ])
    
    to = game.place_most_tiles()
    print(to)
