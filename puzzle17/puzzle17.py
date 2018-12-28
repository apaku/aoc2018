#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import re
import sys

parse_re = re.compile(r"([xy])=(\d+), ([xy])=(\d+)..(\d+)")


def claycoordinates(lines):
    for line in lines:
        match = parse_re.match(line)
        coord1 = match.group(1)
        coord1val = int(match.group(2))
        coord2 = match.group(3)
        line = []
        for c in range(int(match.group(4)), int(match.group(5)) + 1):
            if coord1 == 'x':
                yield (coord1val, c)
            else:
                yield (c, coord1val)


def render(clay_set):
    minx = min(clay_set, key=lambda c: c[0])[0]
    maxx = max(clay_set, key=lambda c: c[0])[0]
    miny = min(clay_set, key=lambda c: c[1])[1]
    maxy = max(clay_set, key=lambda c: c[1])[1]
    for y in range(0, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            if y == 0 and x == 500:
                line += "+"
            elif (x, y) in clay_set:
                line += "#"
            else:
                line += "."
        print(line)


def below(point):
    return (point[0], point[1] + 1)


def is_clay(clay_set, point):
    return point in clay_set


def left(point):
    return (point[0] - 1, point[1])


def above(point):
    return (point[0], point[1] - 1)


def right(point):
    return (point[0] + 1, point[1])


def left_bucket_border(prev_bucket_border, area, fallpoint):
    point = fallpoint
    while True:
        if is_clay(area['clay'], point):
            return point
        if point[0] < area['minx'] or point[0] < prev_bucket_border[0]:
            return None
        point = left(point)


def right_bucket_border(prev_bucket_border, area, fallpoint):
    point = fallpoint
    while True:
        if is_clay(area['clay'], point):
            return point
        if point[0] > area['maxx'] or point[0] > prev_bucket_border[0]:
            return None
        point = right(point)


def amount_of_water_in_bucket_line(left_border, right_border, point):
    left_water = abs(left_border[0] - point[0]) - 1
    right_water = abs(right_border[0] - point[0]) - 1
    return left_water + right_water


def left_bucket_bottom_end(area, fallpoint):
    point = (fallpoint[0], fallpoint[1] + 1)
    while True:
        if not is_clay(area['clay'], point):
            return right(point)
        assert point[0] <= area['maxx']
        point = left(point)


def right_bucket_bottom_end(area, fallpoint):
    point = (fallpoint[0], fallpoint[1] + 1)
    while True:
        if not is_clay(area['clay'], point):
            return left(point)
        assert point[0] <= area['maxx']
        point = right(point)


def fillbucket(area, fallpoint):
    water_cnt = 0
    point = fallpoint
    prev_right_bucket_edge = right_bucket_bottom_end(area, fallpoint)
    prev_left_bucket_edge = left_bucket_bottom_end(area, fallpoint)
    while True:
        left_bucket_edge = left_bucket_border(prev_left_bucket_edge, area,
                                              point)
        right_bucket_edge = right_bucket_border(prev_right_bucket_edge, area,
                                                point)
        fallpoints = []
        if left_bucket_edge is None:
            fallpoints.append(left((prev_left_bucket_edge[0], point[1])))
            left_bucket_edge = fallpoints[-1]
        if right_bucket_edge is None:
            fallpoints.append(right((prev_right_bucket_edge[0], point[1])))
            right_bucket_edge = fallpoints[-1]

        water_cnt += amount_of_water_in_bucket_line(left_bucket_edge,
                                                    right_bucket_edge, point)
        if fallpoints:
            return (water_cnt, fallpoints)
        prev_left_bucket_edge = left_bucket_edge
        prev_right_bucket_edge = right_bucket_edge
        point = above(point)


def part1(clay_set):
    fallpoints = [(500, 0)]
    area = {
        'minx': min(clay_set, key=lambda c: c[0])[0],
        'maxx': max(clay_set, key=lambda c: c[0])[0],
        'miny': min(clay_set, key=lambda c: c[1])[1],
        'maxy': max(clay_set, key=lambda c: c[1])[1],
        'clay': clay_set
    }
    water_cnt = 0
    while True:
        newfallpoints = []
        for i in range(len(fallpoints)):
            fallpoint = fallpoints[i]
            if is_clay(area['clay'], below(fallpoint)):
                print("Entering bucket at: {}".format(fallpoint))
                (water, new_fall_points) = fillbucket(area, fallpoint)
                newfallpoints += new_fall_points
                water_cnt += water + 1
            else:
                if fallpoint[1] >= area['miny'] and fallpoint[1] <= area[
                        'maxy']:
                    water_cnt += 1
                newfallpoints.append(below(fallpoint))
        fallpoints = newfallpoints
        if any([p[1] <= area['maxy'] for p in fallpoints]) == 0:
            break
        if fallpoints[0][1] % 100 == 0:
            print("Reached: {}".format(fallpoints))
    return water_cnt


clay = set(claycoordinates(sys.stdin.readlines()))
render(clay)
print("Part1: {}".format(part1(clay)))