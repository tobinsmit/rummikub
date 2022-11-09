import numpy as np
import rules

class Grid():
    def __init__(self, tiles=None, plan=None):
        assert tiles or plan
        assert not (tiles and plan)

        self.matrix = np.zeros(shape=[len(rules.colorOptions), len(rules.numberOptions)], dtype=int)

        if plan:
            tiles = []
            for group in plan:
                for tile in group:
                    tiles.append(tile)

        for tile in tiles:
            number_idx = tile[0]
            if type(tile[1]) == str:
                color_idx = rules.colorStringMap.index(tile[1])
            else:
                color_idx = tile[1]
            self.matrix[color_idx, number_idx] += 1

    def check_kernels_match(self, kernel_indexes, color_idx, number_idx):
        kernel = np.sum([self.kernels[k] for k in kernel_indexes], 0)
        for kernel_row in range(len(kernel)):
            for kernel_col in range(len(kernel[0])):
                kernel_val = kernel[kernel_row, kernel_col]
                if kernel_val > 0:
                    matrix_row = (kernel_row + color_idx) % len(rules.colorOptions)
                    if rules.loop13to1:
                        matrix_col = (kernel_col - 2 + number_idx) % len(rules.numberOptions)
                    else:
                        matrix_col = (kernel_col - 2 + number_idx)
                        if matrix_col < 0 or matrix_col >= len(rules.numberOptions):
                            continue
                    matrix_val = self.matrix[matrix_row, matrix_col]
                    if matrix_val < kernel_val:
                        return False
        
        return True

    def kernel_to_group_option(self, kernel_idx, color_idx, number_idx):
        kernel = self.kernels[kernel_idx]
        group = []
        new_matrix = np.array(self.matrix, copy=True)
        for kernel_row in range(len(kernel)):
            for kernel_col in range(len(kernel[0])):
                kernel_val = kernel[kernel_row, kernel_col]
                if kernel_val > 0:
                    matrix_row = (kernel_row + color_idx) % len(rules.colorOptions)
                    if rules.loop13to1:
                        matrix_col = (kernel_col - 2 + number_idx) % len(rules.numberOptions)
                    else:
                        matrix_col = (kernel_col - 2 + number_idx)
                        if matrix_col < 0 or matrix_col >= len(rules.numberOptions):
                            raise Exception('Going around the bend but shouldnt')
                    group.append((matrix_col, matrix_row))
                    new_matrix[matrix_row, matrix_col] -= 1
        option = {
            'type': 'new_group',
            'group': group,
            'new_matrix': new_matrix,
        }
        return option


    def find_tile_new_group_options(self, color_idx, number_idx):
        options = []
        for kernel_idx in range(len(self.kernels)):
            works = self.check_kernels_match([kernel_idx], color_idx, number_idx)
            if works:
                option = self.kernel_to_group_option(kernel_idx, color_idx, number_idx)
                options.append(option)        
        return options
        
    kernels = np.array([
        [
            [1,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        [
            [0,1,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        [
            [0,0,1,1,1],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
        ],
        [
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
        ],
        [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
            [0,0,1,0,0],
        ],
        [
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,0,0,0,0],
        ],
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