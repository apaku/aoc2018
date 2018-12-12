#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import re
import sys

def parse_plant_str(state_str):
    return map(lambda x: 1 if x == '#' else 0, state_str)

def parse(lines):
    initial_state = lines[0][len("initial state: "):]
    grow_transitions = set()
    transition_re = re.compile(r'([^ ]+) => #')
    for line in lines[2:]:
        match = transition_re.match(line.strip())
        if match is None:
            continue
        grow_transitions.add(tuple(parse_plant_str(match.group(1))))
    return (list(parse_plant_str(initial_state)), grow_transitions)

def transition(state, transitions):
    newstate = [0,0]
    for i in range(2, len(state)):
        sublist = state[i-2:i+3]
        if tuple(sublist) in transitions:
            newstate.append(1)
        else:
            newstate.append(0)
    return newstate

def transition_to_generation(startstate, transitions, generation):
    newstate = [0, 0, 0, 0, 0] + list(startstate) + [0,0,0,0,0]
    num_entries_to_left = 5
    for i in range(generation):
        newstate = transition(newstate, transitions)
        for j in range(4, -1, -1):
            if newstate[j] == 1:
                num_entries_to_left += 1
                newstate.insert(j, 0)
        if 1 in newstate[-5:]:
            newstate = newstate + [0,0,0,0,0]
        if i % 1000 == 0:
            print("Generation: {}".format(i))
    return sum(map(lambda x: x[0] - num_entries_to_left, filter(lambda x: x[1] == 1, enumerate(newstate))))

(initial_state, transitions) = parse(list(sys.stdin.readlines()))
print("Part1: {}".format(transition_to_generation(initial_state, transitions, 20)))
print("Part2: {}".format(transition_to_generation(initial_state, transitions, 50000000000)))
