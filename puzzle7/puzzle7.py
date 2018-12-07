#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import copy
import re
import sys

input_re = re.compile(r"Step ([^ ]+) must be finished before step ([^ ]+) can begin.")

def parse(line):
    m = input_re.match(line)
    return (m.group(2), m.group(1))

deps = [parse(line) for line in sys.stdin.readlines()]
dependencies = {}
for (dependee, dependant) in deps:
    if dependant not in dependencies:
        dependencies[dependant] = []
    if dependee not in dependencies:
        dependencies[dependee] = []
    
    dependencies[dependee].append(dependant)

def part1(dependencies):
    order = ""
    while len(dependencies) > 0:
        nextstep = list(sorted(filter(lambda x: len(x[1]) == 0, dependencies.items())))[0]
        del dependencies[nextstep[0]]
        for dep in dependencies:
            if nextstep[0] in dependencies[dep]:
                dependencies[dep].remove(nextstep[0])
        order += nextstep[0]
    return order

def part2(dependencies):
    workers = {"1": None, "2": None, "3": None, "4": None, "5": None}
    #workers = {"1": None, "2": None}
    timecount = 0
    workedon = []
    while True:
        #print("Time:{}".format(timecount))
        for worker in workers.keys():
            if workers[worker] is not None:
                #print("Worker: {} {}".format(worker, workers[worker]))
                if workers[worker][0] == 0:
                    stepdone = workers[worker][1]
                    workedon.remove(stepdone)
                    for dep in dependencies:
                        if stepdone in dependencies[dep]:
                            dependencies[dep].remove(stepdone)
                    workers[worker] = None
                else:
                    workers[worker] = (workers[worker][0] - 1, workers[worker][1])
        nextsteps = list(sorted(filter(lambda x: len(x[1]) == 0, dependencies.items())))
        #print("Next steps: {}".format(nextsteps))
        availableworkers = [worker for worker in workers.keys() if workers[worker] is None]
        for nextstep in nextsteps[0:len(availableworkers)]:
            worker = availableworkers.pop()
            #print("Starting worker: {} on step {}".format(worker, nextstep))
            workedon.append(nextstep[0])
            workers[worker] = (ord(nextstep[0]) - 65 + 60, nextstep[0])
            del dependencies[nextstep[0]]
        if len(workedon) == 0 and len(dependencies) == 0:
            break
        timecount += 1

    return timecount
    
print("Part1: {}".format(part1(copy.deepcopy(dependencies))))
print("Part2: {}".format(part2(copy.deepcopy(dependencies))))