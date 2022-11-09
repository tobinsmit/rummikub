import numpy as np

import rules

class Plan():
    def __init__(self, group_list=[]):
        # String to enum
        self.group_list = []
        for group in group_list:
            self.group_list.append([])
            for tile in group:
                num = tile[0]
                if type(tile[1]) == str:
                    suit = rules.suitStringMap.index(tile[1])
                else:
                    suit = int(tile[1])
                self.group_list[-1].append((num, suit))


    def __str__(self):
        # return str(self.group_list)
        s = '['
        for i, group in enumerate(self.group_list):
            if i:
                s = s + ',\n '
            s = s + '['
            for j, tile in enumerate(group):
                s = s + f'({tile[0]:>2}, {rules.suitStringMap[tile[1]]})'
                if j < len(group)-1:
                    s = s + ', '
            s = s + ']'
        s = s + ']'
        return s

    def is_valid(self, verbose=False):
        for group in self.group_list:
            if not Plan.is_group_valid(group):
                return False
        return True

    def is_group_valid(group, verbose=False):
        if len(group) < 3:
            if verbose:
                print('Group too short')
            return False

        ranksList = [tile[0] for tile in group]
        suitsList = [tile[1] for tile in group]
        ranksSet = set(ranksList)
        suitsSet = set(suitsList)

        isGroupOfranks = len(ranksSet) > 1
        isGroupOfsuits = len(suitsSet) > 1

        if isGroupOfranks and isGroupOfsuits:
            if verbose:
                print('rank group and suit group')
            return False
        
        if isGroupOfranks:
            # Check ranks are consecutive
            sortedranks = np.sort(ranksList)
            sortedranksDiff = np.diff(sortedranks)
            if not np.all(sortedranksDiff == 1):
                if verbose:
                    print('rank group not consecutive')
                return False

        if isGroupOfsuits:
            if len(suitsSet) != len(group):
                if verbose:
                    print('Repeated suits')
                return False

        return True

    def find_tile_add_to_group_options(self, rank, suit):
        # TODO
        return []

def test_plan_class():
    def unit_test_valid(group_list, is_valid, error_msg):
        assert Plan(group_list).is_valid() == is_valid, error_msg
        
    assert Plan([[(6, 'Red'), (7, 'Red'), (8, 'Red')]]).is_valid() == True, 'Does not work for normal group of ranks'
    assert Plan([[(10, 'Blu'), (10, 'Red'), (10, 'Blk')]]).is_valid() == True, 'Does not work for normal group of suits'
    assert Plan([[(6, 'Red'), (7, 'Red'), (9, 'Red')]]).is_valid() == False, 'Does not catch gap in group of ranks'
    assert Plan([[(6, 'Red'), (7, 'Red'), (8, 'Blu')]]).is_valid() == False, 'Does not catch group with multiple ranks and multiple suits'
    assert Plan([[(6, 'Red'), (6, 'Red'), (7, 'Red')]]).is_valid() == False, 'Does not catch rank group with double ups'
    assert Plan([[(10, 'Red'), (10, 'Red'), (10, 'Blk')]]).is_valid() == False, 'Does not catch suit group with double ups'
    assert Plan([[(10, 'Red'), (10, 'Blk')]]).is_valid() == False, 'Does not catch suit group with two tiles'
    assert Plan([[(6, 'Red'), (7, 'Red')]]).is_valid() == False, 'Does not catch rank group with two tiles'
    assert Plan([[(num, 'Red') for num in rules.ranks]]).is_valid() == True, 'Does not allow large rank group'
    
    assert Plan([
        [(6, 'Red'), (7, 'Red'), (8, 'Red')],
        [(10, 'Blu'), (10, 'Red'), (10, 'Blk'), (10,'Yel')],
    ]).is_valid() == True, 'Does not work with multiple  groups'
    
    assert Plan([
        [(6, 'Red'), (7, 'Red'), (8, 'Red')],
        [(10, 'Red'), (10, 'Red')],
    ]).is_valid() == False, 'Does not catch bad group in multiple groups'

    print('Unit tests passed')

if __name__=='__main__':
    test_plan_class()

    p = Plan([
        [(6, 'Red'), (7, 'Red'), (8, 'Red')],
        [(10, 'Blu'), (10, 'Red'), (10, 'Blk'), (10,'Yel')],
    ])
    print(p)