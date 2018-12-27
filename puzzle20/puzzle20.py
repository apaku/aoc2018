#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import sys


def parse(idx, data):
    paths = []
    datalen = len(data)
    buf = ""
    curalternativepaths = [""]
    while idx < datalen:
        c = data[idx]
        if c == '|':
            if len(buf) > 0:
                for i in range(len(curalternativepaths)):
                    curalternativepaths[i] += buf
            buf = ""
            paths += curalternativepaths
            curalternativepaths = [""]
        elif c == '(':
            if len(buf) > 0:
                for i in range(len(curalternativepaths)):
                    curalternativepaths[i] += buf
            buf = ""
            (nextidx, subpaths) = parse(idx + 1, data)
            newcuralternativepaths = []
            for p in curalternativepaths:
                for sp in subpaths:
                    newcuralternativepaths.append(p + sp)
            curalternativepaths = newcuralternativepaths
            idx = nextidx
            continue
        elif c == ')':
            if len(buf) > 0:
                for i in range(len(curalternativepaths)):
                    curalternativepaths[i] += buf
            buf = ""
            if len(curalternativepaths) > 0:
                paths += curalternativepaths
            return (idx + 1, paths)
        else:
            buf += c
        idx += 1
    if len(buf) > 0:
        for i in range(len(curalternativepaths)):
            curalternativepaths[i] += buf
    buf = ""
    if len(curalternativepaths) > 0:
        paths += curalternativepaths
    return (idx, paths)


def test_p1():
    data = 'abcd'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcd']


def test_p2():
    data = '(abcd)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcd']


def test_p3():
    data = '(ab|cd)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['ab', 'cd']


def test_p4():
    data = '(ab|cd|ef)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['ab', 'cd', 'ef']


def test_p5():
    data = 'ab(cd|ef)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcd', 'abef']


def test_p6():
    data = 'ab(cd|ef)gh'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcdgh', 'abefgh']


def test_p7():
    data = 'ab((cd)|ef)gh'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcdgh', 'abefgh']


def test_p8():
    data = 'ab((cd|ef)gh|ij)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcdgh', 'abefgh', 'abij']


def test_p9():
    data = 'ab(cd|)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcd', 'ab']


def test_p10():
    data = 'ab(cd|)ef'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcdef', 'abef']


def test_p11():
    data = 'ab((cd|gh|)|ef)'
    parsed = parse(0, data)
    print("Parsed: {} into {}".format(data, parsed))
    assert parsed[1] == ['abcd', 'abgh', 'ab', 'abef']


def tests():
    test_p1()
    test_p2()
    test_p3()
    test_p4()
    test_p5()
    test_p6()
    test_p7()
    test_p8()
    test_p9()
    test_p10()
    test_p11()


# def parse(idx, data):
#     parsed = ""
#     datalen = len(data)
#     while idx < datalen:
#         c = data[idx]
#         print("{} {}".format(idx, c))
#         if c == '(':
#             print("recurse1")
#             (subparsed, nextidx) = parse(idx + 1, data)
#             print("branch1 parse: {}".format(subparsed))
#             idx = nextidx
#         elif c == '|':
#             print("recurse2")
#             (subparsed, nextidx) = parse(idx + 1, data)
#             print("branch2 parse: {}".format(subparsed))
#             idx = nextidx
#         elif c == ')':
#             print("exit recurse")
#             return (parsed, idx + 1)
#         else:
#             parsed += c
#             idx += 1
#     return (parsed, idx)


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


def shorted_walk_distance(path):
    p = Path()
    nextstep = 0
    print("Path len: {}".format(len(path)))
    while nextstep < len(path):
        s = path[nextstep]
        curpoint = p.curpoint()
        newpoint = step(s, curpoint)
        if newpoint in p.points_seen:
            p.revert_to(p.points_seen[newpoint])
        else:
            p.add_step(newpoint)
        nextstep += 1
    return len(p.points_to_walk) - 1


def part1(paths):
    return max(map(lambda p: shorted_walk_distance(p), paths))


tests()

path = sys.stdin.readline().strip()
print("path: {}".format(path))
parsed = parse(0, path[1:-1])
print("{}".format(parsed))
print("Part1: {}".format(part1(parsed[1])))