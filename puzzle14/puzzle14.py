#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys


def part1(maxlenstr):
    maxlen = int(maxlenstr)
    recipelist = [3, 7]
    elf1idx = 0
    elf2idx = 1
    while len(recipelist) < maxlen + 10:
        elf1recipe = recipelist[elf1idx]
        elf2recipe = recipelist[elf2idx]
        recipelist.extend(list(map(int, str(elf1recipe + elf2recipe))))
        elf1idx = (elf1idx + 1 + elf1recipe) % len(recipelist)
        elf2idx = (elf2idx + 1 + elf2recipe) % len(recipelist)
        #print("{} {} {}".format(elf1idx, elf2idx, recipelist))
    return recipelist[maxlen:maxlen + 10]


def part2(sublisttosearch):
    recipelist = [3, 7]
    elf1idx = 0
    elf2idx = 1
    lensublisttosearch = len(sublisttosearch)
    while True:
        elf1recipe = recipelist[elf1idx]
        elf2recipe = recipelist[elf2idx]
        newrecipe = elf1recipe + elf2recipe
        if newrecipe > 9:
            recipelist.append(1)
        recipelist.append(newrecipe % 10)
        lenrecipes = len(recipelist)
        elf1idx = (elf1idx + 1 + elf1recipe) % lenrecipes
        elf2idx = (elf2idx + 1 + elf2recipe) % lenrecipes
        if lenrecipes < lensublisttosearch:
            continue

        #print("{} {} {}".format(elf1idx, elf2idx, recipelist))
        if recipelist[-lensublisttosearch:] == sublisttosearch:
            return lenrecipes - lensublisttosearch
        if recipelist[-lensublisttosearch - 1:-1] == sublisttosearch:
            return lenrecipes - lensublisttosearch - 1
        if recipelist[-lensublisttosearch - 2:-2] == sublisttosearch:
            return lenrecipes - lensublisttosearch - 2
    return None


inputdata = sys.stdin.readline().strip()

print("Part1: {}".format(''.join(map(str, part1(inputdata)))))
print("Part2: {}".format(part2(list(map(int, inputdata)))))