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
    'gtir': gtri,
    'gtrr': gtrr,
    'eqir': eqir,
    'eqri': eqri,
    'eqrr': eqrr
}


def part1(ipreg, instructions):
    registers = [0, 0, 0, 0, 0, 0]
    instr_pointer = 0
    instructions_size = len(instructions)
    while instr_pointer < instructions_size:
        registers[ipreg] = instr_pointer
        instruction = instructions[instr_pointer]
        op = operations[instruction[0]]
        op(registers, instruction[1], instruction[2], instruction[3])
        instr_pointer = registers[ipreg]
        instr_pointer += 1
    return registers


def part2(ipreg, instructions):
    registers = [1, 0, 0, 0, 0, 0]
    instr_pointer = 0
    instructions_size = len(instructions)
    while instr_pointer < instructions_size:
        registers[ipreg] = instr_pointer
        instruction = instructions[instr_pointer]
        if instr_pointer == 3:
            if registers[4] % registers[1] == 0:
                registers[0] += registers[1]
            registers[2] = 11
        else:
            op = operations[instruction[0]]
            op(registers, instruction[1], instruction[2], instruction[3])
        instr_pointer = registers[ipreg]
        instr_pointer += 1
    return registers


(ipreg, instructions) = parse(sys.stdin.readlines())
print("Part1: {}".format(part1(ipreg, instructions)))
print("Part2: {}".format(part2(ipreg, instructions)))
