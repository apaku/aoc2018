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


def getrecipevals(recipes, idx1, idx2):
    return (recipes[idx1], recipes[idx2])


def getnewrecipe(recipe1, recipe2):
    newrecipe = recipe1 + recipe2
    if newrecipe > 9:
        return [1, newrecipe % 10]
    return [newrecipe % 10]


def getnewidx(idx1, idx2, r1, r2, lenr):
    return ((idx1 + 1 + r1) % lenr, (idx2 + 1 + r2) % lenr)


def findsublist(l, lenl, sublist, lensublist):
    def getslice(l, idx1, idx2):
        return l[idx1:idx2]

    if getslice(l, -lensublist, lenl) == sublist:
        return lenl - lensublist
    if getslice(l, -lensublist - 1, -1) == sublist:
        return lenl - lensublist - 1
    return None


def part2(sublisttosearch):
    recipelist = [3, 7]
    elf1idx = 0
    elf2idx = 1
    lensublisttosearch = len(sublisttosearch)
    while True:
        (elf1recipe, elf2recipe) = getrecipevals(recipelist, elf1idx, elf2idx)
        newrecipedigits = getnewrecipe(elf1recipe, elf2recipe)
        recipelist.extend(newrecipedigits)
        lenrecipes = len(recipelist)
        (elf1idx, elf2idx) = getnewidx(elf1idx, elf2idx, elf1recipe,
                                       elf2recipe, lenrecipes)
        if lenrecipes < lensublisttosearch:
            continue

        #print("{} {} {}".format(elf1idx, elf2idx, recipelist))
        idx = findsublist(recipelist, lenrecipes, sublisttosearch,
                          lensublisttosearch)
        if idx is not None:
            return idx
    return None


inputdata = sys.stdin.readline().strip()

#print("Part1: {}".format(''.join(map(str, part1(inputdata)))))
import cProfile
import pstats
p = cProfile.Profile()
p.enable()
print("Part2: {}".format(part2(list(map(int, inputdata)))))
p.disable()
s = pstats.Stats(p)
s.sort_stats("tottime", "cumtime")
s.print_stats()