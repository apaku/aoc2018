#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import heapq
import sys

class coord():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}".format({'id': self.id, 'x': self.x, 'y':self.y})

def parse(lines):
    counter = 0
    for line in lines:
        c = line.strip().split(',')
        yield coord(counter, int(c[0]), int(c[1]))
        counter += 1

def manhatten_distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

coords = list(parse(sys.stdin.readlines()))
minx = min(map(lambda c: c.x, coords))
maxx = max(map(lambda c: c.x, coords))
miny = min(map(lambda c: c.y, coords))
maxy = max(map(lambda c: c.y, coords))
coord_distances = {}
for x in range(minx, maxx + 1):
    for y in range(miny, maxy + 1):
        distances = sorted(map(lambda c: (manhatten_distance((c.x, c.y), (x, y)), c), coords), key=lambda x: x[0])
        if distances[0][0] != distances[1][0]:
            (d, c) = distances[0]
            if c.id not in coord_distances:
                coord_distances[c.id] = []
            coord_distances[c.id].append((d, (x,y), c))

def onborder(coords):
    for c in coords:
        x = c[1]
        if x[0] == minx or x[0] == maxx or x[1] == miny or x[1] == maxy:
            return True
    return False

filtereditems = filter(lambda x: not onborder(x[1]), coord_distances.items())

print("Part1: {} (dist, id, c)".format(max(map(lambda i: (len(i[1]), i[0], i[1][0]), filtereditems))))

def distcalc():
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            distsum = sum(map(lambda c: manhatten_distance((c.x, c.y), (x, y)), coords))
            if distsum < 10000:
                yield 1

print("Part2: {}".format(len(list(distcalc()))))