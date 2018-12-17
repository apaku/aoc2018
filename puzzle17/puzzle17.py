#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import re
import sys

parse_re = re.compile(r"([xy])=(\d+), ([xy])=(\d+)..(\d+)")


def parseclay(line):
    match = parse_re.match(line)
    coord1 = match.group(1)
    coord1val = int(match.group(2))
    coord2 = match.group(3)
    line = []
    for c in range(int(match.group(4)), int(match.group(5)) + 1):
        if coord1 == 'x':
            line.append((coord1val, c))
        else:
            line.append((c, coord1val))
    return line


def part1(claycoordinates):
    coords_set = set(claycoordinates)
    sorted_coords = sorted(claycoordinates)
    minx = min(sorted_coords, key=lambda c: c[0])[0]
    maxx = max(sorted_coords, key=lambda c: c[0])[0]
    maxy = max(sorted_coords, key=lambda c: c[1])[1]
    for y in range(0, maxy + 1):
        line = ""
        for x in range(minx, maxx):
            if y == 0 and x == 500:
                line += "+"
            elif (x, y) in coords_set:
                line += "#"
            else:
                line += "."
        print(line)
    return (minx, maxx, 0, maxy)


print("Part1: {}".format(
    part1([line for l in sys.stdin.readlines() for line in parseclay(l)])))
