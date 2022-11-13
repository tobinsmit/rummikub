print('importing numpy')
import numpy as np
print('importing rules')
import rules
print('importing Plan')
from plan import Plan
print('importing Grid')
from grid import Grid

class Board():
    def __init__(self, tiles):
        self.grid = Grid(tiles=tiles)
        self.original_grid = Grid(tiles=tiles)
        self.plan = Plan()

    def find_tile_moves(self, rank, suit):
        new_group_moves = self.grid.find_tile_new_group_moves(rank, suit)
        add_to_group_moves = self.plan.find_tile_add_to_group_moves(rank, suit)
        return [*new_group_moves, *add_to_group_moves]
        
    def simplify(self):
        print('simplifying')
        fresh_changes = True
        while fresh_changes:
            print('\tsimplifying loopback')
            fresh_changes = False
            for rank in rules.ranks:
                for suit in rules.suits:
                    tiles_unplaced = self.grid.matrix[rank, suit]
                    if tiles_unplaced == 0:
                        continue
                    elif tiles_unplaced < 0:
                        raise Exception()
                    elif tiles_unplaced > 2:
                        raise Exception()
                    
                    moves = self.find_tile_moves(rank, suit)

                    if len(moves) == 0:
                        raise Exception('Tile has no moves')
                    elif len(moves) == tiles_unplaced:
                        # All moves must be true
                        for move in moves:
                            # Enact move
                            if move['type'] == 'new_group':
                                group = move['group']
                                new_matrix = move['new_matrix']
                                self.plan.p.append(group)
                                self.grid.matrix = new_matrix
                            elif move['type'] == 'add_to_group':
                                rank = move['rank']
                                suit = move['suit']
                                new_plan = move['new_plan']
                                self.plan.p = new_plan
                                self.grid.matrix[rank, suit] -= 1
                            else:
                                raise Exception('Bad move type')

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
            # print('board before simplify')
            # print('board.is_done()', board.is_done())
            # print(board.plan)
            # print(board.grid.matrix)
            board.simplify()
            # print('board after simplify')
            # print('board.is_done()', board.is_done())
            # print(board.plan)
            # print(board.grid.matrix)
            if board.is_done():
                return board.plan
            choice = board.find_board_choice()
            for move in choice:
                new_route = [*route, move.new_board]
                if move.new_board.is_done:
                    return move.new_board.plan
                else:
                    routes.append(new_route)

    def is_done(self):
        return self.grid.matrix.sum() == 0

if __name__ == '__main__':
    # board = Board(tiles=[
    #     (6,'Blk'),
    #     (7,'Blk'),
    #     (8,'Blk'),
    #     (9,'Blk'),
    # ])
    # print(board.solve())
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
    ])
    print(board.solve())
