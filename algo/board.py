import numpy as np
import json
import copy

import rules
from plan import Plan
from grid import Grid

class Board():
    class CantSolveTile(Exception):
        pass

    def __init__(self, tiles=None, data_str:(str or None)=None):
        assert (tiles is not None) or (data_str is not None)
        assert (tiles is None) or (data_str is None)

        if tiles is not None:
            self.grid = Grid(tiles=tiles)
            self.plan = Plan()

        if data_str is not None:
            self.grid = Grid(tiles=[])
            self.plan = Plan()
            bd = json.loads(data_str)
            self.plan.p = bd['plan']
            self.grid.matrix = np.array(bd['spare_grid'], dtype=int)

    def print(self, tabs=0):
        self.plan.print(tabs=tabs)
        self.grid.print(tabs=tabs)

    def find_tile_moves(self, rank, suit, debug=False):
        new_group_moves = self.grid.find_tile_new_group_moves(rank, suit)
        add_to_group_moves = self.plan.find_tile_add_to_group_moves(rank, suit)
        # print('new_group_moves', new_group_moves)
        # print('add_to_group_moves', add_to_group_moves)
        # print('matrix', self.grid.matrix)
        # input('enter to continue')

        for move in new_group_moves:
            if debug: print('found new group move')
            new_board = Board(tiles=[])
            new_board.plan.p = copy.deepcopy(self.plan.p)
            new_board.plan.p.append(copy.deepcopy(move['group']))
            
            new_board.grid.matrix = copy.deepcopy(move['new_matrix'])
            move['new_board_data'] = new_board.data_str()

        for move in add_to_group_moves:
            if debug: print('found add to group move')
            rank = move['rank']
            suit = move['suit']
            new_matrix = copy.deepcopy(self.grid.matrix)
            new_matrix[rank, suit] -= 1
            new_board = Board(tiles=[])
            new_board.plan.p = move['new_plan']
            new_board.grid.matrix = copy.deepcopy(new_matrix)
            move['new_board_data'] = new_board.data_str()


        return [*new_group_moves, *add_to_group_moves]
        
    def simplify(self, debug=False):
        if debug:
            print('\t' +'simplifying')
            self.print(tabs=2)
        fresh_changes = True
        while fresh_changes:
            fresh_changes = False
            # print('\nboard')
            # print(self.plan)
            # print(self.grid.matrix)
            for rank in rules.ranks:
                for suit in rules.suits:
                    if debug:
                        print(f'tile=({rank},{suit})')
                    tiles_unplaced = self.grid.matrix[rank, suit]
                    if tiles_unplaced == 0:
                        continue
                    elif tiles_unplaced < 0:
                        raise Exception('Gone into negative')
                    elif tiles_unplaced > 2:
                        raise Exception('Too many of one number')
                    
                    moves = self.find_tile_moves(rank, suit, debug=debug)

                    if len(moves) == 0:
                        raise self.CantSolveTile
                    elif len(moves) == tiles_unplaced:
                        # All moves must be true
                        if debug: 
                            print('\t\t' + f'enacting moves on ({rank}, {suit})')
                        for move in moves:
                            # Enact move
                            if move['type'] == 'new_group':
                                if debug: print('\t\t\t' + 'doing add to group move')
                                data = json.loads(move['new_board_data'])
                                self.grid.matrix = np.array(data['spare_grid'], dtype=int)
                                self.plan.p = data['plan']
                            elif move['type'] == 'add_to_group':
                                if debug: print('\t\t\t' + 'doing add to group move')
                                data = json.loads(move['new_board_data'])
                                self.grid.matrix = np.array(data['spare_grid'], dtype=int)
                                self.plan.p = data['plan']
                            else:
                                raise Exception('Bad move type')

                            if debug: 
                                print('\t\t\t' + 'new board')
                                self.print(tabs=4)

                        fresh_changes = True

            if debug: print('\t'+ 'simplifying loopback')
        if debug: print('Done simplifying')

    def find_board_choice(self, debug=False):
        tile_moves = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=list)
        tile_moves_len = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=int)
        for rank in rules.ranks:
            for suit in rules.suits:
                if self.grid.matrix[rank, suit] > 0:
                    moves = self.find_tile_moves(rank, suit, debug=False)
                    tile_moves[rank, suit] = moves
                    tile_moves_len[rank, suit] = len(moves)
    
        num_least_move_options = tile_moves_len[tile_moves_len>0].min()
        choice_tiles_indices = (tile_moves_len == num_least_move_options).nonzero()
        choice_tile = (choice_tiles_indices[0][0], choice_tiles_indices[1][0])
        choice = tile_moves[choice_tile[0], choice_tile[1]]
        return choice
    
    def solve(self, debug=False):
        if debug:
            print('solving')
        routes = [[self]] 
        for route in routes:
            board = route[-1]
            board.simplify()
            if board.is_done():
                if debug:
                    print('simplify got it')
                return board.plan
            if debug:
                board.print()
                print('finding choices')
            choice = board.find_board_choice(debug=debug)
            for move in choice:
                new_board = Board(data_str=move['new_board_data'])
                if new_board.is_done():
                    if debug:
                        print('one move got it')
                        print(move)
                        print(new_board.grid.matrix)
                    return new_board.plan
                else:
                    new_route = [*route, new_board]
                    routes.append(new_route)
            if debug: print('going to next route')
        if debug: print('Damn didn\'t get it')
        return None

    def is_done(self):
        return self.grid.matrix.sum() == 0

    def data_str(self) -> str:
        o  = dict()
        o['spare_grid'] = self.grid.matrix.tolist()
        o['plan'] = self.plan.p
        s = json.dumps(o)
        return s

if __name__ == '__main__':
    if False:
        board = Board(tiles=[
            (6,'Blk'),
            (7,'Blk'),
            (8,'Blk'),
            (9,'Blk'),
        ])
        print(board.solve())

    if False:
        board = Board(tiles=[
            (6,'Red'),
            (6,'Blk'),
            (6,'Blu'),
            (6,'Yel'),
            (7,'Red'),
            (7,'Yel'),
            (8,'Red'),
            (8,'Yel'),
            (9,'Red'),
            (9,'Blk'),
            (9,'Blu'),
            (9,'Yel'),
            # (12,'Yel'),
        ])
        try:
            print(board.solve())
        except CantSolveTile:
            print('cant solve it')

    if True:
        board = Board(tiles=[
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

            # More in Goodnotes pictures
        ])

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
            except CantSolveTile:
                print('cant solve it')
            end = time.time()
            print(f'Took {end-start}sec')

    if False:
        tiles = []
        for rank in rules.ranks[0:3]:
            for suit in rules.suits[0:1]:
                tiles.append((rank, suit))
                tiles.append((rank, suit))
        board = Board(tiles=tiles)
        try:
            print(board.solve())
        except CantSolveTile:
            print('cant solve it')

