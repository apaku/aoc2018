#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys


def parse(lines):
    for line in lines:
        yield tuple(map(int, line.split(",")))


def manhatten_distance(p1, p2):
    return sum([abs(x[0] - x[1]) for x in zip(p1, p2)])


def connects_to_constellation(constellation, point):
    for p in constellation:
        distance = manhatten_distance(p, point)
        if distance <= 3:
            return True
    return False


def part1(points):
    constellations = [[p] for p in points]
    while True:
        newconstellations = []
        for i in range(len(constellations)):
            constellation = constellations[i]
            constellation_to_merge = None
            for p in constellation:
                for newconstellation in newconstellations:
                    if connects_to_constellation(newconstellation, p):
                        constellation_to_merge = newconstellation
                        break
                if constellation_to_merge is not None:
                    break
            if constellation_to_merge is not None:
                for p in constellation:
                    newconstellation.append(p)
            else:
                newconstellations.append(constellation)
        if len(newconstellations) == len(constellations):
            break
        constellations = newconstellations
    return len(constellations)


points = list(parse(sys.stdin.readlines()))
print("Part1: {}".format(part1(points)))