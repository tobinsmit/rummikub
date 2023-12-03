
ranks = list(range(13))
suit_icons = ['🟥','🟫','🟦','🟨']
num_suits = len(suit_icons)
loop13to1 = False

def label_to_rank_and_suit(label):
    for index, icon in enumerate(suit_icons):
        if label.startswith(icon):
            suit = index
            break
    else:
        print(f"{label=}")
        raise Exception("Bad suit icon")
    
    rank = int(str(label[len(icon)+1:])) - 1
    return (rank, suit)

def rank_and_suit_to_label(rank, suit):
    return f"{suit_icons[suit]} {rank+1}"
