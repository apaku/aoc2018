#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import collections
import itertools
import re
import sys

def part1(numPlayers, lastMarble):
    playerlist = range(1, numPlayers + 1)
    turns = collections.deque(itertools.islice(itertools.cycle(playerlist), 0, lastMarble+1))
    playercounts = dict(map(lambda x: (x, 0), playerlist))
    circle = collections.deque([0])
    for marbleNum in range(1, lastMarble + 1):
        curPlayer = turns.popleft()
        if marbleNum % 23 == 0:
            playercounts[curPlayer] += marbleNum
            circle.rotate(7)
            playercounts[curPlayer] += circle.pop()
            circle.rotate(-1)
        else: 
            circle.rotate(-1)
            circle.append(marbleNum)
    return max(playercounts.items(), key=lambda x: x[1])

def part2(numPlayers, lastMarble):
    return part1(numPlayers, lastMarble * 100)

input_re = re.compile(r'(\d+) players; last marble is worth (\d+) points')
match = input_re.match(sys.stdin.read().strip())
numPlayers = int(match.group(1))
lastMarble = int(match.group(2))

import cProfile, pstats
print("Part1: {}".format(part1(numPlayers, lastMarble)))
print("Part2: {}".format(part2(numPlayers, lastMarble)))
