// Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
// License: MIT

use std::io::{BufRead};
extern crate regex;
use regex::Regex;
use std::cmp;

#[derive(Debug, Copy, Clone, Eq, PartialEq, Hash)]
struct Point {
    x: i32,
    y: i32
}
#[derive(Debug, Copy, Clone)]
struct Rect {
    id: i32,
    tl: Point,
    br: Point
}

fn overlaps(r1: &Rect, r2: &Rect ) -> bool {
    return r1.tl.x < r2.br.x && r1.br.x > r2.tl.x && 
        r1.tl.y < r2.br.y && r1.br.y > r2.tl.y;
}

fn overlap(r1: &Rect, r2: &Rect) -> HashSet<Point> {
    let mut points = HashSet::new();
    if !overlaps( r1, r2 ) {
        if overlaps( r2, r1 ) {
            return overlap(r2, r1);
        }
        return points;
    }
    let overlaptl = Point {
        x: cmp::max(r1.tl.x, r2.tl.x),
        y: cmp::max(r1.tl.y, r2.tl.y)
    };
    let overlapbr = Point {
        x: cmp::min(r1.br.x, r2.br.x),
        y: cmp::min(r1.br.y, r2.br.y)
    };
    for x in overlaptl.x..overlapbr.x {
        for y in overlaptl.y..overlapbr.y {
            let p = Point {
                x: x,
                y: y
            };
            points.insert(p);
        }
    }
    return points;
}

fn overlappedpoints(r: &Rect, others: &Vec<Rect>) -> HashSet<Point> {
    let mut allpoints = HashSet::new();
    for otherrect in others {
        let overlaps = overlap(r, otherrect);
        allpoints = allpoints.union(&overlaps).map(|p| Point { x: p.x, y: p.y }).collect();
    }
    if others.len() > 1 {
        let (nextrect, rest) = others.split_first().unwrap();
        let overlaps = overlappedpoints(nextrect, &rest.to_vec());
        allpoints = allpoints.union(&overlaps).map(|p| Point { x: p.x, y: p.y }).collect();
    }
    return allpoints;
}

fn part1(patches: &Vec<Rect>) -> usize {
    let (head, tail) = patches.split_first().unwrap();
    let allpoints = overlappedpoints( head, &tail.to_vec());
    return allpoints.len();
}

}

fn parse(lines: &Vec<String>) -> Vec<Rect> {
    let re = Regex::new(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$").unwrap();
    let mut rects = Vec::new();
    for line in lines {
        let caps = re.captures(line).unwrap();
        let tl = Point {
                x: (&caps[2]).parse::<i32>().unwrap(),
                y: (&caps[3]).parse::<i32>().unwrap()
        };
        let br = Point {
                x: tl.x + (&caps[4]).parse::<i32>().unwrap(),
                y: tl.y + (&caps[5]).parse::<i32>().unwrap()
        };
        let patch = Rect {
            id: caps[1].parse::<i32>().unwrap(),
            tl: tl,
            br: br
        };
        rects.push(patch);
    }
    return rects;
}

fn main() {
    let stdin = std::io::stdin();
    let lines: Vec<String> = stdin.lock().lines().map(|l| l.unwrap()).collect();
    let patches = parse(&lines);
    println!("Part1: {}", part1(&patches));
    println!("Part2: {:?}", part2(&lines));
}
