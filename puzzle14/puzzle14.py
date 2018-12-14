#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys

def part1(maxlenstr):
    maxlen = int(maxlenstr)
    recipelist = [3,7]
    elf1idx = 0
    elf2idx = 1
    while len(recipelist) < maxlen + 10:
        elf1recipe = recipelist[elf1idx]
        elf2recipe = recipelist[elf2idx]
        recipelist.extend(list(map(int, str(elf1recipe + elf2recipe))))
        elf1idx = (elf1idx + 1 + elf1recipe) % len(recipelist)
        elf2idx = (elf2idx + 1 + elf2recipe) % len(recipelist)
        #print("{} {} {}".format(elf1idx, elf2idx, recipelist))
    return recipelist[maxlen:maxlen+10]

def part2(sublisttosearch):
    recipelist = "37"
    elf1idx = 0
    elf2idx = 1
    searchidx = 0
    while True:
        elf1recipe = int(recipelist[elf1idx])
        elf2recipe = int(recipelist[elf2idx])
        newrecipes = str(elf1recipe + elf2recipe)
        recipelist += newrecipes
        elf1idx = (elf1idx + 1 + elf1recipe) % len(recipelist)
        elf2idx = (elf2idx + 1 + elf2recipe) % len(recipelist)
        if len(recipelist) < len(sublisttosearch):
            continue

        #print("{} {} {}".format(elf1idx, elf2idx, recipelist))
        idx = recipelist.find(sublisttosearch, searchidx)
        if idx != -1:
            return idx
        searchidx = len(recipelist) - len(sublisttosearch)
    return None

inputdata = sys.stdin.readline().strip()

print("Part1: {}".format(''.join(map(str, part1(inputdata)))))
print("Part2: {}".format(part2(inputdata)))

