#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys

# Parse idea:
# parsePlainPath: get's an index and the data, reads until it finds one of the special tokens or EOF,
#                 returns a list with all read bytes (which may be empty) and the first index where a
#                 non-read byte is
# parseBranch: called when a '(' is encountered, received data and index of the '(', loops over the branches until it finds a ')' in the index returned
#              by the latest 'parse'. Concatenates the lists it gets, so it returns a list of all possible paths from all branches and the index after the ')'
# parse: called with index and data, loops until eof or index is not on a letter, calls parsePlainPath, the result is the 'start list' which may be empty,
#        if it encounters a '(' calls parseBranch and with each item in the resulting list and 'multiplexes' its own path list with the result
#        yielding a new list of nxm paths, returns that list plus the index it ended at (which may be eof)

# Once a list of all possible paths is determined, eliminate loops with the existing logic in step/part1,
# that is run through the path and find sub-parts that end up at the same location, eliminate those parts
# Finally determine lengths, find maximum


def parse(data):
    curnode = Path()
    idx = 0
    while idx < len(data):
        s = data[idx]
        if s == '(':
            curnode.children = parse(data[idx + 1:])


class Path:
    def __init__(self):
        self.points_seen = {(0, 0): 0}
        self.points_to_walk = [(0, 0)]

    def curpoint(self):
        return self.points_to_walk[-1]

    def add_step(self, newpoint):
        self.points_seen[newpoint] = len(self.points_to_walk)
        self.points_to_walk.append(newpoint)

    def revert_to(self, idx_to_revert_to):
        points_to_remove = self.points_to_walk[idx_to_revert_to + 1:]
        self.points_to_walk = self.points_to_walk[:idx_to_revert_to + 1]
        for p in points_to_remove:
            del self.points_seen[p]


def step(steptext, point):
    if steptext == 'N':
        return (point[0], point[1] - 1)
    elif steptext == 'W':
        return (point[0] - 1, point[1])
    elif steptext == 'E':
        return (point[0] + 1, point[1])
    elif steptext == 'S':
        return (point[0], point[1] + 1)
    else:
        raise Exception("Invalid step text: {}".format(steptext))


def part1(steplist):
    p = Path()
    nextstep = 1
    while nextstep < len(steplist):
        s = steplist[nextstep]
        if s == '(':
            nextstep = dobranch(p, steplist, s)
        else:
            curpoint = p.curpoint()
            newpoint = step(s, curpoint)
            if newpoint in p.points_seen:
                p.revert_to(p.points_seen[newpoint])
            else:
                p.add_step(newpoint)
            nextstep += 1
    return len(p.points_to_walk)


path = sys.stdin.readline().strip()
print("Pat1: {}".format(part1(list(path)[1:-1])))