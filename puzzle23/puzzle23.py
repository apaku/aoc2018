#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import re
import sys


class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "{},{},{}".format(self.x, self.y, self.z)


class nanobot:
    def __init__(self, id, pos, signalradius):
        self.id = id
        self.signalradius = signalradius
        self.pos = pos

    def __repr__(self):
        return "{}/{}".format(self.pos, self.signalradius)


bot_re = re.compile(r'pos=<([^,]+),([^,]+),([^,]+)>, r=([^,]+)')


def parse(lines):
    bot_id = 0
    for line in lines:
        match = bot_re.match(line)
        yield nanobot(
            bot_id,
            point(
                int(match.group(1)), int(match.group(2)), int(match.group(3))),
            int(match.group(4)))
        bot_id += 1


def distance(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y) + abs(pos1.z - pos2.z)


def inrange(bot, pos):
    return distance(bot.pos, pos) <= bot.signalradius


def part1(bots):
    bot_with_max_radius = max(bots, key=lambda x: x.signalradius)
    reachable_bots = len(
        list(filter(lambda x: inrange(bot_with_max_radius, x.pos), bots)))
    return bot_with_max_radius, reachable_bots


# Somehow work out the intersection of the cubes the bots can reach
# and then take the one with the most bots on it
cubes = {}


def bot_cube(bot):
    def helper(bot):
        for z in range(bot.pos.z - bot.signalradius,
                       bot.pos.z + bot.signalradius + 1):
            for y in range(bot.pos.y - bot.signalradius,
                           bot.pos.y + bot.signalradius + 1):
                for x in range(bot.pos.x - bot.signalradius,
                               bot.pos.x + bot.signalradius + 1):
                    yield point(x, y, z)

    if bot.id not in cubes:
        cubes[bot.id] = set(helper(bot))
    return cubes[bot.id]


def bots_in_range(p, bots):
    return list(filter(lambda bot: inrange(bot, p), bots))


def part2(bots):
    def helper(bots):
        minx = min(map(lambda bot: bot.pos.x, bots))
        maxx = max(map(lambda bot: bot.pos.x, bots))
        miny = min(map(lambda bot: bot.pos.y, bots))
        maxy = max(map(lambda bot: bot.pos.y, bots))
        minz = min(map(lambda bot: bot.pos.z, bots))
        maxz = max(map(lambda bot: bot.pos.z, bots))
        for z in range(minz, maxz + 1):
            print("z: {}".format(z))
            for y in range(miny, maxy + 1):
                print("y: {}".format(y))
                for x in range(minx, maxx + 1):
                    p = point(x, y, z)
                    yield (p, distance(point(0, 0, 0), p),
                           len(bots_in_range(p, bots)))

    max(helper(bots), key=lambda x: (x[2], x[1]))


bots = list(parse(sys.stdin.readlines()))
print("Part1: {}".format(part1(bots)))
print("Part2: {}".format(part2(bots)))
