#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys

def reactedchain(unreactedchain):
    def different_cases(a, b):
        return a.lower() == b.lower() and a != b
    chain = []
    for c in unreactedchain:
        if chain and different_cases(c, chain[-1]):
            chain.pop()
        else:
            chain.append(c)
    return chain

chain = sys.stdin.read().strip()
print("Part1 {}".format(len(reactedchain(chain))))
def lengthofreducedreactions(chain):
    chars = sorted(set(chain.lower()))
    for c in chars:
        reacted = reactedchain(filter(lambda x: x.lower() != c, chain))
        yield (len(reacted), c)

print("Part2: {}".format(min(lengthofreducedreactions(chain))))
