#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

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
    overlappedrect = {
        'x1': max(r1['x1'], r2['x1']),
        'x2': min(r1['x2'], r2['x2']),
        'y1': max(r1['y1'], r2['y1']),
        'y2': min(r1['y2'], r2['y2'])
    }
    points = set()
    for x in range(overlappedrect['x1'], overlappedrect['x2']):
        for y in range(overlappedrect['y1'], overlappedrect['y2']):
            points.add((x, y))
    return points

def overlap(r1, r2):
    if not overlaps(r1, r2):
        if overlaps(r2, r1):
            return calculateoverlap(r2, r1)
        else:
            return set()
    return calculateoverlap(r1, r2)

def overlappedpoints(rect, others):
    allpoints = set()
    for other in others:
        allpoints = allpoints.union(overlap(rect, other))
    return allpoints

def part2(rects):
    allpoints = set()
    for i in range(len(rects)):
        allpoints = allpoints.union(overlappedpoints(rects[i], rects[i+1:]))
    return len(allpoints)

print("{}".format(part2(map(parse, sys.stdin.readlines()))))