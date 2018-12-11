#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys

level_cache = {}

def power_level(cell, serialnum):
    if cell not in level_cache:
        rackId = cell[0] + 10
        power = rackId * cell[1]
        power += serialnum
        power = power * rackId
        digits = list(str(power))
        if len(digits) > 2:
            power = int(digits[-3])
        else:
            power = 0
        power -= 5
        level_cache[cell] = power
    return level_cache[cell]

def grid_power_levels(topleftcell, serialnum, gridsize=3):
    topx = topleftcell[0]
    topy = topleftcell[1]
    grid = itertools.product(range(topx, topx+gridsize), range(topy,topy+gridsize))
    return map(lambda p: power_level(p, serialnum), grid)

def part1(serialnum):
    allcells = itertools.product(range(1, 299), range(1, 299))
    return max(map(lambda p: (sum(grid_power_levels(p, serialnum)), p), allcells))

def max_grid_power_levels(startcell, serialnum):
    gridsize = 1
    oldsum = 0
    while startcell[0] + gridsize < 301:
        powerlevel = sum(grid_power_levels(startcell, serialnum, gridsize))
        if powerlevel < oldsum:
            return (startcell, oldsum, gridsize - 1)
        oldsum = powerlevel
        gridsize += 1
    return (startcell, oldsum, gridsize - 1)


def part2(serialnum):
    allcells = itertools.product(range(1, 299), range(1, 299))
    grid = map(lambda p: max_grid_power_levels(p, serialnum), allcells)
    return max(grid, key=lambda x: x[1])

serialnum = int(sys.stdin.readline().strip())
print("Part1: {}".format(part1(serialnum)))
print("Part2/18: {}".format(part2(18)))
print("Part2/42: {}".format(part2(42)))
print("Part2: {}".format(part2(serialnum)))