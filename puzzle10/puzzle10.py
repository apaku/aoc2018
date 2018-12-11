#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import re
import sys

point_re = re.compile(r'.*<([^>]+)>[^<]+<([^>]+)>.*')

def parse(line):
    match = point_re.match(line)
    point = match.group(1).split(", ")
    velocity = match.group(2).split(", ")
    return ((int(point[0].strip()), int(point[1].strip())),
            (int(velocity[0].strip()), int(velocity[1].strip())))

def renderPointAtTime(point_vel, numSeconds):
    point = point_vel[0]
    velocity = point_vel[1]
    return (point[0] + velocity[0] * numSeconds, point[1] + velocity[1] * numSeconds)

def areaAt(pointinfo, numSeconds):
    points = list(map(lambda x: renderPointAtTime(x, numSeconds), pointinfo))
    xmin = min(map(lambda p: p[0], points))
    xmax = max(map(lambda p: p[0], points))
    ymin = min(map(lambda p: p[1], points))
    ymax = max(map(lambda p: p[1], points))
    return (xmax - xmin) * (ymax - ymin)

def render(pointinfo, numSeconds):
    points = list(map(lambda x: renderPointAtTime(x, numSeconds), pointinfo))
    xmin = min(map(lambda p: p[0], points))
    xmax = max(map(lambda p: p[0], points))
    ymin = min(map(lambda p: p[1], points))
    ymax = max(map(lambda p: p[1], points))
    drawarea = []
    for y in range(ymin, ymax + 1):
        drawarea.append( list( ' ' * (xmax + 1 - xmin) ) )
    for p in points:
        lineidx = p[1] - ymin
        colidx = p[0] - xmin
        drawarea[lineidx][colidx] = '*'
    
    with open('/tmp/drawing_{}.txt'.format(numSeconds), 'w') as f:
        for line in drawarea:
            f.write("{}\n".format(''.join(line)))

points = list(map(parse, sys.stdin.readlines()))

minarea = min(enumerate([areaAt(points, x) for x in range(20000)]), key=lambda x: x[1])
print("minarea in 20k seconds: {}".format(minarea))
render(points, minarea[0])