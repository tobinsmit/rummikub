import numpy as np
import rules
from plan import Plan
from grid import Grid

class CantSolveTile(Exception):
    pass

class Board():
    def __init__(self, tiles):
        self.grid = Grid(tiles=tiles)
        self.plan = Plan()

    def find_tile_moves(self, rank, suit):
        new_group_moves = self.grid.find_tile_new_group_moves(rank, suit)
        add_to_group_moves = self.plan.find_tile_add_to_group_moves(rank, suit)

        for move in new_group_moves:
            group = move['group']
            new_plan = self.plan.p.copy()
            new_plan.append(group)
            move['new_plan'] = new_plan
            new_board = Board(tiles=[])
            new_board.plan.p = new_plan
            new_board.grid.matrix = move['new_matrix']
            move['new_board'] = new_board

        for move in add_to_group_moves:
            rank = move['rank']
            suit = move['suit']
            new_matrix = self.grid.matrix.copy()
            new_matrix[rank, suit] -= 1
            move['new_matrix'] = new_matrix
            new_board = Board(tiles=[])
            new_board.plan.p = move['new_plan']
            new_board.grid.matrix = new_matrix
            move['new_board'] = new_board

        return [*new_group_moves, *add_to_group_moves]
        
    def simplify(self):
        print('simplifying')
        print('\nboard')
        print(self.plan)
        print(self.grid.matrix)
        fresh_changes = True
        while fresh_changes:
            print('simplifying loopback')
            fresh_changes = False
            for rank in rules.ranks:
                for suit in rules.suits:
                    tiles_unplaced = self.grid.matrix[rank, suit]
                    if tiles_unplaced == 0:
                        continue
                    elif tiles_unplaced < 0:
                        raise Exception('Gone into negative')
                    elif tiles_unplaced > 2:
                        raise Exception('Too many of one number')
                    
                    moves = self.find_tile_moves(rank, suit)

                    if len(moves) == 0:
                        raise CantSolveTile
                    elif len(moves) == tiles_unplaced:
                        # All moves must be true
                        for move in moves:
                            # Enact move
                            if move['type'] == 'new_group':
                                print('doing new group move')
                                # group = move['group']
                                # new_matrix = move['new_matrix']
                                # self.plan.p.append(group)
                                # self.grid.matrix = new_matrix
                                new_board = move['new_board']
                                self.grid.matrix = new_board.grid.matrix
                                self.plan.p = new_board.plan.p
                            elif move['type'] == 'add_to_group':
                                print('doing add to group move')
                                # rank = move['rank']
                                # suit = move['suit']
                                # new_plan = move['new_plan']
                                # self.plan.p = new_plan
                                # self.grid.matrix[rank, suit] -= 1
                                new_board = move['new_board']
                                self.grid.matrix = new_board.grid.matrix
                                self.plan.p = new_board.plan.p
                            else:
                                raise Exception('Bad move type')

                            print('new board')
                            print(self.plan)
                            print(self.grid.matrix)

                        fresh_changes = True
                        
    def find_board_choice(self):
        tile_moves = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=list)
        tile_moves_len = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=int)
        for rank in rules.ranks:
            for suit in rules.suits:
                moves = self.find_tile_moves(rank, suit)
                tile_moves[rank, suit] = moves
                tile_moves_len[rank, suit] = len(moves)
    
        num_least_move_options = tile_moves_len[tile_moves_len>0].min()
        choice_tiles_indices = (tile_moves_len == num_least_move_options).nonzero()
        choice_tile = (choice_tiles_indices[0][0], choice_tiles_indices[1][0])
        choice = tile_moves[choice_tile[0], choice_tile[1]]
        return choice
    
    def solve(self):
        print('solving')
        routes = [[self]] 
        for route in routes:
            board = route[-1]
            board.simplify()
            if board.is_done():
                print('simplify got it')
                return board.plan
            print('finding choices')
            choice = board.find_board_choice()
            for move in choice:
                new_board = move['new_board']
                new_route = [*route, new_board]
                if new_board.is_done():
                    print('one move got it')
                    print(move)
                    print(new_board.grid.matrix)
                    return new_board.plan
                else:
                    routes.append(new_route)
            print('going to next route')
        print('Damn didnt get it')
        return None

    def is_done(self):
        return self.grid.matrix.sum() == 0

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
            (5, 'Red'),
            (6, 'Red'),
            (7, 'Red'),

            (6, 'Red'),
            (6, 'Blu'),
            (6, 'Yel'),

            (1, 'Red'),
            (2, 'Red'),
            (3, 'Red'),
            (4, 'Red'),

            (7, 'Red'),
            (8, 'Red'),
            (9, 'Red'),
            (10, 'Red'),

            (10, 'Red'),
            (11, 'Red'),
            (12, 'Red'),

            (2, 'Yel'),
            (3, 'Yel'),
            (4, 'Yel'),
            (5, 'Yel'),

            (1, 'Blk'),
            (2, 'Blk'),
            (3, 'Blk'),
            (4, 'Blk'),
            (5, 'Blk'),
            (6, 'Blk'),
            (7, 'Blk'),

            (4, 'Yel'),
            (5, 'Yel'),
            (6, 'Yel'),
            (7, 'Yel'),

            (9, 'Yel'),
            (10, 'Yel'),
            (11, 'Yel'),
            (12, 'Yel'),

            # More in Goodnotes pictures
        ])
        print(board.solve())
        # except CantSolveTile:
        #     print('cant solve it')
