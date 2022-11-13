weird_matrix = [
    [ 0, 0, 1, 1, 1, 2, 1, 1, 0, 1, 2, 2, 1], # Red
    [ 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 2, 0, 1], # Black
    [ 2, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2], # Blue
    [ 2, 1, 1, 0, 0, 0, 0, 1, 1, 1, 2, 1, 1], # Yellow
]

tiles = []
for rank in range(13):
    for suit in range(4):
        num_tiles = weird_matrix[suit][rank]
        for i in range(num_tiles):
            tiles.append((rank, suit))

print(tiles)