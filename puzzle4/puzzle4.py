#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import datetime
import re
import sys

line_re = re.compile(r'\[([^\]]+)\] (.+)')
guard_re = re.compile(r'Guard #(\d+)')

def parseDates(lines):
    for line in lines:
        match = line_re.match(line)
        date = datetime.datetime.strptime(match.group(1), '%Y-%m-%d %H:%M')
        yield (date, match.group(2))
    
def parseGuardInfo(generator):
    currentgid = -1
    for (date, info) in generator:
        guard_match = guard_re.match(info)
        sleeps = False
        if guard_match is None:
            if info == 'falls asleep':
                sleeps = True
        else:
            currentgid = int(guard_match.group(1))
        yield (date, currentgid, sleeps)
class Guard:
    def __init__(self, gid):
        self.gid = gid
        self.startsleep = None
        self.sleepminutes = {}
        self.totalasleep = 0
    
    def sleep(self, date):
        self.startsleep = date
    
    def __repr__(self):
        return "{}".format({"id": self.gid, "slept": self.sleepminutes})

    def awake(self, date):
        if self.startsleep is None:
            return
        wakedate = date
        for minute in range(self.startsleep.minute, wakedate.minute):
            self.totalasleep += 1
            if minute not in self.sleepminutes:
                self.sleepminutes[minute] = 0
            self.sleepminutes[minute] += 1
        
        self.startsleep = None
def buildguards(lines):
    guards = {}

    for (day, gid, sleeps) in parseGuardInfo(sorted(parseDates(lines))):
        if gid not in guards:
            guards[gid] = Guard(gid)
        if sleeps:
            guards[gid].sleep(day)
        else:
            guards[gid].awake(day)
    return guards

def part1(guards):
    for (gid, guard) in guards.items():
        numminutes = guard.totalasleep
        maxminute = None
        if len(guard.sleepminutes) > 0:
            maxminute = max(sorted(guard.sleepminutes.items(), key=lambda x: x[1]), key=lambda x: x[1])
        yield (numminutes, maxminute, gid)

def part2(guards):
    for (gid, guard) in guards.items():
        maxminute = (0, 0)
        if len(guard.sleepminutes) > 0:
            maxminute = max(sorted(guard.sleepminutes.items(), key=lambda x: x[1]), key=lambda x: x[1])
        yield (maxminute[1], maxminute[0], gid)

guards = buildguards(sys.stdin.readlines())
part1 = max(part1(guards))
part2 = max(part2(guards))
print("Part1: {} {}".format(part1, part1[1][0] * part1[2]))
print("Part2: {} {}".format(part2, part2[1] * part2[2]))