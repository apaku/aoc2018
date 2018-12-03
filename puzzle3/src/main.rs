// Copyright 2018 Andreas Pakulat <andreaspakulat+github@gmail.com>
// License: MIT

use std::io::{BufRead};
extern crate regex;
use regex::Regex;

struct Rect {
    x: i32,
    y: i32,
    w: i32,
    h: i32
}

fn part1(lines: &Vec<Rect>) -> i32 {
    return 0;
}

fn part2(lines: &Vec<String>) -> i32 {
    return 0;
}

fn parse(lines: &Vec<String>) -> Vec<Rect> {
    let re = Regex::new(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$").unwrap();
    let mut rects = Vec::new();
    for line in lines {
        let caps = re.captures(line).unwrap();
        let patch = Rect {
            x: (&caps[1]).parse::<i32>().unwrap(),
            y: (&caps[2]).parse::<i32>().unwrap(),
            w: (&caps[3]).parse::<i32>().unwrap(),
            h: (&caps[4]).parse::<i32>().unwrap()
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
