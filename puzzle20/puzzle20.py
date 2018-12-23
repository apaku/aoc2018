#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys

# Parse idea:
# Determine a list of all possible paths given by the input. How??
# Recurse upon seeing '(', return only once the corresponding ')' has been seen.

# Once a list of all possible paths is determined, eliminate loops with the existing logic in step/part1,
# that is run through the path and find sub-parts that end up at the same location, eliminate those parts
# Finally determine lengths, find maximum


def parse(idx, data):
    parsed = ""
    datalen = len(data)
    while idx < datalen:
        c = data[idx]
        print("{} {}".format(idx, c))
        if c == '(':
            print("recurse1")
            (subparsed, nextidx) = parse(idx + 1, data)
            print("branch1 parse: {}".format(subparsed))
            idx = nextidx
        elif c == '|':
            print("recurse2")
            (subparsed, nextidx) = parse(idx + 1, data)
            print("branch2 parse: {}".format(subparsed))
            idx = nextidx
        elif c == ')':
            print("exit recurse")
            return (parsed, idx + 1)
        else:
            parsed += c
            idx += 1
    return (parsed, idx)


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
print("path: {}".format(path))
parsed = parse(0, path[1:-1])
print("{}".format(parsed))
#print("Pat1: {}".format(part1(list(path)[1:-1])))