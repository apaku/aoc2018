#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys

def reactedchain(unreactedchain):
    chain = list(unreactedchain)
    while True:
        newchain = list(chain)
        for i in range(len(chain) - 1):
            c1 = chain[i]
            c2 = chain[i + 1]
            c1l = c1.lower()
            c2l = c2.lower()
            if c1l == c2l and (c1 != c2):
                newchain = chain[:i] + chain[i + 2:]
                break
        #newchain = list(reactedchain(chain))
        if len(newchain) == len(chain):
            break
        chain = newchain
    return chain

chain = sys.stdin.read().strip()
print("Part1 {}".format(len(reactedchain(chain))))
def lengthofreducedreactions(chain):
    chars = sorted(set(chain.lower()))
    for c in chars:
        reacted = reactedchain(filter(lambda x: x.lower() != c, chain))
        yield (len(reacted), c)

print("Part2: {}".format(min(lengthofreducedreactions(chain))))
