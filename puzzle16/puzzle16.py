#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import ast
import sys


def parse_reg(s):
    return [x for x in ast.literal_eval(s.strip())]


def parse_instr(s):
    return [int(x.strip()) for x in s.strip().split(' ')]


def parseSamples(lines):
    for i in range(len(lines)):
        line = lines[i]
        if 'Before' in line:
            before_reg = parse_reg(line[len('Before: '):])
            calc = parse_instr(lines[i + 1])
            after_reg = parse_reg(lines[i + 2][len('After: '):])
            yield (before_reg, calc, after_reg)


def addi(registers, op1, op2, result):
    registers[result] = registers[op1] + op2
    return registers


def addr(registers, op1, op2, result):
    registers[result] = registers[op1] + registers[op2]
    return registers


def mulr(registers, op1, op2, result):
    registers[result] = registers[op1] * registers[op2]
    return registers


def muli(registers, op1, op2, result):
    registers[result] = registers[op1] * op2
    return registers


def borr(registers, op1, op2, result):
    registers[result] = registers[op1] | registers[op2]
    return registers


def bori(registers, op1, op2, result):
    registers[result] = registers[op1] | op2
    return registers


def banr(registers, op1, op2, result):
    registers[result] = registers[op1] & registers[op2]
    return registers


def bani(registers, op1, op2, result):
    registers[result] = registers[op1] & op2
    return registers


def setr(registers, op1, op2, result):
    registers[result] = registers[op1]
    return registers


def seti(registers, op1, op2, result):
    registers[result] = op1
    return registers


def eqir(registers, op1, op2, result):
    registers[result] = 1 if op1 == registers[op2] else 0
    return registers


def eqri(registers, op1, op2, result):
    registers[result] = 1 if registers[op1] == op2 else 0
    return registers


def eqrr(registers, op1, op2, result):
    registers[result] = 1 if registers[op1] == registers[op2] else 0
    return registers


def gtir(registers, op1, op2, result):
    registers[result] = 1 if op1 > registers[op2] else 0
    return registers


def gtri(registers, op1, op2, result):
    registers[result] = 1 if registers[op1] > op2 else 0
    return registers


def gtrr(registers, op1, op2, result):
    registers[result] = 1 if registers[op1] > registers[op2] else 0
    return registers


operations = [
    addi, addr, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri,
    gtrr, eqir, eqri, eqrr
]


def analyze_samples(sample_calcs):
    for calc in sample_calcs:
        instr = calc[1]
        matching_ops = []
        for op in operations:
            result_reg = op(list(calc[0]), instr[1], instr[2], instr[3])
            if result_reg == calc[2]:
                matching_ops.append(op)
        yield (matching_ops, instr[0])


def part1(analyzations):
    return len(list(filter(lambda x: len(x[0]) > 2, analyzations)))


def determine_opcodes(analyzations):
    opcode_map = {}
    while len(opcode_map.keys()) < 16:
        new_analyzations = []
        for analyzation in analyzations:
            if len(analyzation[0]) > 1:
                new_analyzations.append(analyzation)
            elif len(analyzation[0]) == 1 and analyzation[1] not in opcode_map:
                opcode_map[analyzation[1]] = analyzation[0][0]
        analyzations = []
        for analyzation in new_analyzations:
            newops = []
            for op in analyzation[0]:
                if op not in opcode_map.values():
                    newops.append(op)
            analyzations.append((newops, analyzation[1]))
    return opcode_map


def parseProgram(lines):
    lastLineWithBefore = 0
    for i in range(len(lines)):
        if 'Before' in lines[i]:
            lastLineWithBefore = i

    for i in range(lastLineWithBefore + 4, len(lines)):
        if len(lines[i].strip()) > 0:
            yield parse_instr(lines[i])


def part2(opcode_map, instructions):
    registers = [0, 0, 0, 0]
    for instruction in instructions:
        op = opcode_map[instruction[0]]
        op(registers, instruction[1], instruction[2], instruction[3])
    return registers


lines = sys.stdin.readlines()
analyzations = list(analyze_samples(parseSamples(lines)))
print("Part1: {}".format(part1(analyzations)))
opcode_map = determine_opcodes(list(analyzations))

print("Part2: {}".format(part2(opcode_map, parseProgram(lines))))