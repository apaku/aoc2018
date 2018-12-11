#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys

def power_level(cell, serialnum):
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
    return power

def grid_power_levels(topleftcell, inputgrid, gridsize=3):
    topx = topleftcell[0]
    topy = topleftcell[1]
    grid = itertools.product(range(topx, topx+gridsize), range(topy,topy+gridsize))
    return map(lambda p: inputgrid[p], grid)

def gridsum(p, grid):
    x = p[0]
    y = p[1]
    if x == 1 and y == 1:
        return grid[p]
    if x == 1:
        return grid[p] + grid[(x, y - 1)]
    if y == 1:
        return grid[p] + grid[(x - 1, y)]
    return grid[p] + grid[(x, y-1)] + grid[(x-1,y)] - grid[(x-1,y-1)]

def buildsumgrid(grid, size=301):
    allcells = itertools.product(range(1, size), range(1, size))
    sumgrid = dict(grid)
    for x in range(1, size):
        for y in range(1, size):
            sumgrid[(x, y)] = gridsum((x, y), sumgrid)
    return sumgrid

def generate_summed_areas(sumgrid, size, subsize):
    for x in range(1, size - subsize):
        for y in range(1, size - subsize):
            subgridsum = sumgrid[(x + subsize, y + subsize)] + sumgrid[(x, y)] - sumgrid[(x + subsize, y)] - sumgrid[(x, y + subsize)]
            yield ((x+1, y+1), subgridsum, subsize)

def part2(sumgrid, size=301):
    def helper():
        for subsize in range(2, size - 1):
            for x in generate_summed_areas(sumgrid, size, subsize):
                yield x
    return max(helper(), key=lambda x: x[1])

def part1(sumgrid, size=301):
    return max(generate_summed_areas(sumgrid, size, 3), key=lambda x: x[1])

def buildgrid(serialnum, size=301):
    allcells = itertools.product(range(1, size), range(1, size))
    return dict(map(lambda p: (p,power_level(p, serialnum)), allcells))

serialnum = int(sys.stdin.readline().strip())
grid = buildgrid(serialnum)
sumgrid = buildsumgrid(grid)
print("Part1: {}".format(part1(sumgrid)))
print("Part2/18: {}".format(part2(buildsumgrid(buildgrid(18)))))
print("Part2/42: {}".format(part2(buildsumgrid(buildgrid(42)))))
print("Part2: {}".format(part2(sumgrid)))