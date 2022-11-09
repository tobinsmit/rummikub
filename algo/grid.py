import numpy as np
import rules

class Grid():
    def __init__(self, tiles=None, plan=None):
        assert tiles or plan
        assert not (tiles and plan)

        self.matrix = np.zeros(shape=[len(rules.ranks), len(rules.suits)], dtype=int)

        if plan:
            tiles = []
            for group in plan:
                for tile in group:
                    tiles.append(tile)

        for tile in tiles:
            if type(tile[1]) == str:
                suit = rules.suitStringMap.index(tile[1])
            else:
                suit = tile[1]
            rank = tile[0]
            self.matrix[rank, suit] += 1

    def check_kernels_match(self, kernel_indexes, rank, suit):
        kernel = np.sum([self.kernels[k] for k in kernel_indexes], 0)
        for kernel_rank in range(len(kernel)):
            for kernel_suit in range(len(kernel[0])):
                kernel_val = kernel[kernel_rank, kernel_suit]
                if kernel_val > 0:
                    # TODO make this work and make tests
                    if rules.loop13to1:
                        matrix_rank = (kernel_rank - 2 + rank) % len(rules.ranks)
                    else:
                        matrix_rank = (kernel_rank - 2 + rank)
                        if matrix_rank < 0 or matrix_rank >= len(rules.ranks):
                            continue
                    matrix_suit = (kernel_suit + suit) % len(rules.suits)
                    matrix_val = self.matrix[matrix_rank, matrix_suit]
                    if matrix_val < kernel_val:
                        return False
        
        return True

    def kernel_to_group_option(self, kernel_idx, rank, suit):
        kernel = self.kernels[kernel_idx]
        group = []
        new_matrix = np.array(self.matrix, copy=True)
        for kernel_rank in range(len(kernel)):
            for kernel_suit in range(len(kernel[0])):
                kernel_val = kernel[kernel_rank, kernel_suit]
                if kernel_val > 0:
                    # TODO make this work and make tests
                    if rules.loop13to1:
                        matrix_rank = (kernel_rank - 2 + rank) % len(rules.ranks)
                    else:
                        matrix_rank = (kernel_rank - 2 + rank)
                        if matrix_rank < 0 or matrix_rank >= len(rules.ranks):
                            raise Exception('Going around the bend but shouldnt')
                    matrix_suit = (kernel_suit + suit) % len(rules.suits)
                    group.append((matrix_rank, matrix_suit))
                    new_matrix[matrix_rank, matrix_suit] -= 1
        option = {
            'type': 'new_group',
            'group': group,
            'new_matrix': new_matrix,
        }
        return option


    def find_tile_new_group_options(self, rank, suit):
        options = []
        for kernel_idx in range(len(self.kernels)):
            works = self.check_kernels_match([kernel_idx], rank, suit)
            if works:
                option = self.kernel_to_group_option(kernel_idx, rank, suit)
                options.append(option)        
        return options
        
    # TODO update kernels to reflect change in axes
    kernels = np.array([
        [
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    ])

def test_check_kernels_match():
    g = Grid(tiles=[
        (1,0),
        (2,0),
        (3,0),
        (6,0),
        (6,1),
        (6,2),
    ])

    assert g.check_kernels_match()