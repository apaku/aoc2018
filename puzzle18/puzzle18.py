#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import collections
import sys


def parse(lines):
    for (y, line) in enumerate(lines):
        for (x, c) in enumerate(line.strip()):
            yield ((x, y), c)


def render(area, size):
    for y in range(0, size):
        line = ""
        for x in range(0, size):
            line += area[(x, y)]
        print(line)


def statearound(x, y, area, size):
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            #print("For {}/{} checking at {}/{}".format(x, y, nx, ny))
            if nx == x and ny == y:
                continue
            if nx >= 0 and nx < size and ny >= 0 and ny < size:
                #print("For {}/{} yielding at {}/{}".format(x, y, nx, ny))
                yield area[(nx, ny)]


def nextstate(x, y, area, size):
    curstate = area[(x, y)]
    statesaround = statearound(x, y, area, size)
    c = collections.Counter(statesaround)
    #print("at: {}/{}, value: {}, counter:{}".format(x, y, area[(x, y)], c))
    if curstate == '.':
        if c['|'] >= 3:
            return '|'
    elif curstate == '|':
        if c['#'] >= 3:
            return '#'
    elif curstate == '#':
        if c['#'] >= 1 and c['|'] >= 1:
            return curstate
        else:
            return '.'
    return curstate


def step(area, size):
    newarea = {}
    for y in range(0, size):
        for x in range(0, size):
            newarea[(x, y)] = nextstate(x, y, area, size)
    return newarea


def part1(area, size):
    newarea = dict(area)
    for i in range(0, 10):
        newarea = step(newarea, size)
    wooded = filter(lambda x: x[1] == '|', newarea.items())
    lumberyards = filter(lambda x: x[1] == '#', newarea.items())

    return len(list(wooded)) * len(list(lumberyards))


def part2(area, size):
    targetminute = 431 + ((1000000000 - 431) % 28)
    # Used the following to determine where the loop starts, how long it is etc.
    newarea = dict(area)
    values = {}
    for i in range(0, 600):
        newarea = step(newarea, size)
        wooded = filter(lambda x: x[1] == '|', newarea.items())
        lumberyards = filter(lambda x: x[1] == '#', newarea.items())
        resourcevalue = len(list(wooded)) * len(list(lumberyards))
        if i == targetminute - 1:
            return resourcevalue
        values[resourcevalue] = i


area = dict(parse(sys.stdin.readlines()))
size = max(map(lambda x: x[0], area.keys())) + 1
print("Part1: {}".format(part1(area, size)))
print("Part2: {}".format(part2(area, size)))