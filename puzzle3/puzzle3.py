#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

from collections import Counter
import sys
import re

line_re = re.compile(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$")
def parse(line):
    match = line_re.match(line)
    return {'id': int(match.group(1)),
    'x1': int(match.group(2)),
    'y1': int(match.group(3)),
    'x2': int(match.group(2)) + int(match.group(4)),
    'y2': int(match.group(3)) + int(match.group(5))}

def overlaps(r1, r2):
    return r1['x1'] < r2['x2'] and r1['y1'] < r2['y2'] \
        and r1['x2'] > r2['x1'] and r1['y2'] > r2['y1']

def calculateoverlap(r1, r2):
    x1 = max(r1['x1'], r2['x1'])
    x2 = min(r1['x2'], r2['x2'])
    y1 = max(r1['y1'], r2['y1'])
    y2 = min(r1['y2'], r2['y2'])
    for x in range(x1, x2):
        for y in range(y1, y2):
            yield (x,y)

def generate_all_points(rects):
    for rect in rects:
        for x in range(rect['x1'], rect['x2']):
            for y in range(rect['y1'], rect['y2']):
                yield (x, y)

def part1(rects):
    counter = Counter(generate_all_points(rects))
    return len(list(filter(lambda x: x[1] > 1, counter.items())))

rects = list(map(parse, sys.stdin.readlines()))

print("Part1: {}".format(part1(rects)))
