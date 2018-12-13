#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import itertools
import sys

possible_movements = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
LEFT_MOVES = {'>': '^', '^': '<', '<': 'v', 'v': '>'}
LEFT = -1
STRAIGHT = 0
RIGHT_MOVES = {'>': 'v', 'v': '<', '<': '^', '^': '>'}
RIGHT = 1

CORNER_MOVES = {
    '\\': {
        ">": 'v',
        'v': '>',
        '<': '^',
        '^': '<'
    },
    '/': {
        ">": '^',
        '^': '>',
        '<': 'v',
        'v': '<'
    }
}


class Cart():
    def __init__(self, id, x, y, direction):
        self.id = id
        self.x = x
        self.y = y
        self.direction = direction
        self.turns = itertools.cycle([LEFT, STRAIGHT, RIGHT])

    def __eq__(self, othercart):
        return self.id == othercart.id

    def __lt__(self, othercart):
        if self.y < othercart.y:
            return True
        if self.y == othercart.y and self.x < othercart.x:
            return True
        return False

    def collides(self, othercart):
        return self.x == othercart.x and self.y == othercart.y

    def nextTurn(self):
        return next(self.turns)

    def __repr__(self):
        return "{}: {}".format(self.id, (self.x, self.y, self.direction))

    def determine_direction(self, grid, new_place):
        if new_place == '+':
            turn_direction = self.nextTurn()
            if turn_direction == LEFT:
                return LEFT_MOVES[self.direction]
            elif turn_direction == RIGHT:
                return RIGHT_MOVES[self.direction]
            else:
                return self.direction
        if new_place in CORNER_MOVES:
            return CORNER_MOVES[new_place][self.direction]
        return self.direction

    def __hash__(self):
        return hash(self.id)

    def move(self, grid):
        cart_step = possible_movements[self.direction]
        target_coord = (self.x + cart_step[0], self.y + cart_step[1])
        target_road = grid[target_coord[1]][target_coord[0]]
        if target_road == ' ':
            raise Exception("No valid road at {}: {}".format(
                target_coord, target_road))

        self.direction = self.determine_direction(grid, target_road)
        self.x = target_coord[0]
        self.y = target_coord[1]


def find_collisions(cart_to_check, allcarts):
    collisions = set()
    for cart in allcarts:
        if cart_to_check.id == cart.id:
            continue
        if cart_to_check.collides(cart):
            collisions.add(cart)
            collisions.add(cart_to_check)
    return collisions


def part1(grid, carts):
    newcarts = list(carts)
    collisions = []
    while True:
        for cart in newcarts:
            cart.move(grid)
            collisions = find_collisions(cart, newcarts)
            if len(collisions) > 0:
                return collisions
        newcarts = sorted(newcarts)
    return collisions


def part2(grid, carts):
    newcarts = list(carts)
    while len(newcarts) > 1:
        collided_carts = set()
        for cart in newcarts:
            if cart in collided_carts:
                continue
            cart.move(grid)
            collisions = find_collisions(cart, newcarts)
            for colliding_cart in collisions:
                collided_carts.add(colliding_cart)
        for cart in collided_carts:
            newcarts.remove(cart)
        newcarts = list(sorted(newcarts))
    return newcarts


grid = list(map(lambda l: list(l[:-1]), sys.stdin.readlines()))
idgen = itertools.count()
carts = [
    Cart(next(idgen), i, j, x) for (j, y) in enumerate(grid)
    for (i, x) in enumerate(y) if x in ('>', '<', '^', 'v')
]

print("Part1: {}".format(part1(grid, carts)))
carts = [
    Cart(next(idgen), i, j, x) for (j, y) in enumerate(grid)
    for (i, x) in enumerate(y) if x in ('>', '<', '^', 'v')
]
print("Part2: {}".format(part2(grid, carts)))