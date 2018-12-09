#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys

class Node():
    def __init__(self, id):
        self.id = id
        self.children = []
        self.metadata = []
        self._value = None
    def __repr__(self):
        str = "{}: {}".format(self.id, self.metadata)
        for c in self.children:
            str += "\n  " + c.__repr__()
        return str
    def childvalue(self, idx):
        if idx >= 0 and idx < len(self.children):
            return self.children[idx].value()
        return 0
    def value(self):
        if self._value is None:
            if len(self.children) > 0:
                self._value = sum(map(lambda x: self.childvalue(x-1), self.metadata))
            else:
                self._value = sum(self.metadata)
        return self._value

cnt = 65

def parse(data):
    numChilds = data[0]
    numMetaData = data[1]
    datarest = data[2:]
    node = Node(chr(cnt))
    while numChilds > 0:
        (datarest, child) = parse(datarest)
        numChilds -= 1
        node.children.append(child)
    for i in range(numMetaData):
        node.metadata.append(datarest[i])
    return (datarest[numMetaData:], node)

def part1(node):
    return sum(map(lambda x: part1(x), node.children)) + sum(node.metadata)

def part2(root):
    return root.value()

data = list(map(int, sys.stdin.readlines()[0].strip().split()))
rootnode = parse(data)[1]
print("{}".format(part1(rootnode)))
print("{}".format(part2(rootnode)))