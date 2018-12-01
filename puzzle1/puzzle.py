#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys

def part1(changes):
    return sum(changes)

def part2(changes):
    seenfrequencies = set()
    frequency = 0
    for change in itertools.cycle(changes):
        if frequency in seenfrequencies:
            return frequency
        seenfrequencies.add(frequency)
        frequency += change

changes = [int(x) for x in sys.stdin.readlines()]
print("Part1: {}".format(part1(changes)))
print("Part2: {}".format(part2(changes)))
