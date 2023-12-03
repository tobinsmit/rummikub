#!/usr/bin/env python3

import numpy as np
import copy
import rules


class Plan:
    def __init__(self, p_in=[]):
        # String to enum
        self.p = []
        for group in p_in:
            self.p.append([])
            for tile in group:
                num = tile[0]
                if type(tile[1]) == str:
                    suit = rules.suitStringMap.index(tile[1])
                else:
                    suit = int(tile[1])
                self.p[-1].append((num, suit))

    def print(self, tabs=0, suit_strings=False):
        indent = "\t" * tabs
        s = indent + "["
        for i, group in enumerate(self.p):
            if i:
                s = s + ",\n" + indent + " "
            s = s + "["
            for j, tile in enumerate(group):
                # s = s + f'({tile[0]:>2}, {rules.suitStringMap[tile[1]]})'
                if suit_strings:
                    s = s + f"({tile[0]:>2}, {rules.suitStringMap[tile[1]]})"
                else:
                    s = s + f"({tile[0]:>2}, {tile[1]})"
                if j < len(group) - 1:
                    s = s + ", "
            s = s + "]"
        s = s + "]"
        return s

    def __str__(self):
        return self.print()

    # def __repr__(self):
    #     return self.print()

    def is_valid(self, verbose=False):
        for group in self.p:
            if not Plan.is_group_valid(group):
                return False
        return True

    def is_group_valid(group, verbose=False):
        if len(group) < 3:
            if verbose:
                print("Group too short")
            return False

        ranksList = [tile[0] for tile in group]
        suitsList = [tile[1] for tile in group]
        ranksSet = set(ranksList)
        suitsSet = set(suitsList)

        isGroupOfRanks = len(ranksSet) > 1
        isGroupOfSuits = len(suitsSet) > 1

        if isGroupOfRanks and isGroupOfSuits:
            if verbose:
                print("rank group and suit group")
            return False

        if isGroupOfRanks:
            # Check ranks are consecutive
            sortedRanks = np.sort(ranksList)
            sortedRanksDiff = np.diff(sortedRanks)
            if not np.all(sortedRanksDiff == 1):
                if verbose:
                    print("rank group not consecutive")
                return False

        if isGroupOfSuits:
            if len(suitsSet) != len(group):
                if verbose:
                    print("Repeated suits")
                return False

        return True

    def find_tile_add_to_group_moves(self, rank, suit):
        """Given a tile, find moves adding it to a group"""
        options = []
        for group in self.p:
            new_group = [*group, (rank, suit)]
            res = Plan.is_group_valid(new_group)
            if res:
                new_plan = copy.deepcopy(self.p)
                i = new_plan.index(group)
                new_plan[i] = new_group
                option = {
                    "type": "add_to_group",
                    "old_group": group,
                    "new_group": new_group,
                    "new_plan": new_plan,
                    "rank": rank,
                    "suit": suit,
                }
                options.append(option)

        return options


def test_plan_class():
    def unit_test_valid(p, is_valid, error_msg):
        assert Plan(p).is_valid() == is_valid, error_msg

    assert (
        Plan([[(6, "🟥"), (7, "🟥"), (8, "🟥")]]).is_valid() == True
    ), "Does not work for normal group of ranks"
    assert (
        Plan([[(10, "🟦"), (10, "🟥"), (10, "⬛️")]]).is_valid() == True
    ), "Does not work for normal group of suits"
    assert (
        Plan([[(6, "🟥"), (7, "🟥"), (9, "🟥")]]).is_valid() == False
    ), "Does not catch gap in group of ranks"
    assert (
        Plan([[(6, "🟥"), (7, "🟥"), (8, "🟦")]]).is_valid() == False
    ), "Does not catch group with multiple ranks and multiple suits"
    assert (
        Plan([[(6, "🟥"), (6, "🟥"), (7, "🟥")]]).is_valid() == False
    ), "Does not catch rank group with double ups"
    assert (
        Plan([[(10, "🟥"), (10, "🟥"), (10, "⬛️")]]).is_valid() == False
    ), "Does not catch suit group with double ups"
    assert (
        Plan([[(10, "🟥"), (10, "⬛️")]]).is_valid() == False
    ), "Does not catch suit group with two tiles"
    assert (
        Plan([[(6, "🟥"), (7, "🟥")]]).is_valid() == False
    ), "Does not catch rank group with two tiles"
    assert (
        Plan([[(num, "🟥") for num in rules.ranks]]).is_valid() == True
    ), "Does not allow large rank group"

    assert (
        Plan(
            [
                [(6, "🟥"), (7, "🟥"), (8, "🟥")],
                [(10, "🟦"), (10, "🟥"), (10, "⬛️"), (10, "🟨")],
            ]
        ).is_valid()
        == True
    ), "Does not work with multiple  groups"

    assert (
        Plan(
            [
                [(6, "🟥"), (7, "🟥"), (8, "🟥")],
                [(10, "🟥"), (10, "🟥")],
            ]
        ).is_valid()
        == False
    ), "Does not catch bad group in multiple groups"

    print("Unit tests passed")


if __name__ == "__main__":
    test_plan_class()

    p = Plan(
        [
            [(6, "🟥"), (7, "🟥"), (8, "🟥")],
            [(10, "🟦"), (10, "🟥"), (10, "⬛️"), (10, "🟨")],
        ]
    )
    print(p)
