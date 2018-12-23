#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys


def parse(lines):
    target = lines[1][len("target: "):].split(",")
    return (int(lines[0][len("depth: "):]), (int(target[0]), int(target[1])))


def calc_geo_index(coord, target, depth):
    if coord == (0, 0):
        return 0
    if coord == target:
        return 0
    if coord[1] == 0:
        return coord[0] * 16807
    if coord[0] == 0:
        return coord[1] * 48271
    level_left = erosion_level((coord[0] - 1, coord[1]), target, depth)
    level_above = erosion_level((coord[0], coord[1] - 1), target, depth)
    return level_left * level_above


geo_indices = {}


def geo_index(coord, target, depth):
    if coord not in geo_indices:
        geo_indices[coord] = calc_geo_index(coord, target, depth)
    return geo_indices[coord]


erosion_levels = {}


def erosion_level(coord, target, depth):
    if coord not in erosion_levels:
        idx = geo_index(coord, target, depth)
        erosion_levels[coord] = (idx + depth) % 20183
    return erosion_levels[coord]


def region_type(coord, target, depth):
    return erosion_level(coord, target, depth) % 3


def render(target, depth):
    for y in range(target[1]):
        line = ""
        for x in range(target[0]):
            if x == 0 and y == 0:
                line += 'M'
            elif x == target[0] and y == target[1]:
                line += 'T'
            else:
                region = region_type((x, y), target, depth)
                if region == 0:
                    line += "."
                elif region == 1:
                    line += "="
                elif region == 2:
                    line += "|"
        print(line)


def risk_level(target, depth):
    return sum([
        region_type((x, y), target, depth) for y in range(target[1] + 1)
        for x in range(target[0] + 1)
    ])


(depth, target) = parse(sys.stdin.readlines())

render(target, depth)
print("Part1: {}".format(risk_level(target, depth)))