#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
# License: MIT

import ast
import sys


def parse_reg(s):
    return [x for x in ast.literal_eval(s.strip())]


def parse_instr(s):
    values = s.split(" ")
    return (values[0], int(values[1]), int(values[2]), int(values[3]))


def parse(lines):
    ipreg = -1
    instructions = []
    for line in lines:
        if "#ip" in line:
            ipreg = int(line[4:])
        else:
            instructions.append(parse_instr(line))
    return (ipreg, instructions)


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


operations = {
    'addi': addi,
    'addr': addr,
    'mulr': mulr,
    'muli': muli,
    'banr': banr,
    'bani': bani,
    'borr': borr,
    'bori': bori,
    'setr': setr,
    'seti': seti,
    'gtir': gtir,
    'gtri': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def part1(reg0_startvalue, ipreg, instructions):
    registers = [reg0_startvalue, 0, 0, 0, 0, 0]
    instr_pointer = 0
    instructions_size = len(instructions)
    maxnum = 0
    instructioncnt = 0
    seenvalues = set()
    while instr_pointer < instructions_size:
        registers[ipreg] = instr_pointer
        instruction = instructions[instr_pointer]
        if instr_pointer == 28:
            if registers[2] in seenvalues:
                print("Found loop for {}".format(registers[2]))
                break
            seenvalues.add(registers[2])
            print("Found a candiate number: {}".format(registers[2]))
        op = operations[instruction[0]]
        op(registers, instruction[1], instruction[2], instruction[3])
        instr_pointer = registers[ipreg]
        instr_pointer += 1
        instructioncnt += 1
    return (registers, instructioncnt)


def part2(ipreg, instructions):
    results = sorted([part1(num, ipreg, instructions) for num in targetnums],
                     key=lambda x: x[1])
    return (max(results, key=lambda x: x[1]), list(results))


(ipreg, instructions) = parse(sys.stdin.readlines())
# Number must be between 0 and 2^24 - 1, it's cut off with one of the instructions
#
print("Part1, reg0=1, {}".format(part1(30842, ipreg, instructions)))
# This must be something below the 16777215 I think, but how far away?
part1(155015535680, ipreg, instructions)
#print("Part2, {}".format(part2(ipreg, instructions)))
