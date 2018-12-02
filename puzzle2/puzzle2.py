import sys

def findmismatch(l, r):
    for i in range(len(l)):
        if r[i] != l[i]:
            return i
    return None

def boxids(head, tail):
    ids = []
    for line in tail:
        nonmatchingidx = findmismatch(head, line)
        if nonmatchingidx is None:
            continue
        morenonmatch = findmismatch(head[nonmatchingidx + 1:], line[nonmatchingidx + 1:])
        if morenonmatch is None:
            ids.append(head[:nonmatchingidx] + head[nonmatchingidx + 1:])
    if len(tail) > 1:
        ids = ids + boxids(tail[0], tail[1:])
    return ids

def part2(lines):
    return boxids(lines[0], lines[1:])

print("Part2: {}".format(part2([x.strip() for x in sys.stdin.readlines()])))