
import rules
from plan import Plan
from grid import Grid

class Game():
    def __init__(self, tiles):
        self.grid = Grid(tiles=tiles)
        self.original_grid = Grid(tiles=tiles)
        self.plan = Plan()

    def find_tile_options(self, rank, suit):
        new_group_options = self.grid.find_tile_new_group_options(rank, suit)
        grid_to_plan_options = self.plan.find_tile_add_to_group_options(rank, suit)
        return [*new_group_options, *grid_to_plan_options]
        
    def solve(self):
        fresh_changes = True
        while fresh_changes:
            for rank in rules.ranks:
                for suit in rules.suits:
                    tiles_unplaced = self.grid.matrix[rank, suit]
                    if tiles_unplaced == 0:
                        continue
                    elif tiles_unplaced < 0:
                        raise Exception()
                    elif tiles_unplaced > 2:
                        raise Exception()
                    
                    options = self.find_tile_options(rank, suit)

                    if len(options) == 0:
                        raise Exception('Tile has no options')
                    elif len(options) == tiles_unplaced:
                        # All options must be true
                        for option in options:
                            # Enact option
                            #TODO
                            pass
                            
                        fresh_changes = True
                        

if __name__ == '__main__':
    game = Game(tiles=[
        (6,'Red'),
        (7,'Blk'),
        (8,'Blk'),
    ])
    game.solve()