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
        assert iter(kernel_indexes), 'kernel_indexes not iterable'
        kernel = np.sum([self.kernels[k] for k in kernel_indexes], 0)
        for kernel_rank in range(len(kernel)):
            for kernel_suit in range(len(kernel[0])):
                kernel_val = kernel[kernel_rank, kernel_suit]
                if kernel_val > 0:
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
        assert type(kernel_idx) is not list
        assert type(kernel_idx) is not np.array
        kernel = self.kernels[kernel_idx]
        group = []
        new_matrix = np.array(self.matrix, copy=True)
        for kernel_rank in range(len(kernel)):
            for kernel_suit in range(len(kernel[0])):
                kernel_val = kernel[kernel_rank, kernel_suit]
                if kernel_val > 0:
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


    def find_tile_new_group_moves(self, rank, suit):
        options = []
        for kernel_idx in range(len(self.kernels)):
            works = self.check_kernels_match([kernel_idx], rank, suit)
            if works:
                option = self.kernel_to_group_option(kernel_idx, rank, suit)
                options.append(option)        
        return options
        
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
    assert g.check_kernels_match([2], 1, 0) # 1 and higher
    assert g.check_kernels_match([1], 2, 0) # 2 and sides
    assert g.check_kernels_match([0], 3, 0) # 3 and lower
    assert not g.check_kernels_match([0], 1, 0)
    assert not g.check_kernels_match([1], 1, 0)
    assert not g.check_kernels_match([3], 1, 0)
    assert not g.check_kernels_match([4], 1, 0)
    assert not g.check_kernels_match([5], 1, 0)
    assert g.check_kernels_match([5], 6, 0)
    assert g.check_kernels_match([4], 6, 1)
    assert g.check_kernels_match([3], 6, 2)
    assert not g.check_kernels_match([0], 6, 0)
    assert not g.check_kernels_match([1], 6, 0)
    assert not g.check_kernels_match([2], 6, 0)
    assert not g.check_kernels_match([3], 6, 0)
    assert not g.check_kernels_match([4], 6, 0)
    assert not g.check_kernels_match([0], 6, 3)
    assert not g.check_kernels_match([1], 6, 3)
    assert not g.check_kernels_match([2], 6, 3)
    assert not g.check_kernels_match([3], 6, 3)
    assert not g.check_kernels_match([4], 6, 3)
    assert not g.check_kernels_match([5], 6, 3)
    move = g.kernel_to_group_option(5,6,0)
    group = move['group']
    assert set(group) == set([(6,1),(6,2),(6,0)])
    move = g.kernel_to_group_option(1,2,0)
    group = move['group']
    assert set(group) == set([(3,0),(1,0),(2,0)])
    print('All tests passed :)')

if __name__ == '__main__':
    test_check_kernels_match()
